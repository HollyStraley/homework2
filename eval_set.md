# Evaluation Set

**Business Workflow:** Summarizing SIOP meetings into structured action items
**User:** SIOP Master Scheduler

---

## Evaluation Criteria
1. **Completeness** — All action items mentioned in the transcript are captured
2. **Accuracy** — Owner, requester, priority, and context are correctly assigned
3. **Clarity** — Action text is concise, specific, and actionable
4. **Structure** — Output follows the required format (Action ID, Action Text, Owner, Requester, Priority, Context)
5. **No Hallucination** — No action items, owners, or details are invented that were not in the transcript

---

## Test Cases

---

### Case 1 — Normal: Standard Demand Review Meeting
**Type:** Normal Case
**Meeting Type:** Demand Review
**Attendees:** Sarah Lin (Demand Planner), Marcus Webb (Sales Director), Priya Nair (SIOP Master Scheduler), Tom Reyes (Finance Lead)

**Input Transcript:**
```
Priya: Alright, let's get started with the demand review. Sarah, can you walk us through the latest numbers?

Sarah: Sure. We're seeing a 12% spike in demand for Product Line A in Q3, mostly driven by the new retail partnership Marcus's team signed last month. I need Marcus to get me the confirmed order volumes from that account by end of week so I can update the forecast.

Marcus: Absolutely, I'll have those to you by Friday.

Priya: Great. Tom, given that demand increase, can you flag whether the Q3 budget can absorb any additional procurement costs?

Tom: Yes, I'll run the numbers and send a budget impact summary to Priya and Sarah by next Wednesday.

Priya: Perfect. Sarah, anything else?

Sarah: One more thing — we need to decide if we're going to adjust the safety stock policy for Product Line A given the new demand signal. Priya, can you draft a proposal for the team to review before the next cycle?

Priya: I'll have a draft ready in two weeks.
```

**Expected Output:**
```
| Action ID | Action Text                                                                 | Owner       | Requester | Priority | Context                                                                 |
|-----------|-----------------------------------------------------------------------------|-------------|-----------|----------|-------------------------------------------------------------------------|
| ACT-001   | Provide confirmed order volumes from new retail account to Sarah            | Marcus Webb | Sarah Lin | High     | 12% Q3 demand spike driven by new retail partnership; needed for forecast update |
| ACT-002   | Run budget impact analysis for additional Q3 procurement costs              | Tom Reyes   | Priya Nair | Medium  | Q3 demand increase for Product Line A may require additional procurement spend |
| ACT-003   | Draft safety stock policy adjustment proposal for Product Line A            | Priya Nair  | Sarah Lin | Medium   | New demand signal warrants review of current safety stock levels before next SIOP cycle |
```

**Actual Output:**

| Action ID | Owner | Requester | Priority | Context Summary |
|-----------|-------|-----------|----------|-----------------|
| ACT-001   | Marcus Webb | Sarah Lin | High | Needed by end of week to update demand forecast for Product Line A, which is experiencing a 12% Q3 spike |
| ACT-002   | Tom Reyes | Priya Nair | High | 12% demand increase may require additional procurement spending; budget impact must be assessed |
| ACT-003   | Priya Nair | Sarah Lin | Medium | Revised safety stock policy needed to align inventory strategy with increased demand volatility before next cycle |

**Score:** [ /5]

---

### Case 2 — Normal: Supply Review with Multiple Owners
**Type:** Normal Case
**Meeting Type:** Supply Review
**Attendees:** James Okafor (Supply Planner), Dana Cho (Procurement Manager), Priya Nair (SIOP Master Scheduler), Luis Ortega (Warehouse Ops Lead)

