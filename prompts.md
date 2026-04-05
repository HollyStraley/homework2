# Prompts

**Business Workflow:** Summarizing SIOP meetings into structured action items
**User:** SIOP Master Scheduler
**Model:** claude-haiku-4-5 via Anthropic API

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

### 1. Role Assignment in System Prompt
The system prompt opens with a specific role: *"You are an AI assistant for a SIOP Master Scheduler."* This grounds the model in the business context and reduces the chance of generic responses. By naming the domain (SIOP), the model understands that terms like "demand cycle," "safety stock," and "supply plan" have precise meanings and should be treated accordingly.

### 2. Explicit Output Schema
Rather than asking the model to "summarize action items," the prompt defines exactly six fields with names, types, and constraints (e.g., priority must be "High", "Medium", or "Low"). This enforces consistency across all meeting types and makes the output machine-readable without post-processing guesswork.

### 3. Structured JSON Output
Requesting JSON output instead of free text allows the app to parse, display, and eventually store results programmatically. The system prompt instructs the model to return *only* JSON with no extra commentary, which reduces parsing failures. A code fence stripper was added to handle cases where the model wraps JSON in markdown code blocks.

### 4. TBD for Ambiguous Ownership
The instruction *"use 'TBD' if ownership was never clearly assigned"* was added specifically to handle Case 5 (ambiguous ownership). Without this instruction, the model tends to confidently assign an owner even when the transcript shows disputed responsibility — a known failure mode for LLMs on ownership ambiguity.

### 5. Empty List for No Action Items
The instruction *"If no action items are found, return an empty list []"* handles the edge case where a meeting is purely informational (Case 4). This prevents the model from hallucinating tasks to fill the output and ensures the app can gracefully display "No action items identified."

### 6. Temperature Set to 0
`temperature=0.0` is used throughout to ensure deterministic, reproducible outputs. This is important for evaluation — running the same transcript twice should produce the same result, making it easier to compare outputs across prompt iterations.

### 7. Meeting Type and Attendees as Context
Including the meeting type and full attendees list in the user message (not just the transcript) gives the model additional signal for inferring ownership and priority. For example, knowing the meeting is an "Executive S&OP" helps the model recognize that action items carry higher urgency than a routine demand check-in.
