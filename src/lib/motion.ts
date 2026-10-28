export function reducedMotion(): boolean {
  return typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export const EASE_SOFT = 'cubic-bezier(0.22, 1, 0.36, 1)';
