require "json"
require "net/http"
require "uri"
require "fileutils"
require "dotenv"

module Obis
  class FetchObisSubgroups < Jekyll::Generator
    priority :normal

    OE_ROOT_IDS = [386, 503, 538]
    OE_BASE_URL = "https://oceanexpert.org/api/v1/group/%{group_id}.json?limit=1000"
    OE_LOGIN_URL = "https://oceanexpert.org/api/login_check"
    OBIS_NODES_URL = "https://api.obis.org/node"

    def generate(site)
      return unless build_enabled?(site)

      Dotenv.load

      cache_file = File.join(site.source, "_cache", "obis_subgroups_cache.json")
      
      if File.exist?(cache_file) && (Time.now - File.mtime(cache_file)) < 3600
        Jekyll.logger.info("OBIS", "Using cached subgroups data")
        cached_data = JSON.parse(File.read(cache_file))
        site.data["obis_subgroups"] = cached_data
        return
      end

      Jekyll.logger.info("OBIS", "Authenticating with OceanExpert...")
      auth_token = authenticate_with_oceanexpert(site)
      
      Jekyll.logger.info("OBIS", "Fetching OBIS nodes metadata...")
      obis_nodes = fetch_json(OBIS_NODES_URL)
      name_to_node = map_nodes_by_name(obis_nodes)

      Jekyll.logger.info("OBIS", "Fetching OceanExpert groups...")
      all_groups_data = {}
      
      OE_ROOT_IDS.each do |root_id|
        begin
          Jekyll.logger.info("OBIS", "Processing group #{root_id}...")
          oe_root = fetch_json(format(OE_BASE_URL, group_id: root_id), auth_token)
          
          if root_id == 386
            # For group 386, fetch subgroups with members
            subgroups = build_subgroups_with_members(oe_root, auth_token)
            prioritize_subgroup!(subgroups, 432)
            enrich_with_obis_metadata!(subgroups, name_to_node)
            all_groups_data[root_id.to_s] = subgroups
          else
            # For groups 503 and 538, fetch only members
            members = extract_members(oe_root)
            sort_members_by_last_name!(members)
            all_groups_data[root_id.to_s] = members
          end
        rescue => e
          Jekyll.logger.warn("OBIS", "Failed to process group #{root_id}: #{e.class}: #{e.message}")
          all_groups_data[root_id.to_s] = []
        end
      end

      FileUtils.mkdir_p(File.dirname(cache_file))
      File.write(cache_file, JSON.pretty_generate(all_groups_data))
      Jekyll.logger.info("OBIS", "Cached subgroups data to #{cache_file}")

      site.data["obis_subgroups"] = all_groups_data
    rescue => e
      Jekyll.logger.warn("OBIS", "Failed to fetch OceanExpert groups: #{e.class}: #{e.message}")
    end

    private

    def build_enabled?(site)
      site.config.fetch("obis_fetch_subgroups", true)
    end

    def authenticate_with_oceanexpert(site)
      username = ENV["OCEANEXPERT_USERNAME"]
      password = ENV["OCEANEXPERT_PASSWORD"]
      
      unless username && password
        Jekyll.logger.warn("OBIS", "OceanExpert credentials not found in environment variables (OCEANEXPERT_USERNAME, OCEANEXPERT_PASSWORD), proceeding without authentication")
        return nil
      end

      uri = URI.parse(OE_LOGIN_URL)
      Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == "https") do |http|
        req = Net::HTTP::Post.new(uri.request_uri)
        req["User-Agent"] = "obisnew-jekyll-plugin/1.0 (+https://obis.org)"
        req["Content-Type"] = "application/json"
        req.body = JSON.generate({
          "username" => username,
          "password" => password
        })
        
        http.read_timeout = 30
        http.open_timeout = 10
        res = http.request(req)
        
        unless res.is_a?(Net::HTTPSuccess)
          raise "Authentication failed: HTTP #{res.code} for #{OE_LOGIN_URL}"
        end
        
        response_data = JSON.parse(res.body)
        token = response_data["token"]
        
        unless token
          raise "No token received from OceanExpert authentication"
        end
        
        Jekyll.logger.info("OBIS", "Successfully authenticated with OceanExpert")
        token
      end
    rescue => e
      Jekyll.logger.warn("OBIS", "OceanExpert authentication failed: #{e.class}: #{e.message}")
      nil
    end

    def http_get(uri_str, auth_token = nil)
      uri = URI.parse(uri_str)
      Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == "https") do |http|
        req = Net::HTTP::Get.new(uri.request_uri)
        req["User-Agent"] = "obisnew-jekyll-plugin/1.0 (+https://obis.org)"
        req["Accept"] = "application/json"
        req["Authorization"] = "Bearer #{auth_token}" if auth_token
        http.read_timeout = 30
        http.open_timeout = 10
        res = http.request(req)
        unless res.is_a?(Net::HTTPSuccess)
          raise "HTTP #{res.code} for #{uri_str}"
        end
        res.body
      end
    end

    def fetch_json(url, auth_token = nil)
      body = http_get(url, auth_token)
      JSON.parse(body)
    end

    def extract_members(group_json)
      members = group_json["members"]
      return [] if members.nil?
      
      # Members can be a hash (object) or already an array
      if members.is_a?(Hash)
        # Convert hash to array of values, filtering out any nil values
        members.values.compact
      elsif members.is_a?(Array)
        members.compact
      else
        []
      end
    end

    def build_subgroups_with_members(root_group_json, auth_token = nil)
      subgroups = root_group_json.fetch("subGroups", []) || []
      subgroups.map do |sg|
        sg_id = sg["idGroup"]
        next nil if sg_id.nil?
        details = fetch_json(format(OE_BASE_URL, group_id: sg_id), auth_token)
        members = extract_members(details)
        sort_members!(members)

        {
          "idGroup" => details.fetch("idGroup", sg_id),
          "groupname" => details.fetch("groupname", sg["groupname"]),
          "members" => members
        }
      end.compact
    end

    def map_nodes_by_name(obis_nodes)
      results = obis_nodes.fetch("results", []) || []
      mapping = {}
      results.each do |node|
        name = node["name"]
        mapping[name] = node if name && !name.empty?
      end
      mapping
    end

    def enrich_with_obis_metadata!(groups, name_to_node)
      groups.each do |g|
        node = name_to_node[g["groupname"]]
        next unless node
        urls = node["url"] || []
        g["id"] = node["id"]
        g["lat"] = node["lat"]
        g["lon"] = node["lon"]
        g["description"] = node["description"]
        g["url"] = urls.is_a?(Array) ? (urls.first || nil) : urls
      end
    end

    def sort_members!(members)
      sorted = members.each_with_index.sort_by do |member, idx|
        role = member.fetch("groupRole", "")
        normalized_role = role.to_s.downcase

        priority = if normalized_role.include?("obis manager")
          0
        elsif normalized_role.include?("node manager")
          1
        elsif normalized_role.include?("manager")
          2
        else
          3
        end

        [priority, idx]
      end.map(&:first)

      members.replace(sorted)
    end

    def sort_members_by_last_name!(members)
      return if members.nil? || members.empty?
      
      sorted = members.sort_by do |member|
        member.fetch("lname", "").to_s.downcase
      end

      members.replace(sorted)
    end

    def prioritize_subgroup!(groups, target_id)
      idx = groups.index { |g| g["idGroup"].to_s == target_id.to_s }
      return if idx.nil? || idx.zero?
      groups.unshift(groups.delete_at(idx))
    end
  end
end


