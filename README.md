# Homework 2 - Generative AI

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

## Commit History

| Commit | Description |
|--------|-------------|
| cbcf9b7 | Add opening summary paragraph to prompts.md |
| 0153c36 | Condense design decisions into concise bullet points |
| b1b6a80 | Replace failure conditions paragraph with user's own words |
| 47b0fee | Replace business use case section with user's own words |
| 49b31fb | Restructure report with business use case, comparison table, and failure conditions |
| 34403db | Remove Analysis section from report |
| fb54594 | Add baseline vs final comparison table and Google AI Studio note to report |
| 0453b4b | Add complete report.md with introduction, approach, results, analysis, and conclusion |
| aee8b9f | Add prompt iteration log with V0, V1, V2 and evidence-based improvements |
| 6f088ed | Add full prompts.md with system prompt, user template, and design decisions |
| 142d303 | Remove requirements.txt and results.txt |
| 8f0988a | Add results.txt with demo output for all 5 eval cases |
| 8deb49a | Meet all grading requirements: configurable prompt, file output, API key check, argparse |
| b2d701d | Fill in actual outputs for Cases 2 and 3 from demo run |
| 2ae2baf | Add Cases 2 and 3 to demo sample cases |
| 9105adb | Fill in actual outputs for Cases 1, 4, and 5 from demo run |
| a7d8e1a | Fix JSON parsing to strip markdown code fences from Claude response |
| 157d9b3 | Switch from Google Gemini to Anthropic Claude API |
| a8d1bbb | Switch to gemini-2.0-flash-lite to avoid free tier quota exhaustion |
| b5bce33 | Switch to google-genai SDK and add rate limit delay between demo cases |
| 6ed4bce | Build SIOP action item extractor prototype using Google Gemini API |
| be85c19 | Simplify actual output sections to owner, requester, priority, and context summary |
| f9b6f02 | Add evaluation set with 5 representative SIOP meeting test cases |
| baaeb2d | Update README with SIOP meeting summarization workflow details |
| 4b15244 | Initial commit: add project files for Homework 2 GenAI |

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
