"""
SIOP Meeting Action Item Extractor
-----------------------------------
Business Workflow : Summarize SIOP meetings into structured action items
User              : SIOP Master Scheduler
Model             : Claude (claude-haiku-4-5) via Anthropic API

Usage
-----
  # Run all 5 eval cases and save output to results.txt (default)
  python app.py --demo

  # Run demo with a custom system prompt from a file
  python app.py --demo --system-prompt my_prompt.txt

  # Run demo and save output to a custom file
  python app.py --demo --output my_results.txt

  # Interactive mode — enter your own meeting
  python app.py
"""

import os
import sys
import json
import time
import argparse
import anthropic

# ── Configuration ──────────────────────────────────────────────────────────────
MODEL_NAME   = "claude-haiku-4-5"
MAX_TOKENS   = 1024
TEMPERATURE  = 0.0        # kept at 0 for reproducibility
DELAY_SECS   = 5          # pause between demo calls
DEFAULT_OUTPUT_FILE = "results.txt"

# ── Default System Prompt (configurable via --system-prompt flag) ───────────
DEFAULT_SYSTEM_PROMPT = """
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
    transcript: str,
    system_prompt: str,
    client: anthropic.Anthropic
) -> list[dict]:
    """
    Send meeting details to Claude and return a list of action-item dicts.

    Parameters
    ----------
    meeting_type  : str   e.g. "Demand Review", "Supply Review", "Executive S&OP"
    attendees     : list  Full names + roles, e.g. ["Sarah Lin (Demand Planner)", ...]
    transcript    : str   Raw meeting transcript text
    system_prompt : str   The system instruction sent to the model
    client        : anthropic.Anthropic  Authenticated API client

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
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    # Strip markdown code fences if Claude wraps the JSON in ```json ... ```
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


# ── Formatting Helpers ─────────────────────────────────────────────────────────
def format_action_items(label: str, action_items: list[dict]) -> str:
    """Return a formatted string block for a single case."""
    lines = []
    lines.append(f"\n{'='*70}")
    lines.append(f"  {label}")
    lines.append(f"{'='*70}")

    if not action_items:
        lines.append("\n  No action items identified in this meeting.\n")
        return "\n".join(lines)

    lines.append(f"\n{'─'*70}")
    lines.append(f"  {'ACTION ITEMS':^66}")
    lines.append(f"{'─'*70}")
    for item in action_items:
        lines.append(f"\n  {item.get('action_id', 'N/A')} | {item.get('priority','?')} Priority")
        lines.append(f"  Action  : {item.get('action_text','')}")
        lines.append(f"  Owner   : {item.get('owner','')}")
        lines.append(f"  Request : {item.get('requester','')}")
        lines.append(f"  Context : {item.get('context','')}")
    lines.append(f"\n{'─'*70}\n")
    return "\n".join(lines)


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
        "label": "Case 2 — Normal: Supply Review with Multiple Owners",
        "meeting_type": "Supply Review",
        "attendees": [
            "James Okafor (Supply Planner)",
            "Dana Cho (Procurement Manager)",
            "Priya Nair (SIOP Master Scheduler)",
            "Luis Ortega (Warehouse Ops Lead)",
        ],
        "transcript": """
Priya: Let's go through supply constraints for the next two cycles. James, what are we looking at?

James: We have a capacity constraint at the Chicago DC — we're at 94% utilization and expecting more inbound from the East Coast supplier next month. Luis, we need you to identify overflow storage options by the 15th.

Luis: Understood, I'll look into third-party storage options and get back to you.

James: Also, Dana, we had a lead time increase from Supplier 47 — they moved from 6 to 9 weeks. Can you get on a call with them this week and push back? We need that resolved before the next demand cycle.

Dana: I'll reach out to them today and aim to have an answer by Thursday.

Priya: Great. And James, please update the supply plan in the system to reflect the new lead times so we're not planning on stale data.

James: Will do, I'll update it by EOD tomorrow.
""".strip(),
    },
    {
        "label": "Case 3 — Normal: Executive S&OP Meeting",
        "meeting_type": "Executive S&OP",
        "attendees": [
            "Carol Simmons (VP Supply Chain)",
            "David Park (CFO)",
            "Priya Nair (SIOP Master Scheduler)",
            "Marcus Webb (Sales Director)",
        ],
        "transcript": """
Carol: The consensus plan shows a gap of 8,000 units in Q4 that we haven't resolved. David, we need a decision on whether to approve emergency procurement funding — can you get that approved or denied by end of month?

David: Yes, I'll take it to the exec committee this Thursday and confirm by Friday.

Carol: Marcus, we also need a realistic top-down number from Sales leadership for Q4 — the bottoms-up forecast isn't reconciling. Can you align with your regional managers and bring a revised number to the next exec review?

Marcus: I'll set up alignment sessions this week and have a revised number in two weeks.

Priya: I'll make sure the updated numbers are reflected in the master plan once I hear back from both of you.
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
def run_interactive(system_prompt: str, client: anthropic.Anthropic, output_file: str) -> None:
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
    items = extract_action_items(meeting_type, attendees, transcript, system_prompt, client)
    output = format_action_items("Interactive Session", items)
    print(output)
    save_output(output, output_file)


# ── File Output ────────────────────────────────────────────────────────────────
def save_output(content: str, filepath: str) -> None:
    """Append formatted output to the results file."""
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(content)
    print(f"  [Saved to {filepath}]")


# ── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    # ── Argument Parser ────────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(
        description="SIOP Meeting Action Item Extractor"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run all 5 evaluation cases automatically"
    )
    parser.add_argument(
        "--system-prompt",
        type=str,
        default=None,
        help="Path to a .txt file containing a custom system prompt"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT_FILE,
        help=f"File to save results to (default: {DEFAULT_OUTPUT_FILE})"
    )
    args = parser.parse_args()

    # ── API Key Check ──────────────────────────────────────────────────────────
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n[ERROR] ANTHROPIC_API_KEY environment variable is not set.")
        print("  Set it with: set ANTHROPIC_API_KEY=your-key-here  (Windows CMD)")
        print("  Get a key at: https://console.anthropic.com\n")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # ── Load System Prompt ─────────────────────────────────────────────────────
    if args.system_prompt:
        with open(args.system_prompt, "r", encoding="utf-8") as f:
            system_prompt = f.read().strip()
        print(f"\n[INFO] Using custom system prompt from: {args.system_prompt}")
    else:
        system_prompt = DEFAULT_SYSTEM_PROMPT

    # ── Clear output file for a fresh run ─────────────────────────────────────
    if args.demo:
        open(args.output, "w").close()

    # ── Demo or Interactive ────────────────────────────────────────────────────
    if args.demo:
        print(f"\n[INFO] Model      : {MODEL_NAME}")
        print(f"[INFO] Temperature: {TEMPERATURE} (reproducible)")
        print(f"[INFO] Output file: {args.output}")

        for i, case in enumerate(SAMPLE_CASES):
            items = extract_action_items(
                case["meeting_type"],
                case["attendees"],
                case["transcript"],
                system_prompt,
                client,
            )
            output = format_action_items(case["label"], items)
            print(output)
            save_output(output, args.output)

            if i < len(SAMPLE_CASES) - 1:
                print(f"  Waiting {DELAY_SECS}s before next case...")
                time.sleep(DELAY_SECS)

        print(f"\n[DONE] All cases complete. Results saved to: {args.output}\n")
    else:
        run_interactive(system_prompt, client, args.output)
