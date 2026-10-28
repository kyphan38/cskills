import Link from 'next/link';

import { REPO } from '@/lib/skills';

// A path, like a shell prompt: cskills / legi-quotes. Stays still while
// pages slide (its own view-transition name).
export default function Header({ skill }: { skill?: string }) {
  return (
    <header
      style={{ viewTransitionName: 'site-header' }}
      className="flex items-baseline justify-between border-b border-line py-4 font-mono text-[13px]"
    >
      <div className="flex min-w-0 items-baseline gap-2">
        <Link href="/" transitionTypes={['nav-back']} className={skill ? 'text-faint hover:text-ink' : 'text-ink'}>
          cskills
        </Link>
        {skill && (
          <>
            <span aria-hidden className="text-faint">
              /
            </span>
            <span className="truncate text-ink">{skill}</span>
          </>
        )}
      </div>
      <a href={REPO} className="shrink-0 text-faint hover:text-ink">
        github ↗
      </a>
    </header>
  );
}
