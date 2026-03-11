---
layout: portal
title: "System status"
permalink: /status/
---

<section class="section-dense">
  <div class="container">
    <h1 class="mb-4">System status</h1>

    <div id="status-error" class="alert alert-danger d-none" role="alert"></div>

    <div class="mb-4">
      <h2 class="h4 mb-3">Queued tasks</h2>
      <div id="status-queue">
        <p class="text-muted mb-0">Loading queued tasks…</p>
      </div>
    </div>

    <div class="mb-4">
      <h2 class="h4 mb-3">Recently published datasets</h2>
      <div id="status-datasets">
        <p class="text-muted mb-0">Loading datasets…</p>
      </div>
    </div>

    <div class="mb-4">
      <h2 class="h4 mb-3">Feeds</h2>
      <div id="status-feeds">
        <p class="text-muted mb-0">Loading feeds…</p>
      </div>
    </div>
  </div>
</section>

<script>
document.addEventListener("DOMContentLoaded", function () {
  const apiUrl = "https://api.obis.org/status";

  const errorEl = document.getElementById("status-error");
  const queueEl = document.getElementById("status-queue");
  const feedsEl = document.getElementById("status-feeds");
  const datasetsEl = document.getElementById("status-datasets");

  function showError(message) {
    if (!errorEl) return;
    errorEl.textContent = message;
    errorEl.classList.remove("d-none");
  }

  function initPopovers() {
    if (typeof bootstrap === "undefined" || typeof bootstrap.Popover !== "function") {
      console.error("Bootstrap Popover is not available");
      return;
    }
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    [...popoverTriggerList].forEach((popoverTriggerEl) => {
      new bootstrap.Popover(popoverTriggerEl);
    });
  }

  function escapeText(text) {
    const div = document.createElement("div");
    div.textContent = text == null ? "" : String(text);
    return div.innerHTML;
  }

  function escapeAttr(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function formatDateTime(value) {
    if (!value) return "";
    const str = String(value);
    const match = str.match(/^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})/);
    if (match) {
      const datePart = match[1];
      const timePart = match[2];
      return datePart + " " + timePart;
    }
    return str;
  }

  function renderQueue(queue) {
    if (!queue || queue.length === 0) {
      queueEl.innerHTML = '<p class="text-muted mb-0">No queued tasks.</p>';
      return;
    }

    const rows = queue.map(task => {
      const payload = task.payload || {};
      const datasetId = payload.dataset_id || "";

      let queryBadge = "";
      if (payload.query) {
        const queryText = escapeAttr(JSON.stringify(payload.query));
        queryBadge = `<span class="badge rounded-pill bg-info-subtle text-info-emphasis border border-info-subtle" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-placement="top" data-bs-content="${queryText}">View</span>`;
      }

      return `
        <tr>
          <td>${escapeText(task.id)}</td>
          <td>${escapeText(task.queue)}</td>
          <td>${escapeText(task.priority)}</td>
          <td>${queryBadge}</td>
          <td>${escapeText(datasetId)}</td>
          <td style="white-space: nowrap;">${escapeText(formatDateTime(task.created_at))}</td>
          <td style="white-space: nowrap;">${escapeText(formatDateTime(task.locked_at))}</td>
        </tr>
      `;
    }).join("");

    queueEl.innerHTML = `
      <div class="table-responsive">
        <table class="table table-sm align-middle">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Queue</th>
              <th scope="col">Priority</th>
              <th scope="col">Query</th>
              <th scope="col">Dataset ID</th>
              <th scope="col" style="white-space: nowrap;">Created at</th>
              <th scope="col" style="white-space: nowrap;">Started at</th>
            </tr>
          </thead>
          <tbody>
            ${rows}
          </tbody>
        </table>
      </div>
    `;
    initPopovers();
  }

  function renderFeeds(feeds) {
    const rows = feeds.map(feed => {
      const isDown = !!(feed.error_message || feed.active === false);
      let statusBadge;
      if (isDown) {
        const errorText = feed.error_message ? escapeAttr(feed.error_message) : "No error message available";
        statusBadge = `<span class="badge rounded-pill bg-danger-subtle text-danger-emphasis border border-danger-subtle" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-placement="top" data-bs-content="${errorText}">Down</span>`;
      } else if (feed.active) {
        statusBadge = '<span class="badge rounded-pill bg-success-subtle text-success-emphasis border border-success-subtle">OK</span>';
      } else {
        statusBadge = '<span class="badge rounded-pill bg-secondary-subtle text-secondary-emphasis border border-secondary-subtle">Inactive</span>';
      }

      const urlCell = feed.url
        ? `<a href="${escapeText(feed.url)}" target="_blank" rel="noopener">${escapeText(feed.url)}</a>`
        : '<span class="text-muted">No URL</span>';

      let activeBadge;
      if (feed.active === true) {
        activeBadge = '<span class="badge rounded-pill bg-success-subtle text-success-emphasis border border-success-subtle">Yes</span>';
      } else if (feed.active === false) {
        activeBadge = '<span class="badge rounded-pill bg-danger-subtle text-danger-emphasis border border-danger-subtle">No</span>';
      } else {
        activeBadge = '<span class="badge rounded-pill bg-secondary-subtle text-secondary-emphasis border border-secondary-subtle">Unknown</span>';
      }

      return `
        <tr>
          <td>${statusBadge}</td>
          <td>${activeBadge}</td>
          <td>${escapeText(feed.node_name)}</td>
          <td>${urlCell}</td>
        </tr>
      `;
    }).join("");

    feedsEl.innerHTML = `
      <div class="table-responsive">
        <table class="table table-sm align-middle">
          <thead>
            <tr>
              <th scope="col">Status</th>
              <th scope="col">Active</th>
              <th scope="col">Node</th>
              <th scope="col">URL</th>
            </tr>
          </thead>
          <tbody>
            ${rows}
          </tbody>
        </table>
      </div>
    `;
    initPopovers();
  }

  function renderDatasets(datasets) {
    if (!datasets || datasets.length === 0) {
      datasetsEl.innerHTML = '<p class="mb-0">No recent datasets found.</p>';
      return;
    }

    const sorted = datasets.slice().sort((a, b) => {
      const pa = a.published ? Date.parse(a.published) : 0;
      const pb = b.published ? Date.parse(b.published) : 0;
      return pb - pa;
    }).slice(0, 20);

    const rows = sorted.map(d => {
      const hasTitle = !!d.dataset_title;
      const linkLabel = hasTitle ? d.dataset_title : d.id;
      const titleCell = d.id
        ? `<a href="https://obis.org/dataset/${encodeURIComponent(d.id)}" target="_blank" rel="noopener">${escapeText(linkLabel)}</a>`
        : escapeText(linkLabel);

      const nodes = Array.isArray(d.nodes) ? d.nodes : [];
      const nodesCell = nodes.length
        ? escapeText(nodes.join(", "))
        : '<span></span>';

      return `
        <tr>
          <td style="white-space: nowrap;">${escapeText(formatDateTime(d.published))}</td>
          <td style="white-space: nowrap;">${nodesCell}</td>
          <td>${titleCell}</td>
        </tr>
      `;
    }).join("");

    datasetsEl.innerHTML = `
      <div class="table-responsive">
        <table class="table table-sm align-middle">
          <thead>
            <tr>
              <th scope="col" style="white-space: nowrap;">Published</th>
              <th scope="col" style="white-space: nowrap;">Nodes</th>
              <th scope="col">Title</th>
            </tr>
          </thead>
          <tbody>
            ${rows}
          </tbody>
        </table>
      </div>
    `;
  }

  fetch(apiUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error("Request failed with status " + response.status);
      }
      return response.json();
    })
    .then(data => {
      renderQueue(data.queue || []);
      renderFeeds(data.feeds || []);
      renderDatasets(data.datasets || []);
    })
    .catch(error => {
      console.error("Failed to load status:", error);
      showError("Unable to fetch OBIS status at this time.");
      queueEl.innerHTML = '<p class="mb-0">No data.</p>';
      feedsEl.innerHTML = '<p class="mb-0">No data.</p>';
      datasetsEl.innerHTML = '<p class="mb-0">No data.</p>';
    });
});
</script>

