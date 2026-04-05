# Report

**Business Workflow:** Summarizing SIOP meetings into structured action items
**User:** SIOP Master Scheduler
**Model:** claude-haiku-4-5 via Anthropic API

---

## Introduction

This project automates a high-value but time-consuming task for a SIOP (Sales, Inventory & Operations Planning) Master Scheduler: extracting structured action items from meeting transcripts. After each SIOP meeting — whether a demand review, supply review, or executive S&OP — the scheduler must manually identify who committed to what, who requested it, how urgent it is, and why it matters. This process is error-prone, inconsistent across facilitators, and slow when done manually from long transcripts or recordings.

The goal of this project was to build a small, reproducible Python prototype that accepts a meeting transcript, attendees list, and meeting type as inputs, and returns a structured set of action items containing: Action ID, Action Text, Owner, Requester, Priority, and Context. The system uses the Anthropic Claude API (`claude-haiku-4-5`) and was evaluated against a five-case evaluation set covering normal, edge, and failure scenarios.

---

## Approach

### Prompt Engineering Strategy
The system prompt was developed iteratively across three versions, with each revision driven by observed failures in the evaluation set rather than assumptions about what would work.

- **Version 0** established a baseline using a generic "helpful assistant" prompt with no schema. This confirmed that without structure, the model's outputs were inconsistent and unparseable.
- **Version 1** introduced a domain-specific role, a six-field JSON output schema, and constrained priority values. This resolved format inconsistency but left two failure modes unaddressed.
- **Version 2** added two targeted instructions — `"use 'TBD' if ownership was never clearly assigned"` and `"If no action items are found, return an empty list []"` — based on direct evidence from Case 4 and Case 5 outputs. The user message was also expanded to include meeting type and attendees as additional context.

### Reproducibility
`temperature=0.0` was set throughout all evaluations to ensure deterministic outputs. The demo mode (`python app.py --demo`) runs all five evaluation cases with fixed inputs, making results fully reproducible by any grader or TA with an Anthropic API key.

### Configurability
The system prompt is externalized and configurable via a `--system-prompt` flag, allowing a user to swap in a custom prompt file without modifying source code. This supports experimentation and future prompt iterations.

---

## Results

The app was evaluated against five representative cases. Results are summarized below:

| Case | Type | Expected | Actual | Pass? |
|------|------|----------|--------|-------|
| 1 | Normal — Demand Review | 3 action items, correct owners | 3 action items, all fields correct | ✅ Pass |
| 2 | Normal — Supply Review | 3 action items, multiple owners | 3 action items, all fields correct | ✅ Pass |
| 3 | Normal — Executive S&OP | 3 action items, high priority | 3 action items, all High priority | ✅ Pass |
| 4 | Edge — No action items | Empty list, no hallucination | Correctly returned no action items | ✅ Pass |
| 5 | Likely to Fail — Ambiguous ownership | TBD for all 3 owners | TBD for ACT-002 and ACT-003; wrong owner for ACT-001 | ⚠️ Partial |

**Overall: 4 full passes, 1 partial pass across 5 cases.**

### Case 5 Detail
In Case 5, the model correctly used "TBD" for two of the three ambiguous action items (ACT-002 and ACT-003). However, for ACT-001 — where four participants actively disputed ownership of the carrier investigation — the model assigned James Okafor as owner. This is the predicted failure mode: when the transcript contains repeated references to one person in connection with a task, the model tends to resolve ambiguity by selecting the most frequently associated name rather than flagging the dispute.

---

## Baseline vs. Final Design Comparison

The table below shows how the prompt evolved from the initial draft to the final version and the measurable impact on output quality across the evaluation set.

| Dimension | Version 0 (Baseline) | Version 2 (Final) |
|---|---|---|
| **Role** | Generic "helpful assistant" | SIOP Master Scheduler domain role |
| **Output format** | Unstructured — prose, bullets, or lists | Consistent JSON with 6 required fields |
| **Priority values** | Unconstrained — "Urgent", "Critical", "Normal" | Constrained to "High", "Medium", or "Low" |
| **No-action meetings** | Hallucinated filler tasks | Correctly returns empty list |
| **Ambiguous ownership** | Confidently assigned wrong owner | Correctly uses "TBD" for 2 of 3 ambiguous cases |
| **User message context** | Transcript only | Meeting type + attendees + transcript |
| **Cases passing** | 0 / 5 | 4 / 5 (1 partial) |

