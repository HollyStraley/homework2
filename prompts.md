# Prompts

**Business Workflow:** Summarizing SIOP meetings into structured action items
**User:** SIOP Master Scheduler
**Model:** claude-haiku-4-5 via Anthropic API

Across the revisions, the biggest things that changed was defining the outputs more (example low, medium, high priority) and implementing a 'TBD' for ownership when the prototype isn't sure who it belongs to and ultimately flags for human review. These changes enforces consistency and accuracy so the wrong human isn't assigned to the wrong task.

---

## Prompt Iteration Log

The system prompt went through three versions. Each revision was driven by specific evidence observed in the model's outputs against the evaluation set.

---

### Version 0 — Initial Draft

**System Prompt:**
```
You are a helpful assistant. Read the following meeting transcript and summarize the action items.
```

**User Message:**
```
Transcript:
{transcript}
```

**What changed and why:**
This was the simplest possible starting point — a generic role and a single instruction with no output format defined. It was tested first to establish a baseline and understand where the model would fail without guidance.

**What we observed:**
- Output format was completely inconsistent: some responses used bullet points, others used numbered lists, others wrote full paragraphs
- Priority values varied with no constraint — the model used "Urgent", "Critical", "Normal", and "Low" interchangeably across cases
- Ownership was assigned confidently even in Case 5 where it was disputed, with no indication of ambiguity
- In Case 4 (no action items), the model invented vague placeholder tasks like "Team to reconvene next cycle" rather than returning nothing
- No requester or context fields were included since they were never asked for

---

### Version 1 — Added Role, Schema, and JSON Output

**System Prompt:**
```
You are an AI assistant for a SIOP (Sales, Inventory & Operations Planning) Master Scheduler.
Your job is to read a meeting transcript and extract every action item that was committed to or requested.

For each action item return a JSON object with exactly these fields:
  - action_id   : sequential string, e.g. "ACT-001"
  - action_text : concise, specific description of the task (1-2 sentences)
  - owner       : full name of the person responsible for completing the action
  - requester   : full name of the person who requested or triggered the action
  - priority    : one of "High", "Medium", or "Low"
  - context     : 1-2 sentence explanation of why this action matters

Always return valid JSON — a list of action-item objects — with no extra commentary.
```

**User Message:**
```
Transcript:
{transcript}
```

**What changed and why:**
Three things were added based on Version 0 failures: (1) a specific domain role to ground the model in SIOP context, (2) an explicit six-field output schema so every response had the same structure, and (3) a constrained priority field with only three allowed values to eliminate inconsistent labels.

**What improved, stayed the same, or got worse:**
- ✅ Output format became fully consistent across all normal cases — JSON parsed correctly every time
- ✅ Priority values were now always "High", "Medium", or "Low" with no variation
- ✅ Cases 1, 2, and 3 produced accurate, well-structured action items
- ⚠️ Case 4 (no action items) still caused issues — without guidance, the model returned an empty JSON object `{}` instead of a valid empty list, breaking the parser
- ⚠️ Case 5 (ambiguous ownership) still failed — the model confidently assigned James Okafor as owner for ACT-001 despite ownership being openly disputed in the transcript

---

### Version 2 — Final Prompt (Added Edge Case Handling and Context Inputs)

**System Prompt:**
```
You are an AI assistant for a SIOP (Sales, Inventory & Operations Planning) Master Scheduler.
Your job is to read a meeting transcript and extract every action item that was committed to or requested.

For each action item return a JSON object with exactly these fields:
  - action_id   : sequential string, e.g. "ACT-001"
  - action_text : concise, specific description of the task (1-2 sentences)
  - owner       : full name of the person responsible for completing the action
                  (use "TBD" if ownership was never clearly assigned)
  - requester   : full name of the person who requested or triggered the action
  - priority    : one of "High", "Medium", or "Low"
  - context     : 1-2 sentence explanation of why this action matters

If no action items are found, return an empty list [].

Always return valid JSON — a list of action-item objects — with no extra commentary.
```

**User Message:**
```
Meeting Type : {meeting_type}

Attendees:
  - {attendee_1}
  - {attendee_2}
  - ...

Transcript:
{transcript}
```

**What changed and why:**
Two instructions were added to the system prompt: `"use 'TBD' if ownership was never clearly assigned"` to address the ambiguous ownership failure in Case 5, and `"If no action items are found, return an empty list []"` to fix the parser crash in Case 4. The user message was also expanded to include meeting type and attendees list, giving the model additional context to infer priority and ownership more accurately.

**What improved, stayed the same, or got worse:**
- ✅ Case 4 now correctly returns an empty list and the app displays "No action items identified" without hallucinating tasks
- ✅ Case 5 improved partially — ACT-002 and ACT-003 now correctly use "TBD" where ownership was unclear
- ⚠️ Case 5 ACT-001 still assigns James Okafor as owner — this remains the confirmed failure case, as the model resolves ambiguity by picking the most referenced name rather than flagging the dispute
- ✅ Cases 1, 2, and 3 remained accurate and consistent with the previous version

---

## Final System Prompt (Version 2)

```
You are an AI assistant for a SIOP (Sales, Inventory & Operations Planning) Master Scheduler.
Your job is to read a meeting transcript and extract every action item that was committed to or requested.

For each action item return a JSON object with exactly these fields:
  - action_id   : sequential string, e.g. "ACT-001"
  - action_text : concise, specific description of the task (1-2 sentences)
  - owner       : full name of the person responsible for completing the action
                  (use "TBD" if ownership was never clearly assigned)
  - requester   : full name of the person who requested or triggered the action
  - priority    : one of "High", "Medium", or "Low"
  - context     : 1-2 sentence explanation of why this action matters

If no action items are found, return an empty list [].

Always return valid JSON — a list of action-item objects — with no extra commentary.
```

---

## Design Decisions

- **Role assignment** — Giving the model a specific SIOP role grounds it in the business context and reduces generic responses.
- **Explicit output schema** — Defining all six fields with constraints (e.g. priority must be "High", "Medium", or "Low") enforces consistency and makes output machine-readable.
- **JSON output** — Requesting JSON instead of free text allows the app to parse and display results reliably. A code fence stripper handles cases where the model wraps the JSON in markdown blocks.
- **TBD for ambiguous ownership** — Without this instruction the model confidently assigns wrong owners; "TBD" signals to the reviewer that human confirmation is needed.
- **Empty list for no action items** — Prevents the model from hallucinating tasks when a meeting is purely informational.
- **Temperature set to 0** — Ensures deterministic, reproducible outputs so the same transcript always returns the same result.
- **Meeting type and attendees as context** — Giving the model this additional input helps it infer priority and ownership more accurately, especially for executive-level meetings.
