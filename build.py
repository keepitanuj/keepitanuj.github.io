# generates every page. run: python3 build.py .
import pathlib, sys
root = pathlib.Path(sys.argv[1])

def page(path, title, body, current=None, desc="anuj sangwan writes about random things."):
    # every link is relative, so the site works at a domain root (user.github.io, custom domain)
    # and under a sub-path (user.github.io/repo/) alike.
    up = "../" * path.count("/")
    home = up or "./"
    body = body.replace('href="/', f'href="{up}')
    nav = ""
    for href, label in [(f"{up}blog/", "writing"), (f"{up}about/", "about"), (f"{up}now/", "now")]:
        cur = ' aria-current="page"' if current == label else ""
        nav += f'<a href="{href}"{cur}>{label}</a>'
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..600&display=swap">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<header class="bar">
  <a class="home" href="{home}">anuj sangwan</a>
  <nav>{nav}</nav>
  <span class="clock" data-clock></span>
</header>
<main>
{body.strip()}
</main>
<footer class="foot">no cookies, no tracking, no newsletter popup. made by hand, slowly.</footer>
<script src="{up}assets/site.js"></script>
</body>
</html>
'''
    f = root / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html)

# ---------- home ----------
page("index.html", "anuj sangwan", '''
<p class="intro">hi, i'm anuj. i write about <em>whatever i can't stop thinking about</em> — benches, pigeons, grocery stores at 2am — roughly in the order it happens.</p>

<ul class="elsewhere">
  <li>elsewhere</li>
  <li><a href="#">instagram <span>@<span class="ph">handle</span> ↗</span></a></li>
  <li><a href="#">letterboxd <span>@<span class="ph">handle</span> ↗</span></a></li>
  <li><a href="#">spotify <span><span class="ph">profile</span> ↗</span></a></li>
  <li><a href="#">x <span>@<span class="ph">handle</span> ↗</span></a></li>
  <li><a href="#">email <span><span class="ph">hi@…</span></span></a></li>
</ul>

<ol class="timeline" data-timeline></ol>
<p class="timeline-end"></p>
''')

# ---------- writing index ----------
page("blog/index.html", "writing — anuj sangwan", '''
<div class="page">
  <h1>writing</h1>
  <p class="mono" style="margin:-1.8rem 0 6rem">no categories. no tags. just the order it happened in, spaced out by how long it took.</p>
</div>
<ol class="timeline" data-timeline></ol>
<p class="timeline-end"></p>
''', current="writing")

# ---------- about ----------
page("about/index.html", "about — anuj sangwan", '''
<article class="page">
  <div class="lede"><span class="meta">about<br>written once,<br>edited often</span>
  <h1>i'm anuj. i notice things and then can't let them go.</h1></div>
  <div class="prose">
    <p>right now i'm <span class="ph">a student / working as something</span> in <span class="ph">city</span>. most of my day is spent on <span class="ph">the main thing</span>, and most of my evenings are spent on everything else.</p>
    <p>this site is where the everything else goes. it isn't a portfolio and it isn't a brand. it's closer to a notebook that i'm okay with you reading: rankings nobody asked for, small experiments on myself, thoughts that are too long for a caption and too dumb for an essay.</p>

    <h2><span class="n">01</span>things i'm into</h2>
    <p><span class="ph">a few honest interests, e.g. films, a sport, a specific kind of music, cooking one dish very well</span>.</p>

    <h2><span class="n">02</span>things i'm bad at</h2>
    <p>replying to texts on time. leaving parties. knowing when a post is finished.</p>

    <h2><span class="n">03</span>how this site works</h2>
    <p>everything on the front page is laid out by time. the space between two posts is the time between them. long gaps stay long. i'd rather you see that i disappeared for two months than pretend i didn't.</p>
    <p>the <a href="/now/">now page</a> works the same way: older updates fade until they're barely there.</p>

    <h2><span class="n">04</span>say hi</h2>
    <p>email is best: <span class="ph">hi@…</span>. i read everything. i reply to most of it, eventually.</p>
  </div>
</article>
''', current="about")

# ---------- now ----------
page("now/index.html", "now — anuj sangwan", '''
<article class="page">
  <div class="lede"><span class="meta">now<br>last updated<br><span data-updated></span></span>
  <h1>what i'm doing, roughly, lately.</h1></div>
  <p class="mono" style="margin:-1.8rem 0 5rem">older entries fade out. that's the point. (hover to read them anyway.)</p>
  <ol class="log" data-now>
    <li>
      <time datetime="2026-11-11"></time>
      <dl>
        <dt>mostly</dt><dd><span class="ph">the main thing this month</span></dd>
        <dt>reading</dt><dd><span class="ph">book title</span>, slowly, on the bus</dd>
        <dt>on repeat</dt><dd><span class="ph">album or artist</span></dd>
        <dt>watching</dt><dd>one film a week, logged on letterboxd so i can't lie about it</dd>
        <dt>trying to</dt><dd>sleep before 1. it's going badly.</dd>
      </dl>
    </li>
    <li>
      <time datetime="2026-09-20"></time>
      <dl>
        <dt>mostly</dt><dd>recovering from the clock experiment</dd>
        <dt>reading</dt><dd><span class="ph">book title</span></dd>
        <dt>trying to</dt><dd>cook something that isn't eggs</dd>
      </dl>
    </li>
    <li>
      <time datetime="2026-07-02"></time>
      <dl>
        <dt>mostly</dt><dd>building this website instead of writing on it</dd>
        <dt>obsessed with</dt><dd>a pigeon. more on that later.</dd>
      </dl>
    </li>
  </ol>
