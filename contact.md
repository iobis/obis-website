---
layout: page
title: Contact
permalink: /contact/
---

<div class="section-light">

<h1>Team and contacts</h1>

<p>For general enquiries and technical questions, contact the OBIS Secretariat at <a href="mailto:helpdesk@obis.org">helpdesk@obis.org</a>.</p>

{% assign nodes = site.data.obis_subgroups['386'] %}
{% for node in nodes %}
  <section class="section-superdense">
    <h4 class="nodename">{{ node.groupname }}</h4>
    <p>
    {% if node.url %}
        <a href="{{ node.url }}" target="_blank">Website</a> | 
    {% endif %}
    <a href="/node/{{ node.id }}" target="_blank">Node page</a>
    </p>

    <div class="row contacts">
        {% for contact in node.members %}
        <div class="col-md-3 contact">
            <p><b><a href="https://oceanexpert.org/expert/{{ contact.idInd }}" target="_blank">{{ contact.fname }} {{ contact.lname }}</a></b>
            {% if contact.groupRole and contact.groupRole != "" %}
            <br/><span class="contact-role">{{ contact.groupRole }}</span>
            {% endif %}
            {% if contact.email1 %}
            <br/><span class="contact-email">{{ contact.email1 }}</span>
            {% endif %}
            </p>
        </div>
        {% endfor %}
    </div>
  </section>
{% endfor %}

</div>