# Kami Reading Style

Use this style for long prose that should be read, skimmed, printed, and
returned to: essays, DOCX memos, long articles, policy drafts, letters,
research notes, and plain-text manuscripts.

Underlying System: Kami Longform Reader

Reference inspiration: tw93/Kami's `demo-kaku.html` document template and
design constraints. Treat Kami as a restrained document system, not an app UI.
The page should feel like warm printed pages adapted to the browser.

## First Viewport Contract

The first viewport must immediately read as a quiet document:

1. A warm parchment canvas, never pure white.
2. A serif-led cover with a small top label, large title, short lede, one ink
   line, and compact metadata.
3. A slim inline contents strip below the cover.
4. Chapter sections that feel like printable pages: eyebrow, title, lead, body.
5. No sticky side rail, dashboard cards, app top bar, marketing hero, or big
   chrome around the text.

## Visual System

Use these tokens or very close equivalents:

```css
--parchment: #f5f4ed;
--ivory: #faf9f5;
--sand: #e8e6dc;
--border: #e8e6dc;
--border-soft: #e5e3d8;
--brand: #1B365D;
--brand-tint: #EEF2F7;
--brand-tint-strong: #E4ECF5;
--near-black: #141413;
--dark-warm: #3d3d3a;
--olive: #504e49;
--stone: #6b6a64;
```

Rules:

- Page background is parchment `#f5f4ed`; article surfaces are ivory
  `#faf9f5`.
- Ink blue `#1B365D` is the only chromatic accent and should stay below about
  five percent of the visible surface.
- Use warm grays only. Avoid neutral or blue-tinted grays.
- Use almost no shadows. If a lifted box is necessary, use a whisper shadow or
  hairline border only.
- Tags and highlights use solid hex fills, never rgba.
- No italic anywhere. Do not use `font-style: italic`, slanted captions, or
  italic quote styling.

## Typography

- English: serif for headings and body. Good stack:
  `Charter, Georgia, Palatino, "Times New Roman", serif`.
- CJK fallback for multilingual content:
  `"Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", "STSong"`.
- UI labels, overlines, and tiny controls may use a quiet sans stack, but the
  article itself is serif.
- Serif body: weight 400. Serif headings: weight 500. Do not synthesize heavy
  bold.
- Body reading line-height: 1.5 to 1.55. Dense notes: 1.4 to 1.45. Headlines:
  1.1 to 1.3.
- Article column width should stay around 62-72 characters.

## Layout System

Build from these primitives:

- `.kami-reader`: root parchment shell with `data-ha-style="kami-reading"`.
- `.kami-cover`: cover label, title, lede, ink line, metadata.
- `.kami-toc`: slim inline section index.
- `.kami-page`: chapter-level printable reading section.
- `.kami-card`: small ivory callout, metric, table wrapper, or note.
- `.kami-tag`: solid ink-tint inline tag or code label.
- `.kami-progress`: reading progress indicator.
- `.kami-source-drawer`: collapsible source/evidence appendix.

The article should be the entire visual center. A page can use small ivory
cards for metrics, notes, or tables, but these are secondary document elements,
not dashboard panels. On mobile, stack metadata and grids; text must remain
comfortable without horizontal scroll.

## Interaction Model

Include only interactions that help reading:

- Scroll progress linked to `.kami-progress`.
- Clickable inline table of contents.
- Collapsible appendix for source text, extracted metadata, or evidence.
- Optional search or font controls only if they stay visually tiny and do not
  create an app shell.

Do not make charts the primary interaction unless the source truly requires
them. Long prose should privilege reading, navigation, annotation, and source
inspection.

## Content Treatment

- Preserve the author's hierarchy and sequence.
- Convert long paragraphs into comfortable reading blocks; do not over-summarize
  away the original text.
- Pull out a small number of key claims as margin notes or quiet callouts.
- Keep caveats and source metadata visible.
- For memos, expose decisions, risks, open questions, owners, and dates as
  document-native notes, lists, or compact tables rather than KPI tiles.

## Avoid

- Generic document review shells.
- Dashboard-first pages.
- Marketing hero sections.
- Sticky sidebars and heavy reading toolbars.
- Multi-color palettes.
- Cool gray backgrounds.
- Pure white canvases.
- Italic quotes.
- Heavy bold serif.
- Floating card piles.
- Claiming conclusions that are not supported by the source.

## Final Style Gate

Before finalizing, verify the page would still look like a Kami document if all
content were replaced by another essay: parchment, serif, ink-blue restraint,
cover, printable chapter sections, tiny document controls, and no generic
app/dashboard grammar.
