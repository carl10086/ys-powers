# Mermaid Diagram Support

Complete rules for embedding, validating, and interacting with mermaid diagrams
in generated HTML pages.

## Trigger Conditions

Render mermaid when the source contains any of:

- ` ```mermaid ` code blocks.
- Code files where a flowchart, call graph, or module-dependency diagram aids
  understanding.
- Markdown/text describing processes, state machines, or architecture.

## Syntax Validation Workflow

**Goal**: catch invalid mermaid syntax before generating HTML.

1. **Extract blocks**: scan input for all ` ```mermaid ` code blocks.
2. **Install validator** (if missing):
   ```bash
   npm list mermaid >/dev/null 2>&1 || npm install mermaid
   ```
3. **Validate each block** with a small Node.js script:
   ```bash
   node --input-type=module <<'EOF'
   import mermaid from 'mermaid';
   mermaid.initialize({ startOnLoad: false });
   const code = \`...diagram code...\`;
   try {
     await mermaid.parse(code);
     console.log('OK');
   } catch (e) {
     console.error(e.message);
     process.exit(1);
   }
   EOF
   ```
4. **Handle failure**:
   - If exit code != 0, capture the parse error message.
   - Report to user: which block failed, error position, and reason.
   - **Stop**. Do not generate HTML until user fixes the syntax.
5. **Skip when clean**: if no mermaid blocks exist, skip this step.

## HTML Rendering Rules

- Load `https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js` from CDN.
- Initialize in an inline `<script>` after DOM ready.
- Customize theme with Clockless CSS variables (colors, fonts, border-radius).

### Responsive Container

```css
.mermaid-wrapper {
  overflow-x: auto;
  padding: 1rem;
  position: relative;
}
```

## Zoom Controls

Prevent mermaid from compressing wide diagrams into an unreadable size.

### Disable Auto-Scale

Add to mermaid `%%{init}%%`:

```json
{
  "flowchart": { "useMaxWidth": false },
  "gantt": { "useMaxWidth": false },
  "sequence": { "useMaxWidth": false }
}
```

This lets the SVG render at its natural size.

### Zoom UI

Place a control bar at the top-right of each `.mermaid-wrapper`:

```
[ − ]  [ 100% ]  [ + ]  [ ⟲ 重置 ]
```

- **+** / **−**: adjust `transform: scale(factor)` on the SVG.
  - Step: `0.2`
  - Range: `0.5` to `3.0`
- **重置**: restore scale to `1.0`.
- Set `transform-origin: top left` so the SVG stays anchored.

The wrapper’s `overflow-x: auto` handles overflow after zooming.

### Mobile

- Buttons must be ≥ 44 px touch targets.
- Support pinch zoom via `touchmove` distance calculation (optional).

## Render Fallback

If mermaid fails to render in the browser:

1. Keep the original source code visible in a `<pre>` block.
2. Add a short label: "图表渲染失败，显示原始代码。"

## Implementation Notes

- Do not add external JS libraries beyond mermaid.js itself.
- Zoom logic should be ~30 lines of vanilla JS per page.
- Respect `prefers-reduced-motion` for any zoom transitions.
