"""
SIOP Meeting Action Item Extractor
-----------------------------------
Business Workflow : Summarize SIOP meetings into structured action items
User              : SIOP Master Scheduler
Model             : Claude (claude-haiku-4-5) via Anthropic API
"""

import os
import json
import time
import anthropic

# ── Configuration ──────────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

MODEL_NAME  = "claude-haiku-4-5"
MAX_TOKENS  = 1024
TEMPERATURE = 0.0   # kept at 0 for reproducibility
DELAY_SECS  = 5     # short pause between demo calls

# ── System Prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
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
""".strip()

# ── Core Function ──────────────────────────────────────────────────────────────
def extract_action_items(
    meeting_type: str,
    attendees: list[str],
    transcript: str
) -> list[dict]:
    """
    Send meeting details to Claude and return a list of action-item dicts.

    Parameters
    ----------
    meeting_type : str   e.g. "Demand Review", "Supply Review", "Executive S&OP"
    attendees    : list  Full names + roles, e.g. ["Sarah Lin (Demand Planner)", ...]
    transcript   : str   Raw meeting transcript text

    Returns
    -------
    list of dicts, each containing the six action-item fields
    """
    attendees_block = "\n".join(f"  - {a}" for a in attendees)

    user_message = f"""
Meeting Type : {meeting_type}

Attendees:
{attendees_block}

Transcript:
{transcript}
""".strip()

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    return json.loads(response.content[0].text)


# ── Pretty Printer ─────────────────────────────────────────────────────────────
def print_action_items(action_items: list[dict]) -> None:
    if not action_items:
        print("\n  No action items identified in this meeting.\n")
        return

    print(f"\n{'─'*70}")
    print(f"  {'ACTION ITEMS':^66}")
    print(f"{'─'*70}")
    for item in action_items:
        print(f"\n  {item.get('action_id', 'N/A')} | {item.get('priority','?')} Priority")
        print(f"  Action  : {item.get('action_text','')}")
        print(f"  Owner   : {item.get('owner','')}")
        print(f"  Request : {item.get('requester','')}")
        print(f"  Context : {item.get('context','')}")
    print(f"\n{'─'*70}\n")


# ── Sample Test Cases ──────────────────────────────────────────────────────────
SAMPLE_CASES = [
    {
        "label": "Case 1 — Normal: Standard Demand Review",
        "meeting_type": "Demand Review",
        "attendees": [
            "Sarah Lin (Demand Planner)",
            "Marcus Webb (Sales Director)",
            "Priya Nair (SIOP Master Scheduler)",
            "Tom Reyes (Finance Lead)",
        ],
        "transcript": """
Priya: Alright, let's get started with the demand review. Sarah, can you walk us through the latest numbers?

Sarah: Sure. We're seeing a 12% spike in demand for Product Line A in Q3, mostly driven by the new retail partnership Marcus's team signed last month. I need Marcus to get me the confirmed order volumes from that account by end of week so I can update the forecast.

Marcus: Absolutely, I'll have those to you by Friday.

Priya: Great. Tom, given that demand increase, can you flag whether the Q3 budget can absorb any additional procurement costs?

Tom: Yes, I'll run the numbers and send a budget impact summary to Priya and Sarah by next Wednesday.

Priya: Perfect. Sarah, anything else?

Sarah: One more thing — we need to decide if we're going to adjust the safety stock policy for Product Line A given the new demand signal. Priya, can you draft a proposal for the team to review before the next cycle?

Priya: I'll have a draft ready in two weeks.
""".strip(),
    },
    {
        "label": "Case 4 — Edge: No Explicit Action Items",
        "meeting_type": "Demand Review",
        "attendees": [
            "Sarah Lin (Demand Planner)",
            "Priya Nair (SIOP Master Scheduler)",
            "Tom Reyes (Finance Lead)",
        ],
        "transcript": """
Priya: Let's do a quick check-in on the demand picture for Q2.

Sarah: Looks pretty stable. Forecast is in line with last cycle — no major changes. Product Lines B and C are tracking to plan.

Tom: Financials align with what we reviewed last week. Nothing new to flag.

Priya: Great. Sounds like we're in a good place. Let's reconvene next cycle unless something changes.
""".strip(),
    },
    {
        "label": "Case 5 — Likely to Fail: Ambiguous Ownership",
        "meeting_type": "Supply Review",
        "attendees": [
            "James Okafor (Supply Planner)",
            "Dana Cho (Procurement Manager)",
            "Priya Nair (SIOP Master Scheduler)",
            "Rachel Moore (Logistics Coordinator)",
        ],
        "transcript": """
Priya: We really need to get on top of the inbound shipment delays. It's been a recurring issue.

James: Yeah, someone should probably look into the root cause with the carrier. It's been three weeks.

Dana: Procurement has been trying to get answers too. I feel like logistics needs to own that conversation.

Rachel: I mean, we've reached out but haven't heard back. Maybe procurement should escalate?

Dana: We could, but honestly it might carry more weight coming from supply planning.

James: Either way, we need a decision on whether to activate the secondary carrier. That's been sitting for a while.

Priya: Right, let's not let that slip again. Someone needs to own that.

Rachel: Agreed. We also need to update the inbound tracking board but I'm not sure who has access to do that.

Priya: Okay, we'll figure it out offline. Let's move on.
""".strip(),
    },
]


# ── Interactive Mode ───────────────────────────────────────────────────────────
def run_interactive() -> None:
    print("\n=== SIOP Action Item Extractor (Interactive Mode) ===\n")
    meeting_type = input("Meeting type (e.g. Demand Review): ").strip()
    print("Enter attendees one per line. Press Enter twice when done:")
    attendees = []
    while True:
        line = input("  Attendee: ").strip()
        if not line:
            break
        attendees.append(line)
    print("Paste the transcript below. Type END on a new line when finished:")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    transcript = "\n".join(lines)

    print("\nProcessing...")
    items = extract_action_items(meeting_type, attendees, transcript)
    print_action_items(items)


# ── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Run all sample cases with a short pause between each
        for i, case in enumerate(SAMPLE_CASES):
            print(f"\n{'='*70}")
            print(f"  {case['label']}")
            print(f"{'='*70}")
            items = extract_action_items(
                case["meeting_type"],
                case["attendees"],
                case["transcript"],
            )
            print_action_items(items)

            if i < len(SAMPLE_CASES) - 1:
                print(f"  Waiting {DELAY_SECS}s before next case...")
                time.sleep(DELAY_SECS)
    else:
        run_interactive()
