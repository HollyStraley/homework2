# Report

---

## 1. Business Use Case

I chose a workflow in summarizing SIOP (Sales, Inventory & Operations Planning) meetings into quick actionable items for the SIOP Master Scheduler (or others in similar roles). In each meeting (specifically FOR meetings), there are many action items that have different urgency needs. In partially automating these notes and organizing them by importance, it could save the Master Scheduler some time.

As for the chosen model that I used, I initially tried to work with the Google AI Studio and unfortunately couldn't get it working, despite creating a new API key. Instead, I used Anthropic Claude API and was able to resolve things rather quickly and my prototype was up and running shortly after.

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

The prototype performed well on most clear structured transcripts that defined specific ownership (as it showed in most cases). However, in some cases such as case 5 when the ownership is not clear, the prototype was not able to successfully flag it correctly and was instead using 'TBD' or another name that was mentioned frequently. Overall, I would recommend deploying this workflow but would also keep in mind that anytime there is any 'follow up' requests, those are reviewed by a human as the priority on those may be scored differently than what the prototype would do.
