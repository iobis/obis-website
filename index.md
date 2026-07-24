---
layout: default
---

<section class="section-highlight pt-6 pb-5">
  <div class="container">
  {% include search_form.html centered=true %}
  </div>
</section>

<section class="section-highlight pt-0">
  <div class="container">
    <h2>Featured news and stories</h2>
    {% assign filtered_posts = site.posts | sort: 'date' | reverse %}
    {% include post_cards.html filtered_posts=filtered_posts limit=6 %}
    <p style="text-align: center; margin-top: 2.5rem; font-size: 1.53rem;"><a href="/news" class="usecase-read-more"><strong>Read more news ›</strong></a></p>
  </div>
</section>

<section class="section-light">
  <div class="container">
    <h2>Recent datasets</h2>
    <div id="datasets" class="row row-cols-1 row-cols-md-3 g-4"></div>
  </div>
</section>

<section class="section-highlight">
  <div class="container">

    <div class="row align-items-center">
      
      <div class="col-md-4 mb-4 mb-md-0">
        <h2>OBIS in numbers</h2>
      </div>

      <div class="col-md-8">
        <div class="row">
          
          <div class="col-6 col-md-4 mb-4">
            <div class="display-5 fw-bold">{{ site.data.statistics.presence | divided_by: 1000000 }}M</div>
            <div>species observations</div>
          </div>

          <div class="col-6 col-md-4 mb-4">
            <div class="display-5 fw-bold">{{ site.data.statistics.species | divided_by: 1000 }}K</div>
            <div>marine species</div>
          </div>

          <div class="col-6 col-md-4 mb-4">
            <div class="display-5 fw-bold">{{ site.data.statistics.datasets | number_with_delimiter }}</div>
            <div>datasets</div>
          </div>

          <div class="col-6 col-md-4 mb-4">
            <div class="display-5 fw-bold">{{ site.data.obis_subgroups['386'].size }}</div>
            <div>nodes worldwide</div>
          </div>

          <div class="col-6 col-md-4 mb-4">
            <div class="display-5 fw-bold">{{ site.data.statistics.dna | divided_by: 1000000 }}M</div>
            <div>DNA sequences</div>
          </div>

          <div class="col-6 col-md-4 mb-4">
            <div class="display-5 fw-bold">{{ site.data.statistics.mof | divided_by: 1000000 }}M</div>
            <div>measurements and facts</div>
          </div>

          <div class="col-6 col-md-4 mb-4">
            <div class="display-5 fw-bold">6K</div>
            <div>scientists &amp; data managers</div>
          </div>

          <div class="col-6 col-md-4 mb-4">
            <div class="display-5 fw-bold">99</div>
            <div>countries engaged</div>
          </div>

        </div>
      </div>

    </div>

  </div>
</section>

<section class="section-light">
  <div class="container">
    <h2>Use cases</h2>
    {% assign filtered_usecases = site.usecases | sort: 'date' | reverse %}
    {% include usecase_cards.html filtered_usecases=filtered_usecases limit=6 %}
    <p><a href="/usecases">Read more use cases here</a></p>

  </div>
</section>

<script>
function performSearch() {
  const entityEl = document.getElementById("entity");
  const queryEl = document.getElementById("query");
  if (!entityEl || !queryEl) return;
  const entity = entityEl.value;
  const query = queryEl.value.trim();
  if (!query) return;
  const params = new URLSearchParams();
  if (entity) params.set("entity", entity);
  params.set("q", query);
  window.location.href = "/search?" + params.toString();
}

function stripHtmlTags(html) {
   let doc = new DOMParser().parseFromString(html, "text/html");
   return doc.body.textContent || "";
}

function truncateText(text, maxLength) {
  let ellipsis = "...";
  if (text.length <= maxLength) return text;
  const truncated = text.slice(0, maxLength + 1);
  const lastSpaceIndex = truncated.lastIndexOf(" ");
  if (lastSpaceIndex === -1) return text.slice(0, maxLength) + ellipsis;
  return text.slice(0, lastSpaceIndex) + ellipsis;
}

function formatDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

async function loadRecentDatasets() {
  try {
    const response = await fetch("https://api.obis.org/dataset/published?size=6");
    const data = await response.json();

    const container = document.getElementById("datasets");
    container.innerHTML = "";

    data.results.forEach(dataset => {
      const card = document.createElement("div");
      card.className = "col";

      const nodeBadges = dataset.nodes && dataset.nodes.length > 0
        ? dataset.nodes.map(node => 
            `<a href="/node/${node.id}"><span class="badge tag">${node.name}</span></a>`
          ).join(' ')
        : '';

      card.innerHTML = `
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">
            <a href="/dataset/${dataset.id}">${dataset.title}</a>
          </h5>
          <p class="card-text">${formatDate(dataset.published)}</p>
          ${nodeBadges ? `<p>${nodeBadges}</p>` : ''}
          <p class="card-text">${truncateText(stripHtmlTags(dataset.abstract), 500)}</p>
        </div>
      </div>
      `;

      container.appendChild(card);
    });
  } catch (error) {
    console.error("Error loading datasets:", error);
  }
}

window.addEventListener("DOMContentLoaded", loadRecentDatasets);
</script>