import { type ReactNode, ViewTransition } from 'react';

// Every page wraps its content the same way, so a forward link slides it
// left and a back link slides it right. Browser back has no type: no slide.
export default function Page({ children }: { children: ReactNode }) {
  return (
    <ViewTransition
      enter={{ 'nav-forward': 'nav-forward', 'nav-back': 'nav-back', default: 'none' }}
      exit={{ 'nav-forward': 'nav-forward', 'nav-back': 'nav-back', default: 'none' }}
      default="none"
    >
      <main className="pb-24">{children}</main>
    </ViewTransition>
  );
}
