# Boarding-pass deck — slide author spec

Audience: the presenter's design team (designers). Craft matters: strong grid, generous type, consistent spacing, nothing tiny, nothing empty. Airline-ticket / boarding-pass aesthetic throughout (fields with mono labels, perforations, codes, stamps, departure-board, IATA codes, fare-rule style lists). Chinese content.

## Files
- `build/template.html` — shared shell (CSS design system + JS). READ IT FULLY first. DO NOT EDIT IT.
- `git show c45d557:index.html (旧版内容来源)` — previous version; the source of all slide CONTENT (text, image paths, captions). Keep every fact/sentence's meaning; you may tighten wording slightly, never invent new facts/numbers.
- Write your slides as `build/parts/sNN.html` (NN = 2-digit slide number), one `<section>` per file.
- Write your extra CSS in ONE file `build/parts/<yourprefix>.css`. Prefix every class you add with your prefix (e.g. `.a-board`). Don't override shared classes globally.
- Don't touch other agents' files.

## Slide markup
```html
<section class="slide" data-seg="aln" data-title="短标题（显示在票根）">
  <div class="pass-body"> ...your content... </div>
</section>
```
JS wraps it in the ticket: header strip (brand + Flight/Segment/Class/Gate) and the right coupon (route, big gate number, title, seat map, barcode). You only design the `.pass-body`.
- `data-seg`: brd (slides 1–2), aln (3–7), upg (8–16, accent becomes ember), lng (17–22), arr (23).
- Optional `data-alliance="ow|st|sa"` is unused by the shell; color via `var(--ow)/--st/--sa` yourself.

## Canvas
Fixed 1920×1080 scaled by JS; use px freely. `.pass-body` content box ≈ **1356 × 772 px** (flex column, padding already applied). Fill it — use `.grow` / flex:1 for the main block so slides don't look empty, but never overflow (it's clipped).
Min font sizes: body ≥ 24px, captions/labels ≥ 14px (mono labels can be 13–15px).

## Shared pieces available (see template)
`.eyebrow` (mono kicker with accent bar; `<b>` for accent), `h1` 104px, `h2` 64px, `h3` 34px, `.lead` 28px, `.tiny`, `.rules` (numbered fare-rule list, 30px), `.tag .tag-tip/.tag-exp/.tag-core`, `.stamp`, `.fig` + `.cap` (caption chip; `<span class="code">CX</span>` inside for IATA code), `.fig.fig-video`, `.fig.fig-contain`, `data-gallery="name"` on `.fig` for lightbox groups, `.hf-k/.hf-v` (ticket field label/value), `.num` (Barlow digits), `.mono`.
Tokens: --paper --paper-2 --panel --ink --ink-soft --muted --line --line-strong --navy --navy-2 --on-navy --on-navy-muted --champagne --ember --accent --accent-soft --ow --st --sa --ok, fonts --font --display --mono. Use tokens only (dark theme must work; `[data-theme="dark"]` overrides exist).
`.fig` images: add `loading="lazy"` is NOT needed. Keep alt text.

## Broken photos
These files are pure black (HEIC decode failed): nz-lounge/nz-1..4.jpg. Keep the `<img>` but add `data-pending` on their `.fig` (styled placeholder "原图待补" is built in).
Hong Kong videos are portrait 2160×3840 (9:16). Beijing/Taipei photos are only 512×512.

## Verify
```
cd build && python3 build.py /tmp/<you>.html && node shot.js /tmp/<you>.html <scratch dir> light && node shot.js /tmp/<you>.html <scratch dir> dark
```
Note: the built file only contains whatever parts exist so far, so slide numbers in the hash may shift; screenshot all and look at yours (Read the PNGs). Check light AND dark, check no overflow/clipping, iterate until it looks like a polished designer deck. Don't build to ../index.html. Don't commit. Report briefly what you made.
