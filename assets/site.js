// anuj sangwan — mockup. one small script, no dependencies.

const SITE = {
  timezone: "Asia/Kolkata", // [placeholder] anuj's actual timezone
};

// newest first. add a post: make blog/<slug>/index.html and add a line here.
const POSTS = [
  { slug: "every-bench-in-my-neighborhood-ranked", date: "2026-11-09", title: "every bench in my neighborhood, ranked", excerpt: "eleven benches, four criteria, one clear winner and one bench that should be arrested." },
  { slug: "the-2am-grocery-store", date: "2026-10-31", title: "the 2am grocery store is the last third place", excerpt: "nobody is performing anything at 2am. you're just a guy holding oat milk." },
  { slug: "a-week-without-knowing-the-time", date: "2026-09-12", title: "i tried to go a week without knowing what time it was", excerpt: "covered every clock i own. lasted six days. learned that i eat when i'm bored, not when i'm hungry." },
  { slug: "a-pigeon-lives-on-my-balcony", date: "2026-08-03", title: "notes on the pigeon that lives on my balcony", excerpt: "his name is kevin. he did not choose it and does not answer to it." },
  { slug: "first-post-i-guess", date: "2026-06-01", title: "first post, i guess", excerpt: "a website in 2026, like it's 2006. here's why." },
];

// site root, worked out from where this script lives, so links work at "/" or "/repo/".
const ROOT = new URL("../", document.currentScript.src).href;

const DAY = 86400000;
const today = new Date(new Date().toDateString());
const parse = (d) => new Date(d + "T00:00:00");
const daysBetween = (a, b) => Math.round((a - b) / DAY);

function ago(days) {
  if (days <= 0) return "today";
  if (days === 1) return "yesterday";
  if (days < 14) return `${days} days ago`;
  if (days < 60) return `${Math.round(days / 7)} weeks ago`;
  if (days < 365) return `${Math.round(days / 30)} months ago`;
  const y = Math.round(days / 365);
  return y === 1 ? "a year ago" : `${y} years ago`;
}

function fmt(d) {
  return parse(d).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "2-digit" }).toLowerCase();
}

function gapWords(days) {
  if (days < 14) return null;
  const pick = [
    "of nothing",
    "of silence",
    "of living, presumably",
    "offline",
    "of drafts that didn't make it",
  ];
  return `${days} days ${pick[days % pick.length]}`;
}

// --- the timeline: vertical distance between posts = days between them ---
function renderTimeline(el) {
  const PX_PER_DAY = 3.2;
  const MIN = 22, MAX = 240;
  const space = (days) => Math.max(MIN, Math.min(MAX, days * PX_PER_DAY));

  const rows = [];
  rows.push(`<li class="now-row"><span class="mono now-mark">today</span></li>`);

  let prev = today;
  POSTS.forEach((p) => {
    const d = parse(p.date);
    const gap = daysBetween(prev, d);
    const words = prev === today ? (gap >= 1 ? `${gap} days since the last one` : null) : gapWords(gap);
    rows.push(`<li class="gap" style="height:${space(gap)}px" aria-hidden="true">${words ?? ""}</li>`);
    rows.push(`
      <li class="post">
        <time datetime="${p.date}" title="${ago(daysBetween(today, d))}">${fmt(p.date)}</time>
        <a href="${ROOT}blog/${p.slug}/">
          <span class="t">${p.title}</span>
          <span class="x"><span>${p.excerpt}</span></span>
        </a>
      </li>`);
    prev = d;
  });

  el.innerHTML = rows.join("");
  const first = POSTS[POSTS.length - 1];
  const end = document.querySelector(".timeline-end");
  if (end) end.textContent = `that's everything. started ${ago(daysBetween(today, parse(first.date)))}.`;
}

// --- post pages: relative date + earlier/later ---
function renderPost(el) {
  const slug = el.dataset.post;
  const i = POSTS.findIndex((p) => p.slug === slug);
  if (i < 0) return;
  const p = POSTS[i];
  const words = el.querySelector(".prose")?.innerText.split(/\s+/).length ?? 0;
  const meta = el.querySelector(".lede .meta");
  if (meta) {
    meta.innerHTML = `<time datetime="${p.date}">${fmt(p.date)}</time><br>${ago(daysBetween(today, parse(p.date)))}<br>${Math.max(1, Math.round(words / 230))} min read`;
  }
  const later = POSTS[i - 1], earlier = POSTS[i + 1];
  const adj = document.createElement("nav");
  adj.className = "adjacent";
  adj.innerHTML =
    (earlier ? `<a href="${ROOT}blog/${earlier.slug}/"><span class="mono">← earlier</span>${earlier.title}</a>` : "") +
    (later ? `<a href="${ROOT}blog/${later.slug}/"><span class="mono">later →</span>${later.title}</a>` : `<a href="${ROOT}"><span class="mono">later →</span>nothing yet. check back.</a>`);
  el.appendChild(adj);
}

// --- /now: entries fade as they age ---
function renderNow(el) {
  const items = [...el.querySelectorAll(":scope > li")];
  items.forEach((li) => {
    const t = li.querySelector("time");
    const days = daysBetween(today, parse(t.getAttribute("datetime")));
    li.style.opacity = Math.max(0.18, 1 - days / 110).toFixed(2);
    t.innerHTML = `${fmt(t.getAttribute("datetime"))}<br>${ago(days)}`;
  });
  const latest = items[0]?.querySelector("time").getAttribute("datetime");
  const u = document.querySelector("[data-updated]");
  if (u && latest) u.textContent = ago(daysBetween(today, parse(latest)));
}

// --- his local time, top right ---
function clock(el) {
  const tick = () => {
    const t = new Date().toLocaleTimeString("en-GB", { timeZone: SITE.timezone, hour: "2-digit", minute: "2-digit" });
    const h = +t.slice(0, 2);
    const mood = h < 5 ? "probably still up" : h < 9 ? "probably asleep" : h < 18 ? "probably around" : h < 23 ? "probably online" : "probably should sleep";
    el.textContent = `${t} for anuj — ${mood}`;
  };
  tick();
  setInterval(tick, 30000);
}

document.querySelectorAll("[data-timeline]").forEach(renderTimeline);
document.querySelectorAll("[data-post]").forEach(renderPost);
document.querySelectorAll("[data-now]").forEach(renderNow);
document.querySelectorAll("[data-clock]").forEach(clock);
