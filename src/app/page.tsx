import Header from '@/components/Header';
import Page from '@/components/Page';
import SkillList from '@/components/SkillList';
import { plain } from '@/lib/md';
import { getSkills } from '@/lib/skills';

export default function Home() {
  const skills = getSkills();
  const items = skills.map((s) => ({
    name: s.name,
    summary: s.summary,
    family: s.family,
    text: [s.name, s.summary, plain(s.description)].join(' ').toLowerCase(),
  }));
  const families = new Set(skills.map((s) => s.family)).size;
  return (
    <>
      <Header />
      <Page>
        <div className="mx-auto max-w-[60rem] pt-16 md:pt-24">
          <h1 className="font-mono text-[28px] leading-tight tracking-tight text-ink md:text-[36px]">~/.claude/skills</h1>
          <p className="mt-3 font-mono text-[13px] text-faint">
            {skills.length} skills · {families} families
          </p>
          <div className="mt-12">
            <SkillList items={items} />
          </div>
        </div>
      </Page>
    </>
  );
}
