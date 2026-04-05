# Report

---

## 1. Business Use Case

The chosen workflow is summarizing SIOP (Sales, Inventory & Operations Planning) meetings into structured action items for a SIOP Master Scheduler. After each meeting — whether a demand review, supply review, or executive S&OP — the scheduler must manually identify who committed to what, who requested it, how urgent it is, and why it matters. This process is time-consuming, inconsistent across facilitators, and error-prone when done manually from long transcripts or recordings. Partially automating it saves the scheduler significant time, improves clarity by enforcing a consistent output structure, and ensures no follow-ups are missed regardless of who ran the meeting.

The model selected for this project is **claude-haiku-4-5** via the Anthropic Claude API. Claude was chosen over other available models for several reasons. First, it performed reliably on structured extraction tasks — returning well-formatted JSON consistently without requiring complex post-processing. Second, it handled edge cases gracefully, correctly returning an empty list when a meeting had no action items rather than hallucinating tasks. Third, the Anthropic API was straightforward to set up and use. This project originally attempted to use Google AI Studio with the Gemini API, but despite creating a new project, enabling the Generative Language API, and generating multiple API keys, the free tier quota was consistently set to 0 and could not be resolved after significant troubleshooting. Switching to the Anthropic Claude API resolved all access issues immediately and the prototype was up and running within minutes.

---

## 2. Baseline vs. Final Design Comparison

The system prompt went through three versions. Each revision was driven by specific failures observed in the evaluation set rather than assumptions about what would work.

| Dimension | Version 0 (Baseline) | Version 2 (Final) |
|---|---|---|
| **Role** | Generic "helpful assistant" | SIOP Master Scheduler domain role |
| **Output format** | Unstructured — prose, bullets, or lists | Consistent JSON with 6 required fields |
| **Priority values** | Unconstrained — "Urgent", "Critical", "Normal" | Constrained to "High", "Medium", or "Low" |
| **No-action meetings** | Hallucinated filler tasks | Correctly returns empty list |
| **Ambiguous ownership** | Confidently assigned wrong owner | Correctly uses "TBD" for 2 of 3 ambiguous cases |
| **User message context** | Transcript only | Meeting type + attendees + transcript |
| **Cases passing** | 0 / 5 | 4 / 5 (1 partial) |

The most significant improvement came from adding an explicit output schema (V0 → V1), which alone moved the system from 0 passing cases to 3 by enforcing consistent structure and constrained field values. The second revision (V1 → V2) added two targeted instructions — `"return an empty list if no action items are found"` and `"use TBD if ownership was never clearly assigned"` — which resolved the no-action hallucination in Case 4 and partially resolved ambiguous ownership in Case 5. Including meeting type and attendees in the user message also improved the model's ability to infer priority, particularly for executive-level meetings where urgency is higher.

---

## 3. Where the Prototype Still Fails or Requires Human Review

The prototype performs reliably on well-structured transcripts with clear commitments and named owners, but two conditions require human review before action items are distributed to stakeholders. First, when ownership is disputed or never explicitly assigned — as in Case 5 — the model partially flags ambiguity using "TBD" but still tends to assign a name when one person is mentioned frequently in connection with a task. In these cases, a human must confirm or reassign ownership before the action item is acted on. Second, priority inference is subjective: the model makes reasonable judgments based on meeting type and context, but may rate items differently than the scheduler would, particularly for follow-up or administrative tasks. A human review step is recommended any time priority affects resource allocation or escalation decisions.
