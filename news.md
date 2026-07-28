---
layout: page
---

<div class="container">
  <h1>News</h1>
  <div class="mt-5">
      {% assign all_posts = site.posts | sort: 'date' | reverse %}
      {% include post_cards.html filtered_posts=all_posts %}
  </div>
</div>
