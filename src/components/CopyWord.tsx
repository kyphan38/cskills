'use client';

import { useCopy } from '@/components/useCopy';

// "copy" turns into "copied": the two words cross-fade in the same spot,
// so the row does not shift.
export default function CopyWord({ text, className = '' }: { text: string; className?: string }) {
  const { copied, copy } = useCopy();
  return (
    <button
      type="button"
      onClick={() => void copy(text)}
      aria-label={copied ? 'copied' : `copy ${text}`}
      className={`relative inline-grid font-mono text-[12px] text-faint transition-transform duration-150 hover:text-ink active:scale-[0.97] active:text-ink ${className}`}
    >
      <span
        aria-hidden
        className={`col-start-1 row-start-1 transition-[opacity,transform] duration-200 ease-[var(--ease-soft)] ${copied ? '-translate-y-1 opacity-0' : 'opacity-100'}`}
      >
        copy
      </span>
      <span
        aria-hidden
        className={`col-start-1 row-start-1 text-ink transition-[opacity,transform] duration-200 ease-[var(--ease-soft)] ${copied ? 'opacity-100' : 'translate-y-1 opacity-0'}`}
      >
        copied
      </span>
    </button>
  );
}
