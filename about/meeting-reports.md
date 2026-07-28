---
identifier: meeting-reports
lang: en
layout: page_narrow
shorttitle: Meeting reports
title: Meeting reports
---

# Meeting reports

Official reports of OBIS Steering Group (SG-OBIS) and Executive Committee (OBIS-EC) meetings.

{% assign reports = site.data.meeting_reports %}

{% if reports.steering_group and reports.steering_group.size > 0 %}
## OBIS Steering Group (SG-OBIS)

<table class="table-meeting-reports">
  <thead>
    <tr>
      <th>Meeting</th>
      <th>Report</th>
    </tr>
  </thead>
  <tbody>
    {% for report in reports.steering_group %}
    <tr>
      <td>{{ report.meeting_date_label }}</td>
      <td><a href="{{ report.url }}" target="_blank" rel="noopener">{{ report.title }}</a></td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endif %}

{% if reports.executive_committee and reports.executive_committee.size > 0 %}
## OBIS Executive Committee (OBIS-EC)

<table class="table-meeting-reports">
  <thead>
    <tr>
      <th>Meeting</th>
      <th>Report</th>
    </tr>
  </thead>
  <tbody>
    {% for report in reports.executive_committee %}
    <tr>
      <td>{{ report.meeting_date_label }}</td>
      <td><a href="{{ report.url }}" target="_blank" rel="noopener">{{ report.title }}</a></td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endif %}

{% if reports.other and reports.other.size > 0 %}
## Other

<table class="table-meeting-reports">
  <thead>
    <tr>
      <th>Meeting</th>
      <th>Report</th>
    </tr>
  </thead>
  <tbody>
    {% for report in reports.other %}
    <tr>
      <td>{{ report.meeting_date_label }}</td>
      <td><a href="{{ report.url }}" target="_blank" rel="noopener">{{ report.title }}</a></td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endif %}

{% unless reports.reports and reports.reports.size > 0 %}
<p>Meeting reports could not be loaded right now. Please try again later, or browse them on <a href="https://oceanexpert.org/documentList/238">OceanExpert</a>.</p>
{% endunless %}
