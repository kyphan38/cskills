'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

// Esc on a skill page goes back to the list (same as the "skills" word).
export default function EscapeBack() {
  const router = useRouter();
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== 'Escape' || e.defaultPrevented) return;
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA')) return;
      router.push('/', { transitionTypes: ['nav-back'] });
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [router]);
  return null;
}
