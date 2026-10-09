export function pinForLeave(element: Element) {
  const el = element as HTMLElement
  el.style.top = `${el.offsetTop}px`
  el.style.left = `${el.offsetLeft}px`
  el.style.width = `${el.offsetWidth}px`
  el.style.height = `${el.offsetHeight}px`
}
