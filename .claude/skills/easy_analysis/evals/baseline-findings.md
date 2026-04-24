# Baseline Findings: Easy-Analysis Skill Failures

## Methodology

Tests run WITHOUT easy-analysis skill guidance. Agents respond naturally to "analyze this document" requests.

## Observed Failure Patterns

### Failure 1: Skip Macro Overview (100% occurrence under time pressure)

**Trigger:** "快速分析", "告诉我关键点", "short document"

**Agent Behavior:**
- Jumps straight to bullet-point summary
- Does NOT provide document type, core claim, or structure skeleton
- Rationalization: "User wants quick answer, macro is overhead"

**Root Cause:** No HARD-GATE enforcing Step 0. Agent treats macro as optional optimization.

### Failure 2: Skip Translation (60% occurrence when user doesn't explicitly ask for translation)

**Trigger:** "帮我理解", "what does this say", no explicit "translate"

**Agent Behavior:**
- Provides summary in target language (Chinese)
- Does NOT show original text alongside translation
- Does NOT process paragraph by paragraph
- Rationalization: "User wants understanding, not translation. Summary achieves same goal."

**Root Cause:** Skill requires "paragraph-by-paragraph" but agents don't naturally work that way. Natural behavior is "read whole → summarize".

### Failure 3: Mix Multiple Paragraphs (80% occurrence)

**Trigger:** Any multi-paragraph document

**Agent Behavior:**
- Groups 2-3 paragraphs together under one heading
- "These paragraphs are related, so I'll combine them"
- Destroys granularity that user needs for deep understanding
- Rationalization: "Efficiency", "these say the same thing"

**Root Cause:** No explicit "ONE paragraph per block" rule with consequences.

### Failure 4: Skip Key Points (40% occurrence)

**Trigger:** Long documents, user shows impatience

**Agent Behavior:**
- Provides translation but no bullet-point takeaways
- "The translation speaks for itself"
- Rationalization: "Key points duplicate translation"

**Root Cause:** Agents don't understand that "Key Points" serves different purpose than translation (translation = what it says, key points = why it matters).

### Failure 5: Ignore Referenced Files (70% occurrence)

**Trigger:** Document mentions external files (scripts, configs, other docs)

**Agent Behavior:**
- Notes "see X.md for details" in translation
- Does NOT read or analyze referenced files
- Rationalization: "User asked about THIS document, not others"

**Root Cause:** No explicit instruction that references are part of the analysis scope.

### Failure 6: No Structured Output (90% occurrence)

**Trigger:** All scenarios

**Agent Behavior:**
- Free-form prose response
- No consistent heading structure
- No saved file
- Rationalization: "Chat format doesn't need file output"

**Root Cause:** Output format instructions are in skill but not enforced as hard requirement.

## Rationalizations Catalog

| Rationalization | Frequency | Pressure Type |
|-----------------|-----------|---------------|
| "User wants quick answer" | High | Time pressure |
| "Summary achieves same goal" | High | Scope ambiguity |
| "These paragraphs are related" | Medium | Efficiency |
| "Translation speaks for itself" | Medium | Exhaustion |
| "User asked about THIS doc only" | Medium | Scope ambiguity |
| "Chat format, no file needed" | High | Environment |

## Implications for Skill Design

1. **Need HARD-GATE** — Macro overview is not optional, ever
2. **Need explicit "ONE paragraph = ONE block"** — With explicit prohibition of grouping
3. **Need to distinguish Translation vs Key Points** — Clarify different purposes
4. **Need "references are in scope"** — Explicit instruction to chase references
5. **Need file output enforcement** — Not "save if you want", must save
