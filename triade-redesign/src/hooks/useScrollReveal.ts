import { useEffect, useRef } from 'react'

export function useScrollReveal(threshold = 0.1, rootMargin = '0px 0px -50px 0px') {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed')
            observer.unobserve(entry.target)
          }
        })
      },
      { threshold, rootMargin }
    )

    const children = el.querySelectorAll('.scroll-reveal')
    children.forEach((child) => observer.observe(child))
    if (el.classList.contains('scroll-reveal')) observer.observe(el)

    return () => observer.disconnect()
  }, [threshold, rootMargin])

  return ref
}
