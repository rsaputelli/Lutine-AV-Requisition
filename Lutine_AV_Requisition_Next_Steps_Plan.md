Lutine AV Requisition App — Current State + Next Steps Plan (Restart Memo)
Current app location / structure

Local project folder:

C:\Users\RaySaputelli\NJAFP-Lutine Dropbox Dropbox\Ray Saputelli\LUTINE MANAGEMENT\7_Client Apps and Documentation\lutine-av-requisition

Current structure:

app.py

lib/supabase_client.py (standard client getter: get_supabase())

pages/01_AV_Intake.py

Supabase tables (existing)

Same Supabase project as Master Calendar app:

venues

av_requests

av_request_items

equipment_inventory (inventory CSV import completed earlier)

av_allocations (tracks assignment of specific equipment items to requests)

Intake workflow status (working)

✅ AV Intake supports:

Event optional (standalone AV requests supported)

Venue required

Inline venue creation

New venue creation auto-selects venue + pre-fills ship-to address

Submit creates:

av_requests record with correct venue_id

associated rows in av_request_items

✅ Shipping address logic (stable)

On new venue create:

st.session_state["selected_venue_id"] = new_venue_created["id"]

st.session_state["ship_to_address_prefill"] = _build_venue_ship_to_text(new_venue_created)

st.rerun()

If user selects an existing venue:

st.session_state.pop("ship_to_address_prefill", None) to avoid carryover

✅ Date fields (added + working)
av_requests schema now includes:

deliver_by_date (required)

event_start_date (optional)

event_end_date (optional)

UI now captures these fields and writes them into av_requests.

Key workflow clarification

Intake is done by the meetings team.

Allocation (assigning specific assets) is done by ops (Redeye / Ray).

Read access can be broad; write actions must be restricted.

Write restrictions required:

Only ops can assign/reassign specific equipment in av_allocations

(Everyone can view requests)

Execution Plan (best order for fastest adoption + low rework)
Phase 1 — Replace random email requests ASAP (1–2 sessions)
1) Email routing + confirmations (highest ROI)

On AV Request submit:

Route email to internal owner based on items:

laptops → Redeye tech support + cc Ray

owls/projectors → Ray

CC the meeting manager/requester on all confirmations (any direction)

Email includes:

meeting name / client / deliver-by date

venue + ship-to address

requested item quantities

request ID

link to view request detail (when available)

Goal: eliminate ad-hoc email requests by making the app send the “official” email automatically.

2) Add Request Detail page (read-only)

Create pages/02_AV_Request_Detail.py to display:

request header + status

venue + ship-to

deliver-by + optional event date range

requested item lines

assigned equipment list (if any)

This page becomes the “single source of truth” record for ops + meetings.

Phase 2 — Controlled edits (1 session)
3) Edit path (conservative)

Enable editing only the fields that realistically change:

deliver-by date

ship-to / recipient / hotel contact fields

special instructions

item quantities

On update:

send “Request updated” email to internal owner + cc meeting manager

keep logic minimal to avoid breaking stable intake

(Decision point later: whether meetings can edit after allocation or only ops.)

Phase 3 — Ops-only equipment assignment (asset-level tracking) (1–2 sessions)
4) Allocation UI (ops write actions only)

Create pages/03_AV_Allocation.py (ops workflow):

assign specific equipment_inventory items to a request via av_allocations

reassign equipment

mark equipment returned

This is critical for loss/theft/wipe scenarios:

identify “which device was where”

find last known request + ship-to

support remote wipe with serial/asset tag if needed

5) Enforce ops-only write permissions (UI + DB)

Do BOTH:

UI gating: hide allocation/return buttons unless user is ops

Supabase DB enforcement (real security):

enable RLS on av_allocations

policies: anyone can read, only ops can insert/update/delete

Phase 4 — Logistics tracking + nice-to-haves (after adoption)
6) Tracking + return notes

Add to av_requests (or later a dedicated table):

tracking_number

shipped_at

return_notes

Trigger emails on status changes; always CC meeting manager.

7) Inventory overlap warnings / shortage detection (optional)

Use:

deliver-by date

allocations
to flag equipment shortages / double-booking.

8) ICS / Calendar enrichment (cool later)

If request is linked to an existing event:

optionally update event description / ICS with AV notes
This is a later enhancement once workflow is stable.

Tomorrow’s restart objective (recommended)

Implement Phase 1 Step 1: Email Routing + CC meeting manager first, because that is the fastest way to replace random email requests and drive adoption.