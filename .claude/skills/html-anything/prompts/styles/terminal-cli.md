# Terminal CLI Style

Use this style when the user explicitly asks for a terminal, CLI, shell,
mainframe, hacker, server-console, ZSH/BASH, or system-level interface. It is
especially strong for CI logs, server logs, stack traces, repo audits, incident
notes, runbooks, technical timelines, and source material that already feels
like command output.

This style is not cyberpunk decoration. It is a usable terminal work surface.
Do not add Matrix rain, neon-purple gradients, rounded SaaS cards, glassmorphic
panels, or dashboard chrome.

## Underlying System: Terminal CLI

The page feels like a clean `tmux` / `vim` split session on a phosphor
monitor: brutally functional, dark-only, high-contrast, monospace everywhere,
and organized around commands, panes, status codes, and raw evidence.

Base scaffold:

1. **Shell header** — a command prompt line such as
   `operator@html-anything:~/source$ scan --summary --evidence` with a blinking
   cursor and compact run/source metadata.
2. **Status rail** — terminal-native metrics as status codes and ASCII bars,
   e.g. `[ERR] exit=1`, `[OK] lint`, `[||||||....] 62%`.
3. **Pane grid** — strict terminal panes with 1px green borders and title bars:
   `+--- RUN SUMMARY ---+`, `+--- RISK HOTSPOTS ---+`, `+--- RAW LOG ---+`.
4. **Command controls** — prompt-like inputs and bracket buttons:
   `[ COPY SUMMARY ]`, `[ JUMP RAW ]`, `[ FILTER ERR ]`.
5. **Raw drill-down** — searchable, line-numbered, collapsible source evidence
   rendered close to the insights it supports.

## Token Override

Use these tokens in `:root`. This is a dark-mode-only surface. Do not add a
light theme.

```css
:root {
  color-scheme: dark;

  --bg: #0a0a0a;
  --surface: #0a0a0a;
  --surface-container-lowest: #0a0a0a;
  --surface-container-low: #0d160d;
  --surface-container: #102610;
  --surface-container-high: #153315;

  --primary: #33ff00;
  --secondary: #ffb000;
  --muted: #1f521f;
  --accent: #33ff00;
  --error: #ff3333;
  --border: #1f521f;
  --border-strong: #33ff00;

  --fg-1: #33ff00;
  --fg-2: #b7ff9a;
  --fg-muted: #1f521f;
  --on-primary: #050505;

  --green: #33ff00;
  --yellow: #ffb000;
  --red: #ff3333;
  --blue: #72d5ff;

  --font-headline: 'JetBrains Mono', 'Fira Code', 'SF Mono', Menlo, Consolas, monospace;
  --font-body: 'JetBrains Mono', 'Fira Code', 'SF Mono', Menlo, Consolas, monospace;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Menlo, Consolas, monospace;

  --space-xs: 4px; --space-sm: 8px; --space-md: 12px;
  --space-lg: 16px; --space-xl: 20px; --space-2xl: 24px;
  --space-3xl: 32px; --space-4xl: 48px; --space-5xl: 64px;

  --radius-sm: 0; --radius-md: 0; --radius-lg: 0;
  --radius-xl: 0; --radius-2xl: 0; --radius-pill: 0;

  --shadow-sm: none;
  --shadow-md: none;
  --shadow-lg: none;
  --shadow-accent: none;
  --text-glow: 0 0 5px rgba(51, 255, 0, 0.5);
}
```

Use this Google Fonts import if a font import is useful:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

## Visual Rules

- Monospace supremacy: every visible character uses `var(--font-mono)`.
- Headers are uppercase and compact. Prefer `RUN SUMMARY` over poetic titles.
- Radius is always `0`. Borders are always 1px solid or dashed green.
- No drop shadows. Use a subtle green text glow only when it does not harm
  readability.
- Add a low-opacity scanline overlay with `pointer-events: none`.
- Use amber for warnings/accent details and red for true errors.
- Use ASCII separators: `//`, `===`, `---`, `+--- TITLE ---+`.
- Use raw ASCII visualizations instead of glossy charts.

## Component Vocabulary

Required class names and primitives:

- `.terminal-cli-shell`
- `.shell-prompt`
- `.terminal-cursor`
- `.terminal-pane`
- `.pane-title`
- `.status-code`
- `.ascii-bar`
- `.command-button`
- `.prompt-input`
- `.raw-console`
- `.scanline-overlay`

Buttons:

- Bracketed commands: `[ COPY SUMMARY ]`, `[ SHOW ERRORS ]`.
- Hover/focus uses inverted video: green background, black text.
- Active state may shift text by 1px or briefly blink.

Inputs:

- Render as prompts, not boxes:
  `grep@raw:~$ <input>`
- Focus shows inverted video or a crisp green underline.

Panes:

- Black background, 1px green border.
- Title bar is text-native: `+--- RISK HOTSPOTS ---+`.
- Content uses compact line-height and aligned labels.

## Interaction Model

- Raw source is searchable. Search should highlight or filter lines.
- Status codes and pane controls are keyboard accessible.
- Any inferred conclusion is labeled `[HYP]` or "Hypothesis".
- Copy controls put useful Markdown/plain text on the clipboard.
- If the source contains raw lines, clicking a finding should jump to the
  matching line in `.raw-console`.

## Motion

- Use a blinking block or underscore cursor in the shell header.
- A short typewriter reveal is allowed for the initial command/status line.
- Optional hover glitch is limited to a 1px label offset.
- Respect `prefers-reduced-motion`: disable typing, blinking, and glitch.

## Good Fits

- CI/build logs, server logs, stack traces, repo audits, PR review summaries.
- Security/incident notes where source evidence matters.
- Technical teaching pages that should feel like a shell lab.
- Any brief where the user explicitly asks for terminal/CLI/mainframe style.

## Avoid

- Generic `hero + KPI cards + chart cards + table` layouts.
- Rounded product cards, pastel dashboards, or marketing-style hero sections.
- Matrix rain or decorative hacker clichés.
- Smooth gradients, blur, glass, or purple cyberpunk lighting.
- Hiding source evidence behind decorative copy.

## Compliance Gate

Before returning HTML for this style, confirm:

- Root is `<html ... data-ha-style="terminal-cli">`.
- First viewport contains a prompt, status rail, and at least two terminal
  panes.
- The page uses dark-only terminal tokens and monospace everywhere.
- It includes `.scanline-overlay`, `.shell-prompt`, `.terminal-pane`,
  `.status-code`, `.ascii-bar`, and `.raw-console`.
- Interactive controls are bracketed terminal commands with accessible labels.