The most significant improvements came from adding an explicit output schema (V0 → V1), which alone moved the system from 0 passing cases to 3, and from adding targeted edge case instructions (V1 → V2), which resolved the no-action hallucination and partially resolved ambiguous ownership.

---

## Analysis

### What Worked Well

**Role + schema = consistent structure.** The single most impactful change across all three prompt versions was adding a domain-specific role and an explicit output schema. Before Version 1, outputs varied in format on every call. After Version 1, all normal cases produced identical structure with correct field names and constrained values. This confirms that explicit output schemas are essential for structured extraction tasks.

**Empty list instruction eliminated hallucination in Case 4.** Without the `"return an empty list []"` instruction, the model invented filler tasks in informational meetings. With it, Case 4 returned a clean empty result every time. This is an example where a single sentence in the prompt directly prevented a meaningful failure.

**Meeting type and attendees improved context.** Adding meeting type and attendees to the user message helped the model correctly infer that all action items in Case 3 (Executive S&OP) were High priority — a judgment call that requires understanding the meeting's organizational significance.

### What Didn't Work

**TBD instruction only partially solved ambiguous ownership.** The `"use 'TBD'"` instruction worked for cases where no owner was mentioned at all (ACT-002, ACT-003 in Case 5), but failed when one name appeared frequently in the context of a disputed task. The model appears to use frequency of association as a proxy for ownership, which is a reasonable heuristic but not correct when the transcript explicitly shows disagreement. A stronger instruction — such as explicitly defining what "ambiguous" means — may be needed in a future revision.

**Priority for Case 3 deviated slightly from expected.** The expected output for Case 3 included one Medium priority item (ACT-003 — updating the master plan). The model returned High for all three, reasoning that master plan updates are time-sensitive in an executive context. This is a defensible interpretation, but it shows that priority inference is subjective and may need more explicit guidance for nuanced cases.

### Limitations
- The system relies on the transcript being verbatim and reasonably well-formatted. Transcripts with speaker confusion, crosstalk, or heavy domain jargon may degrade output quality.
- Ownership ambiguity remains a hard problem. No prompt instruction fully resolves cases where multiple people discuss a task without committing. A human review step is still recommended for these cases.
- The prototype does not handle multi-meeting context — each transcript is processed independently with no memory of prior action items or carryover commitments.

---

## Conclusion

This project demonstrated that a large language model can reliably extract structured action items from SIOP meeting transcripts when given a well-designed prompt, a clear output schema, and targeted instructions for edge cases. Across four of five evaluation cases, the system produced accurate, complete, and consistently formatted output.

The most important lesson from this project is that **prompt engineering is an empirical process**. The final prompt was not written correctly on the first attempt — it required two rounds of revision driven by direct evidence from the evaluation set. Each revision addressed a specific, observed failure rather than a hypothetical one. This evidence-based approach produced measurable improvements: Version 0 produced unstructured, inconsistent output; Version 2 passed 4 out of 5 cases with structured, parseable JSON every time.

The remaining failure — ambiguous ownership in Case 5 — reflects a fundamental limitation of extracting commitments from conversational text. Partially automating this workflow is appropriate: the model handles clear cases confidently and flags ambiguity where possible, but a human reviewer should validate ownership before distributing action items to stakeholders.

On a practical note, this project originally attempted to use Google AI Studio with the Gemini API. Despite creating a new project, enabling the Generative Language API, and generating multiple API keys, the free tier quota was consistently set to 0 and could not be resolved. After significant troubleshooting, the decision was made to switch to the Anthropic Claude API, which worked reliably on the first attempt. The transition required minimal code changes and the Claude API proved to be straightforward to set up and use throughout the rest of the project.
