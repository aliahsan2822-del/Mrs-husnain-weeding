# Wedding Invitation · M Husnain weds Bint-e-Nazir

A luxury, cinematic, 3D interactive wedding invitation. It is a **single static page** (`index.html`) – no build step,
no framework, no backend. Open the file in a browser, or put the folder on any static host.

**Flow:** closed emerald book on an ivory backdrop ("You're Invited") → tap → the cover swings open in 3D and the open book stays on screen
(Bismillah & verse, names) → scroll through: Home · announcement · date · **Join Us For** (events) · venue · countdown · our story · moments · closing.

---

## Repo structure

```
wedding-invitation/
├── index.html                 ← the whole invitation (HTML + CSS + JS + embedded images & fonts)
├── favicon.svg
├── robots.txt                 ← blocks search engines (private invitation)
├── assets/
│   ├── images/                ← source pictures (couple, card, g1–g5) – for reference / editing
│   └── fonts/                 ← the two Arabic calligraphy font subsets used (OFL)
├── vendor/                    ← local copies of GSAP, ScrollTrigger, Lenis (optional self-hosting)
├── tools/embed_images.py      ← re-embeds assets/images/* into index.html
├── vercel.json                ← Vercel config + headers
├── netlify.toml               ← Netlify config + headers
├── .github/workflows/deploy-pages.yml   ← GitHub Pages auto-deploy
├── package.json               ← convenience scripts (no dependencies)
├── CHANGELOG.md
├── THIRD_PARTY_NOTICES.md
└── README.md
```

## Run locally

```bash
python3 -m http.server 8080      # then open http://localhost:8080
# or
npm start                        # uses `npx serve`
```
(Opening `index.html` by double-click also works.)

---

## Customise (everything is in the `CONFIG` object near the top of the `<script>` in `index.html`)

| What | Where |
|---|---|
| Names | `bride`, `groom` (the invitation always shows the **groom first**) |
| Main date & time (big date section, countdown) | `date: '2026-12-11T07:00:00'` (local time, ISO format) |
| Venue + "View Location" map button | `venue.{name,line1,line2,mapQuery,mapUrl}` |
| **Join Us For** cards | `events: [ { name, date, time, place } ]` – currently only **Mehndi**. Add or remove freely: the cards re-fit the area automatically (1 card = one generous centred card, 2 cards = two equal cards side by side on tablets/desktop and stacked & centred on phones, 3+ cards = a staggered grid). Optional flags: `main: true` (gold "The Ceremony" tag), `dark: true` (emerald card). |
| Our story timeline | `story` |
| "Moments" captions & photos | `gallery` |
| Background music | `music.src` (path to an mp3). Empty = built-in soft music (pre-rendered into a seamless loop) |

Other text lives directly in the HTML: the blessings on the cover (search `bless`), the cover wishes,
the Bismillah/verse page (`bk-bism`, `bk-ayat`) and the closing line.

### Replace the pictures
The pictures are embedded in `index.html` (so it stays one file). To change them:

1. Drop new files into `assets/images/` using the **same names** (`couple`, `card`, `g1`…`g5`; webp/png/jpg).
   `couple` and `card` should be transparent PNG/WebP cut-outs, portrait; keep each file under ~250 KB (about 900 px wide).
2. Run `python3 tools/embed_images.py` (or `npm run embed-images`).
3. If a gallery photo has a different shape, update its `ar` (width ÷ height) in `CONFIG.gallery`.

Prefer normal files instead of embedding? Set e.g. `src: 'assets/images/g1.webp'` in `CONFIG.gallery`
and `heroImage: 'assets/images/couple.webp'` – then you can host the images separately.

---

## Deploy (pick one – all free)

**Netlify** – drag the whole folder onto <https://app.netlify.com/drop>, or *Add new site → Import from Git*
(no build command, publish directory `.`; `netlify.toml` is already set up).

**Vercel** – `npx vercel` in this folder, or import the Git repo (Framework preset: *Other*, no build command).

**GitHub Pages** – push to GitHub, then *Settings → Pages → Source: GitHub Actions*.
The included workflow publishes on every push to `main` at `https://<user>.github.io/<repo>/`.

**Cloudflare Pages** – connect the repo; build command empty; output directory `/`.

```bash
git init && git add . && git commit -m "Wedding invitation"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

**Custom domain:** add it in your host's dashboard (Netlify/Vercel/Cloudflare → Domains) and follow the DNS steps.

### Sharing tips
* Share the link on WhatsApp. For a **preview picture**, add after deploying (absolute URL required):
  `<meta property="og:image" content="https://YOUR-DOMAIN/assets/images/couple.webp">` in the `<head>`.
* A QR code of the link works nicely on printed cards (any free QR generator).
* The page asks search engines not to index it (`robots.txt`, `noindex` meta, and headers). Remove those if you want it public.

### Offline / self-hosting the libraries
By default the page loads GSAP, ScrollTrigger and Lenis from public CDNs and the Latin fonts from Google Fonts.
The Arabic calligraphy fonts, images and music engine are already embedded. To remove the CDN dependency, change the three
`<script src=…>` tags near the end of `index.html` to:

```html
<script src="vendor/gsap.min.js"></script>
<script src="vendor/ScrollTrigger.min.js"></script>
<script src="vendor/lenis.min.js"></script>
```
If a library fails to load, the invitation still opens and reads correctly, just with fewer scroll animations.

---

## Mobile & performance notes

* **Music is glitch-free.** The built-in score is rendered once in the background (a few seconds after the page loads, off the main thread)
  into a seamless 64-second loop and then simply played back as a looping buffer. Scrolling or heavy animation cannot make it stutter.
  Want your own track? Set `music.src` to an mp3 (about 128 kbps, 1–3 MB works best on phones).
* **The open book stays on screen** so the Bismillah page can be read. On phones the camera moves onto the left page, then the right page.
  A tap (or Enter) continues at any time; otherwise it continues by itself.
* **Phones & tablets get a lighter experience:** native scrolling, one-shot reveals instead of scrubbed 3D, fewer ongoing animations,
  and every block is centred in a single column (the Join Us For cards are centred).

### Troubleshooting
* **No music on a phone:** check the silent switch (iPhone) and the media volume; the music starts when the book is tapped.
* **Music starts a moment late:** the loop is rendered right after the page loads; on very slow phones it can take a few seconds. It fades in when ready.
* **After editing and deploying you still see the old page:** hard-refresh (or clear the site data).

## Browser support
Current Chrome, Edge, Safari (iOS 16+) and Firefox. It respects *reduced motion* settings.

## Credits & licences
See `THIRD_PARTY_NOTICES.md`. The couple illustrations and photos are the couple's own personal artwork – do not reuse them without permission.