</article>
''', current="now")

# ---------- posts ----------
def post(slug, title, body):
    page(f"blog/{slug}/index.html", f"{title} — anuj sangwan", f'''
<article class="page" data-post="{slug}">
  <div class="lede"><span class="meta"></span>
  <h1>{title}</h1></div>
  <div class="prose">
{body.strip()}
  </div>
</article>
''', current="writing")

post("a-week-without-knowing-the-time", "i tried to go a week without knowing what time it was", '''
<p>i covered every clock i own with tape. phone in grayscale, lock screen clock hidden, laptop menu bar turned off. microwave unplugged, which in hindsight was the real sacrifice.</p>
<p>the rule was simple: for seven days i'm not allowed to know the time. i can know if it's light or dark. i can know if i'm hungry. that's it.</p>

<h2><span class="n">day 1</span>it's fine, actually</h2>
<p>the first day felt like a holiday. i woke up when i woke up. i ate when i was hungry. i felt smug in the specific way you feel smug on the first day of anything.</p>

<h2><span class="n">day 3</span>i eat when i'm bored</h2>
<p>this was the big one. without a clock telling me it was "lunchtime" i expected to eat less. i ate more. it turns out i don't eat when i'm hungry, i eat when i don't know what to do next, and without time to structure the day i never knew what to do next.</p>

<blockquote>time isn't something i keep. it's something that keeps me.</blockquote>

<p>that sounds deep. i wrote it at what i later found out was 4:12am.</p>

<figure>
  <div class="img">[ photo: taped-up oven clock ]</div>
  <figcaption>fig. 1 — the oven. the tape held. i did not.</figcaption>
</figure>

<h2><span class="n">day 6</span>i broke</h2>
<p>someone asked me to meet "at 6" and i realised i had no way to do that without cheating. so i cheated. it was 5:51. i had been, by pure vibes, almost exactly right.</p>

<h2><span class="n">notes</span>what i'd tell you if you tried it</h2>
<ul>
  <li>tell people first. they get weird about it otherwise.</li>
  <li>you will look at your wrist even if you've never worn a watch.</li>
  <li>sunsets get very important, very fast.</li>
  <li>don't unplug the microwave.<sup><a href="#n1">1</a></sup></li>
</ul>

<div class="notes">
  <p id="n1">1. you can't heat things in it, obviously, but mostly the beep was the only thing in the flat that sounded like it knew what it was doing.</p>
</div>
''')

post("every-bench-in-my-neighborhood-ranked", "every bench in my neighborhood, ranked", '''
<p>eleven benches. four criteria: comfort, view, shade, and what i'm calling "vibe integrity," which is whether the bench feels like it wants you there.</p>
<h2><span class="n">11</span>the one outside the bank</h2>
<p>metal. armrests every forty centimetres so you can't lie down. a bench that has been designed by someone who hates benches. it should be arrested.</p>
<h2><span class="n">06</span>the bus stop one</h2>
<p>it's fine. it's a bench. it knows what it is and it doesn't pretend to be anything else, which honestly is more than i can say for most people.</p>
<h2><span class="n">01</span>the one by the old tree</h2>
<p>wooden, slightly warped, one plank missing. full shade until 3pm. a man feeds birds there every thursday and has never once acknowledged me, which is exactly the right amount of acknowledgement.</p>
''')

post("the-2am-grocery-store", "the 2am grocery store is the last third place", '''
<p>nobody is performing anything at 2am. you're just a guy holding oat milk under fluorescent light, and so is everyone else.</p>
<p>i've started going on purpose. not for anything in particular. it's the only place i know where strangers are in the same room, doing the same small thing, and nobody needs anything from anybody.</p>
<blockquote>the cashier and i have a nod now. it took four months.</blockquote>
<p>i don't know her name. i don't want to know her name. the nod is perfect and i won't ruin it.</p>
''')

post("a-pigeon-lives-on-my-balcony", "notes on the pigeon that lives on my balcony", '''
<p>his name is kevin. he did not choose it and does not answer to it.</p>
<p>he arrived in june. he sits on the railing from roughly sunrise to roughly whenever, looking at the building across the road like he's waiting for it to apologise.</p>
<ul>
  <li>he does not like bread. he likes the idea of bread.</li>
  <li>he has a friend who visits on weekends. i assume it's his friend. it could be his landlord.</li>
  <li>he has seen me cry once and was very normal about it.</li>
</ul>
''')

post("first-post-i-guess", "first post, i guess", '''
<p>a website in 2026, like it's 2006.</p>
<p>i wanted somewhere that isn't a feed. somewhere nothing gets ranked, nothing autoplays, and a post from two years ago sits exactly where i left it. so i made one.</p>
<p>i'll write about whatever. if that sounds unfocused, that's because it is.</p>
''')
