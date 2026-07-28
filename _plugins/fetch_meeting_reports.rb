require "json"
require "net/http"
require "uri"
require "fileutils"
require "time"
require "date"
require "dotenv"

module Obis
  class FetchMeetingReports < Jekyll::Generator
    priority :normal

    DOCLIST_URL = "https://oceanexpert.org/api/v1/document/viewDoclistRecord/238.json"
    CALENDAR_URL = "https://oceanexpert.org/api/v1/getEventCalendar/269.json?start=2010-01-01&end=2030-12-31"
    EVENT_DOCS_URL = "https://oceanexpert.org/api/v1/event/viewEventDocs/%{event_id}.json"
    DOCUMENT_URL = "https://oceanexpert.org/document/%{doc_id}"
    EVENT_URL = "https://oceanexpert.org/event/%{event_id}"

    def generate(site)
      return unless site.config.fetch("obis_fetch_meeting_reports", true)

      Dotenv.load

      cache_file = File.join(site.source, "_cache", "meeting_reports_cache.json")
      if File.exist?(cache_file) && (Time.now - File.mtime(cache_file)) < 3600
        Jekyll.logger.info("OBIS", "Using cached meeting reports data")
        site.data["meeting_reports"] = JSON.parse(File.read(cache_file))
        return
      end

      Jekyll.logger.info("OBIS", "Fetching OceanExpert meeting reports...")
      doclist = fetch_json(DOCLIST_URL)
      documents = doclist.fetch("documents", []) || []

      Jekyll.logger.info("OBIS", "Fetching OBIS event calendar for meeting dates...")
      calendar = fetch_json(CALENDAR_URL)
      events = flatten_calendar_events(calendar.fetch("events", {}) || {})
      meeting_events = events.select { |event| meeting_event?(event) }

      wanted_ids = documents.map { |doc| doc["idDoc"] }.compact
      wanted_codes = documents.map { |doc| normalize_code(doc["docCode"]) }.reject(&:empty?)

      by_id = {}
      by_code = {}

      meeting_events.each do |event|
        begin
          payload = fetch_json(format(EVENT_DOCS_URL, event_id: event["idEvent"]))
          docs_block = ((payload["event"] || {})["documents"] || {})
          docs_block.each_value do |arr|
            next unless arr.is_a?(Array)

            arr.each do |doc|
              meta = event_meta(event)
              id = doc["idDoc"]
              code = normalize_code(doc["docCode"])

              next unless wanted_ids.include?(id) || wanted_codes.include?(code)

              by_id[id] ||= meta if id
              by_code[code] ||= meta unless code.empty?
            end
          end
        rescue => e
          Jekyll.logger.warn("OBIS", "Failed to fetch docs for event #{event["idEvent"]}: #{e.class}: #{e.message}")
        end
      end

      reports = documents.map do |doc|
        code = normalize_code(doc["docCode"])
        meta = by_id[doc["idDoc"]] || by_code[code] || {}
        category = categorize(doc)

        {
          "idDoc" => doc["idDoc"],
          "docCode" => (doc["docCode"] || "").strip,
          "title" => doc["title"],
          "url" => format(DOCUMENT_URL, doc_id: doc["idDoc"]),
          "category" => category,
          "event_id" => meta["idEvent"],
          "event_title" => meta["eventTitle"],
          "event_url" => meta["idEvent"] ? format(EVENT_URL, event_id: meta["idEvent"]) : nil,
          "start_on" => meta["startOn"],
          "end_on" => meta["endOn"],
          "meeting_date_label" => format_date_range(meta["startOn"], meta["endOn"]),
          "sort_date" => meta["startOn"] || doc["publishedOn"]
        }
      end

      reports.sort_by! { |report| report["sort_date"] || "" }
      reports.reverse!

      data = {
        "doclist" => doclist["doclist"],
        "reports" => reports,
        "steering_group" => reports.select { |r| r["category"] == "steering_group" },
        "executive_committee" => reports.select { |r| r["category"] == "executive_committee" },
        "other" => reports.select { |r| r["category"] == "other" }
      }

      FileUtils.mkdir_p(File.dirname(cache_file))
      File.write(cache_file, JSON.pretty_generate(data))
      Jekyll.logger.info("OBIS", "Cached #{reports.size} meeting reports")

      site.data["meeting_reports"] = data
    rescue => e
      Jekyll.logger.warn("OBIS", "Failed to fetch meeting reports: #{e.class}: #{e.message}")
      site.data["meeting_reports"] ||= { "reports" => [], "steering_group" => [], "executive_committee" => [], "other" => [] }
    end

    private

    def http_get(uri_str)
      uri = URI.parse(uri_str)
      Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == "https") do |http|
        req = Net::HTTP::Get.new(uri.request_uri)
        req["User-Agent"] = "obisnew-jekyll-plugin/1.0 (+https://obis.org)"
        req["Accept"] = "application/json"
        http.read_timeout = 60
        http.open_timeout = 15
        res = http.request(req)
        unless res.is_a?(Net::HTTPSuccess)
          raise "HTTP #{res.code} for #{uri_str}"
        end
        res.body
      end
    end

    def fetch_json(url)
      JSON.parse(http_get(url))
    end

    def flatten_calendar_events(events)
      items = []
      case events
      when Hash
        events.each_value do |value|
          if value.is_a?(Array)
            items.concat(value)
          elsif value.is_a?(Hash)
            items << value
          end
        end
      when Array
        items.concat(events)
      end
      items
    end

    def meeting_event?(event)
      title = "#{event["title"]} #{event["shorttitle"]}"
      return true if title.match?(/EC-OBIS|OBIS-EC|SG-OBIS/i)
      return true if title.match?(/OBIS.*Executive Comm?ittee|Executive Comm?ittee.*OBIS/i)
      return true if title.match?(/Steering Group.*OBIS|OBIS.*Steering Group/i)
      false
    end

    def event_meta(event)
      {
        "idEvent" => event["idEvent"],
        "eventTitle" => event["title"],
        "startOn" => event["startOn"],
        "endOn" => event["endOn"]
      }
    end

    def normalize_code(code)
      code.to_s.strip.gsub(/\s+/, "")
    end

    def categorize(doc)
      code = normalize_code(doc["docCode"])
      title = doc["title"].to_s
      return "executive_committee" if code.match?(/\AEC-OBIS/i) || title.match?(/Executive Comm?ittee/i)
      return "steering_group" if code.match?(/SG-OBIS/i) || title.match?(/Steering Group/i) || code == "WR237"
      "other"
    end

    def format_date_range(start_on, end_on)
      start_date = parse_date(start_on)
      end_date = parse_date(end_on)
      return nil unless start_date

      if end_date.nil? || end_date == start_date
        return start_date.strftime("%-d %B %Y")
      end

      if start_date.year == end_date.year && start_date.month == end_date.month
        "#{start_date.strftime("%-d")}-#{end_date.strftime("%-d %B %Y")}"
      elsif start_date.year == end_date.year
        "#{start_date.strftime("%-d %B")} - #{end_date.strftime("%-d %B %Y")}"
      else
        "#{start_date.strftime("%-d %B %Y")} - #{end_date.strftime("%-d %B %Y")}"
      end
    end

    def parse_date(value)
      return nil if value.nil? || value.to_s.strip.empty?
      Time.parse(value.to_s).to_date
    rescue ArgumentError
      nil
    end
  end
end
