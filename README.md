# cskills

My Claude Code skills, and the site that lists them: cskills.kyphan38.com

## Use on a new machine

```sh
git clone https://github.com/kyphan38/cskills.git ~/ws/app/cskills
sh ~/ws/app/cskills/scripts/install.sh
```

`~/.claude/skills` then points to `skills/` in this repo. `git pull` updates
every skill.

## Site

```sh
npm install
npm run dev     # http://localhost:3000
npm run build   # static files in out/
```

Vercel: import the repo, framework Next.js, domain `cskills.kyphan38.com`
(DNS: `cskills` CNAME as Vercel says).
