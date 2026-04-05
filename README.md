# Homework 2 - Generative AI

[https://www.youtube.com/channel/UCtEsf8bLE9IcRMv8LOFllUA](https://www.youtube.com/channel/UCtEsf8bLE9IcRMv8LOFllUA)

## Overview
This project explores prompt engineering and evaluation for a generative AI application focused on automating a real business workflow using the **Anthropic Claude API**.

## Business Workflow: Meeting Summarization into Action Items

**Chosen Workflow:** Summarizing meetings into structured action items

**User:** SIOP Master Scheduler

### System Input
The system receives the following information from each meeting:
- **Attendees List** — Names and roles of all meeting participants
- **Full Transcript** — Complete verbatim transcript of the meeting
- **Meeting Type** — The category or purpose of the meeting (e.g., demand review, supply review, executive S&OP)

### System Output
The system produces a structured set of action items, each containing:
- **Action ID** — Unique identifier for tracking purposes
- **Action Text** — Clear description of the task to be completed
- **Owner** — The person responsible for completing the action
- **Requester** — The person or role who requested the action
- **Priority** — Urgency level of the action item (e.g., High, Medium, Low)
- **Context** — Background information or rationale to help the owner understand the action

### Why This Is Valuable to Partially Automate

Manually extracting action items from long SIOP meetings is time-consuming and error-prone. By automating this workflow, the SIOP Master Scheduler can save significant time that would otherwise be spent re-listening to recordings or parsing dense transcripts. Automation also improves **clarity** by enforcing a consistent structure for every action item, reducing ambiguity about ownership and deadlines. Finally, it drives **consistency** across meeting types — ensuring no critical follow-ups are missed and that every stakeholder receives the same quality of post-meeting documentation regardless of who is facilitating.

## Files
- `app.py` — Main application code
- `prompts.md` — Prompt templates and design decisions
- `eval_set.md` — Evaluation dataset with inputs and expected outputs
- `report.md` — Analysis and findings


## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Anthropic API key
```bash
# Windows (Command Prompt)
set ANTHROPIC_API_KEY=your-api-key-here
```
Get a free API key at [https://console.anthropic.com](https://console.anthropic.com).

### 3. Run the app

**Interactive mode** — enter your own meeting details:
```bash
python app.py
```

**Demo mode** — runs all 3 sample eval cases automatically:
```bash
python app.py --demo
```