**Input Transcript:**
```
Priya: Let's go through supply constraints for the next two cycles. James, what are we looking at?

James: We have a capacity constraint at the Chicago DC — we're at 94% utilization and expecting more inbound from the East Coast supplier next month. Luis, we need you to identify overflow storage options by the 15th.

Luis: Understood, I'll look into third-party storage options and get back to you.

James: Also, Dana, we had a lead time increase from Supplier 47 — they moved from 6 to 9 weeks. Can you get on a call with them this week and push back? We need that resolved before the next demand cycle.

Dana: I'll reach out to them today and aim to have an answer by Thursday.

Priya: Great. And James, please update the supply plan in the system to reflect the new lead times so we're not planning on stale data.

James: Will do, I'll update it by EOD tomorrow.
```

**Expected Output:**
```
| Action ID | Action Text                                                                 | Owner          | Requester   | Priority | Context                                                                        |
|-----------|-----------------------------------------------------------------------------|----------------|-------------|----------|--------------------------------------------------------------------------------|
| ACT-001   | Identify overflow storage options for Chicago DC                            | Luis Ortega    | James Okafor | High    | Chicago DC at 94% utilization with additional inbound expected next month       |
| ACT-002   | Contact Supplier 47 to negotiate lead time back to 6 weeks                  | Dana Cho       | James Okafor | High    | Lead time increased from 6 to 9 weeks; must resolve before next demand cycle    |
| ACT-003   | Update supply plan in system to reflect Supplier 47 new lead times          | James Okafor   | Priya Nair  | High     | Current plan based on stale 6-week lead time; update needed by EOD tomorrow     |
```

**Actual Output:**

| Action ID | Owner | Requester | Priority | Context Summary |
|-----------|-------|-----------|----------|-----------------|
| ACT-001   |       |           |          |                 |
| ACT-002   |       |           |          |                 |
| ACT-003   |       |           |          |                 |

**Score:** [ /5]

---

### Case 3 — Normal: Executive S&OP Meeting
**Type:** Normal Case
**Meeting Type:** Executive S&OP
**Attendees:** Carol Simmons (VP Supply Chain), David Park (CFO), Priya Nair (SIOP Master Scheduler), Marcus Webb (Sales Director)

**Input Transcript:**
```
Carol: The consensus plan shows a gap of 8,000 units in Q4 that we haven't resolved. David, we need a decision on whether to approve emergency procurement funding — can you get that approved or denied by end of month?

David: Yes, I'll take it to the exec committee this Thursday and confirm by Friday.

Carol: Marcus, we also need a realistic top-down number from Sales leadership for Q4 — the bottoms-up forecast isn't reconciling. Can you align with your regional managers and bring a revised number to the next exec review?

Marcus: I'll set up alignment sessions this week and have a revised number in two weeks.

Priya: I'll make sure the updated numbers are reflected in the master plan once I hear back from both of you.
```

**Expected Output:**
```
| Action ID | Action Text                                                                 | Owner          | Requester      | Priority | Context                                                                              |
|-----------|-----------------------------------------------------------------------------|----------------|----------------|----------|--------------------------------------------------------------------------------------|
| ACT-001   | Get exec committee approval or denial on emergency procurement funding       | David Park     | Carol Simmons  | High     | 8,000-unit Q4 gap unresolved; funding decision needed to close gap                   |
| ACT-002   | Align with regional managers and submit revised Q4 top-down Sales forecast   | Marcus Webb    | Carol Simmons  | High     | Bottoms-up forecast not reconciling with top-down; needed for next exec review       |
| ACT-003   | Update master plan once funding decision and revised forecast are received    | Priya Nair     | Carol Simmons  | Medium   | Master plan must reflect latest financial and sales inputs before next SIOP cycle    |
```

**Actual Output:**

| Action ID | Owner | Requester | Priority | Context Summary |
|-----------|-------|-----------|----------|-----------------|
| ACT-001   |       |           |          |                 |
| ACT-002   |       |           |          |                 |
| ACT-003   |       |           |          |                 |

**Score:** [ /5]

---

### Case 4 — Edge Case: Meeting with No Explicit Action Items
**Type:** Edge Case
**Meeting Type:** Demand Review
**Attendees:** Sarah Lin (Demand Planner), Priya Nair (SIOP Master Scheduler), Tom Reyes (Finance Lead)

