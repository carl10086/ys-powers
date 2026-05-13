---
description: Implements the next documentation task incrementally — draft, review against style guide, verify, save. Use when writing or updating technical documentation, user guides, API docs, or any Markdown documents following a spec/plan workflow.
---

## Workflow

Copy this checklist and track progress:

```
Doc Task Progress:
- [ ] Step 1: Read plan task and acceptance criteria
- [ ] Step 2: Load context (existing docs, references, code)
- [ ] Step 3: Draft content following the style guide
- [ ] Step 4: Self-review against checklist
- [ ] Step 5: Fix issues found
- [ ] Step 6: Save to specified path
- [ ] Step 7: Mark task complete
```

**Step 1: Read plan task**

Read the plan for this feature. If a plan was generated earlier in this session, use that file path. Otherwise, check `docs/ys-powers/plans/` for the most recent plan file, or ask the user for the spec path if ambiguous. Then pick the next pending documentation task.

Extract:
- Task description
- Acceptance criteria (what must be covered)
- Target file path
- Document type (install guide, API doc, tutorial, troubleshooting)

**Step 2: Load context**

Based on document type, load relevant context:
- Technical docs → read related source code, API definitions
- Product docs → read product specs, design docs
- Reference docs → read existing similar documents for style consistency

**Step 3: Draft content**

Write the documentation following the style guide. Use the appropriate template for the document type:

**Install guide template:**
```markdown
# [Title]

## Requirements
- OS / version constraints
- Dependencies and versions

## Installation
### Method 1 (recommended)
### Method 2 (alternative)

## Verification

## FAQ
```

**API doc template:**
```markdown
### [METHOD] [endpoint]

#### Parameters
| Name | Type | Required | Description |

#### Request example
#### Response example (success)
#### Response example (error)

#### Error codes
```

**Tutorial template:**
```markdown
## Goal
## Prerequisites
## Step 1
## Step 2
## Next steps
```

**Troubleshooting template:**
```markdown
## [Problem title]
### Symptoms
### Cause
### Solution
```

**Step 4: Self-review**

Review against the checklist in `docs/ys-powers/guidelines/chinese-tech-writing-guide.md` Section 9. Key items:

- [ ] Title levels are continuous, only one H1 per document
- [ ] Chinese and English are separated by spaces
- [ ] Code blocks have language identifiers
- [ ] Command lines use `$` for input, no `$` for output
- [ ] User-replaceable content wrapped in `< >` with explanation
- [ ] All code examples are runnable (or explicitly noted as simplified)
- [ ] Proper nouns have correct capitalization (GitHub, JavaScript, macOS)
- [ ] Technical terms have Chinese-English annotation on first appearance
- [ ] Error messages quoted in full original text
- [ ] Internal links use relative paths

**Step 5: Fix issues**

If any checklist item fails, revise the content. Repeat Step 4 until all items pass.

**Step 6: Save**

Save the document to the target path specified in the plan task. Confirm the path with the user if ambiguous.

**Step 7: Mark complete**

Mark the task as complete in the plan and move to the next pending documentation task.

## Feedback Loop

If verification fails during Step 4:
1. Note each issue with specific section reference
2. Revise the content
3. Run self-review again
4. Only proceed when all requirements are met
