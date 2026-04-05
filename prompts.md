# Prompts

**Business Workflow:** Summarizing SIOP meetings into structured action items
**User:** SIOP Master Scheduler
**Model:** claude-haiku-4-5 via Anthropic API

---

## System Prompt

This is the system instruction sent to the model before every request. It establishes the model's role, defines the exact output schema, and sets boundaries for what to do when no action items exist.

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

## User Message Template

This is the structure of the message sent to the model for each meeting. The three variables — `{meeting_type}`, `{attendees}`, and `{transcript}` — are populated at runtime.

```
Meeting Type : {meeting_type}

Attendees:
  - {attendee_1}
  - {attendee_2}
  - ...

Transcript:
{transcript}
```

**Example populated input (Case 1):**
```
Meeting Type : Demand Review

Attendees:
  - Sarah Lin (Demand Planner)
  - Marcus Webb (Sales Director)
  - Priya Nair (SIOP Master Scheduler)
  - Tom Reyes (Finance Lead)

Transcript:
Priya: Alright, let's get started with the demand review...
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

---

## What Was Tried and What Didn't Work

| Approach | Result |
|---|---|
| No schema defined — asked for "a summary of action items" | Output format was inconsistent; some responses used bullet points, others used prose |
| Asked for priority without defining valid values | Model used values like "Urgent", "Critical", "Normal" — inconsistent across cases |
| No TBD instruction for ambiguous ownership | Model confidently assigned wrong owners in Case 5 (confirmed failure) |
| No empty list instruction for no-action meetings | Model invented placeholder tasks in Case 4 on early iterations |
