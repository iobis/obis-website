// Accepts an element, an element id or a CSS selector.
export function resolveTarget(target) {
    if (typeof target !== "string") return target;
    return document.querySelector(target.startsWith("#") || /[.\[\s>]/.test(target) ? target : `#${target}`);
}
