// Progressive-enhancement infinite scroll for /news.
// Jekyll still renders real, independently crawlable pages (/news, /news/page/2/, ...)
// via jekyll-paginate-v2; this script fetches and appends them as the user scrolls,
// so SEO crawling and indexing are unaffected while browsers get a seamless feed.
// Without JS (or if a fetch fails), the Previous/Next links in #news-pagination-nav
// remain fully functional as normal navigation.
(function () {
  const postsContainer = document.getElementById("news-posts");
  const nav = document.getElementById("news-pagination-nav");
  let nextLink = document.getElementById("news-next-page-link");

  if (!postsContainer || !nav || !nextLink || !("IntersectionObserver" in window)) {
    return;
  }

  let loading = false;

  function getRow(container) {
    return container.querySelector(".row");
  }

  async function loadNextPage() {
    if (loading || !nextLink) return;
    loading = true;

    const nextUrl = nextLink.getAttribute("href");

    try {
      const response = await fetch(nextUrl);
      if (!response.ok) throw new Error(`HTTP error ${response.status}`);
      const html = await response.text();
      const doc = new DOMParser().parseFromString(html, "text/html");

      const fetchedRow = getRow(doc.getElementById("news-posts"));
      const currentRow = getRow(postsContainer);
      if (fetchedRow && currentRow) {
        Array.from(fetchedRow.children).forEach((card) => currentRow.appendChild(card));
      }

      history.replaceState(null, "", nextUrl);

      const fetchedNextLink = doc.getElementById("news-next-page-link");
      if (fetchedNextLink) {
        nextLink.setAttribute("href", fetchedNextLink.getAttribute("href"));
      } else {
        observer.unobserve(nav);
        nextLink = null;
      }
    } catch (err) {
      console.error("Error loading more news:", err);
      // Leave the nav visible so the user can retry via the normal Next link.
    } finally {
      loading = false;
    }
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) loadNextPage();
      });
    },
    { rootMargin: "600px" }
  );

  // The nav stays in the DOM as the scroll trigger (visibility:hidden, not display:none,
  // so it still reports intersections) and as a visible fallback if JS never activates.
  nav.style.visibility = "hidden";
  observer.observe(nav);
})();
