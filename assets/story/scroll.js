// Scrollytelling helper: calls `onStep` whenever a step element crosses the middle
// of the viewport (adjustable with `offset`, 0 = top, 1 = bottom).
//
//   scroll(".story-step", (step, index) => {
//       map.flyTo({ center: JSON.parse(step.dataset.center), zoom: +step.dataset.zoom });
//   });
export function scroll(steps, onStep, { offset = 0.5 } = {}) {
    const elements = typeof steps === "string" ? [...document.querySelectorAll(steps)] : [...steps];
    if (!elements.length) return;

    const margin = `${-offset * 100}% 0px ${-(1 - offset) * 100 + 0.1}% 0px`;
    let current = -1;

    const observer = new IntersectionObserver((entries) => {
        for (const entry of entries) {
            if (!entry.isIntersecting) continue;
            const index = elements.indexOf(entry.target);
            if (index === current) continue;
            current = index;
            elements.forEach((el, i) => el.classList.toggle("is-active", i === index));
            onStep(entry.target, index);
        }
    }, { rootMargin: margin, threshold: 0 });

    elements.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
}
