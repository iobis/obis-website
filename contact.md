---
layout: page
title: Contact
permalink: /contact/
---

<div class="section-light">

<h1>Team and contacts</h1>

{% assign nodes = site.data.obis_subgroups %}
{% for node in nodes %}
  <section class="section-superdense">
    <h4 class="nodename">{{ node.groupname }}</h4>
    <p>
    {% for u in node.url %}
        <a href="{{ u }}" target="_blank">{{ u }}</a>
    {% endfor %}
    </p>

    <div class="row">
        {% for contact in node.members %}
        <div class="col-md-3">
            <p><b>{{ contact.fname }} {{ contact.lname }}</b>
            {% if contact.groupRole %}
            <br/>{{ contact.groupRole }}
            {% endif %}
            {% if contact.email1 %}
            <br/><a href="mailto:{{ contact.email1 }}">{{ contact.email1 }}</a>
            {% endif %}
            </p>
        </div>
        {% endfor %}
    </div>
  </section>
{% endfor %}

</div>