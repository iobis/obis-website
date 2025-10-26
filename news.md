---
layout: page
pagination:
  enabled: true
  collection: posts
  per_page: 12
---

<div class="container">
  <h1>News</h1>
  <div class="mt-5">
      {% include post_cards.html filtered_posts=paginator.posts limit=12 %}
  </div>
  
  <!-- Pagination links -->
  {% if paginator.total_pages > 1 %}
  <nav aria-label="Page navigation" class="mt-5 text-center">
    {% if paginator.previous_page %}
      <a href="{{ paginator.previous_page_path }}">Previous</a>
    {% endif %}
    
    {% if paginator.previous_page and paginator.next_page %}
      <span class="mx-3">|</span>
    {% endif %}
    
    {% if paginator.next_page %}
      <a href="{{ paginator.next_page_path }}">Next</a>
    {% endif %}
  </nav>
  {% endif %}
</div>