**Input Transcript:**
```
Priya: Let's do a quick check-in on the demand picture for Q2.

Sarah: Looks pretty stable. Forecast is in line with last cycle — no major changes. Product Lines B and C are tracking to plan.

Tom: Financials align with what we reviewed last week. Nothing new to flag.

Priya: Great. Sounds like we're in a good place. Let's reconvene next cycle unless something changes.
```

**Expected Output:**
```
No action items identified in this meeting. The demand outlook for Q2 is stable, with Product Lines B and C tracking to plan and financials aligned. No follow-ups required at this time.
```

**Actual Output:**

No action items identified in this meeting. ✅

**Notes:** The model should gracefully return a "no action items" response rather than hallucinating tasks or forcing a table with empty fields.
**Score:** [ /5]

---

### Case 5 — Likely to Fail: Ambiguous Ownership and Implied Actions
**Type:** Likely to Fail
**Meeting Type:** Supply Review
**Attendees:** James Okafor (Supply Planner), Dana Cho (Procurement Manager), Priya Nair (SIOP Master Scheduler), Rachel Moore (Logistics Coordinator)

**Input Transcript:**
```
Priya: We really need to get on top of the inbound shipment delays. It's been a recurring issue.

James: Yeah, someone should probably look into the root cause with the carrier. It's been three weeks.

Dana: Procurement has been trying to get answers too. I feel like logistics needs to own that conversation.

Rachel: I mean, we've reached out but haven't heard back. Maybe procurement should escalate?

Dana: We could, but honestly it might carry more weight coming from supply planning.

James: Either way, we need a decision on whether to activate the secondary carrier. That's been sitting for a while.

Priya: Right, let's not let that slip again. Someone needs to own that.

Rachel: Agreed. We also need to update the inbound tracking board but I'm not sure who has access to do that.

Priya: Okay, we'll figure it out offline. Let's move on.
```

**Expected Output:**
```
| Action ID | Action Text                                                                  | Owner             | Requester   | Priority | Context                                                                               |
|-----------|------------------------------------------------------------------------------|-------------------|-------------|----------|---------------------------------------------------------------------------------------|
| ACT-001   | Escalate inbound shipment delay root cause investigation with carrier         | TBD (Dana Cho or Rachel Moore) | Priya Nair | High | Three-week recurring delay; ownership disputed between Procurement and Logistics      |
| ACT-002   | Make decision on activating secondary carrier                                 | TBD (James Okafor or Priya Nair) | James Okafor | High | Decision has been pending; delays in activation risk further supply disruption       |
| ACT-003   | Update inbound tracking board                                                 | TBD (access unclear) | Rachel Moore | Low    | Tracking board out of date; access needs to be confirmed before task can be assigned  |
```

**Actual Output:**

| Action ID | Owner | Requester | Priority | Context Summary |
|-----------|-------|-----------|----------|-----------------|
| ACT-001   | James Okafor ⚠️ | Priya Nair | High | Delays recurring for three weeks; root cause investigation essential to resolving supply chain issue |
| ACT-002   | TBD | James Okafor | High | Decision pending for extended period; needed to mitigate ongoing inbound delays and ensure supply continuity |
| ACT-003   | TBD | Rachel Moore | Medium | Tracking board needs to be current for inbound visibility; access and ownership need clarification |

**Notes:** This is a likely failure case because ownership is never clearly assigned — the model may confidently assign a wrong owner, omit action items entirely, or fail to flag ambiguity. The ideal output acknowledges the ambiguity rather than fabricating definitive owners.
**Score:** [ /5]

---

## Summary

| Case | Type              | Description                                      | Score | Notes |
|------|-------------------|--------------------------------------------------|-------|-------|
| 1    | Normal            | Standard demand review with clear action items   |       |       |
| 2    | Normal            | Supply review with multiple owners               |       |       |
| 3    | Normal            | Executive S&OP with high-stakes decisions        |       |       |
| 4    | Edge Case         | Meeting with no action items                     |       |       |
| 5    | Likely to Fail    | Ambiguous ownership and implied actions          |       |       |
