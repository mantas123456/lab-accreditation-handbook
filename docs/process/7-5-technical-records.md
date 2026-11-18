---
clause: "7.5"
description: What technical records a lab must keep so any result can be traced and repeated, with a worked record trail for one moisture result.
---

# 7.5 Technical records

## In one sentence

Keep enough information about each test that someone else could see how the
result was obtained, and if possible repeat the test under conditions as
close to the original as possible. Record every change so the original can
still be read.

## What an assessor looks for

An assessor will pick a report, often an old one, and ask you to show
everything behind it. They expect to find:

- **The original observations and data**, recorded at the time the work was
  done, not copied up later.
- **Calculations and data transfers** that can be checked.
- **Who did what and when**: who tested, who checked the data, who
  approved the report, with dates.
- **Which equipment, reference materials, reagents and method version**
  were used, so the conditions can be reconstructed.
- **Environmental conditions**, where they affect the result.
- **QC results** for the run ([7.7](7-7-validity-of-results.md)).
- **Amendments that leave the original readable**, with the date, the
  person and the reason. In electronic systems, an audit trail.

## How to do it in a small lab

1. **Design worksheets around the method.** Each method gets a worksheet
   (paper or electronic) with fields for the raw readings, the equipment
   IDs, the reference material or control sample lot, the analyst and the
   date. If a field is on the sheet, people fill it in.
2. **Record raw data, not results.** Write the three weighings, not just
   the moisture percentage. Keep instrument printouts or export files.
3. **Link everything by lab number and date.** The worksheet points to the
   balance ID; the balance's records ([6.4](../resources/6-4-equipment.md))
   show it was in calibration on that day.
4. **Correct the right way.** On paper: one line through the old value so
   it can still be read, the new value next to it, initials, date and
   reason. Never correction fluid, never overwriting. In software: changes
   logged automatically with user, time, old value and reason
   ([7.11](7-11-data-management.md)).
5. **Check before reporting.** A second person checks transcriptions and
   calculations, at least for a sample of results, and signs or logs it.
6. **Keep records for the defined period** (often the accreditation cycle,
   or longer if the customer or law requires it) in a way that protects
   them and lets you find them ([8.4](../management/8-4-records.md)).

## Worked example

An assessor picks report 26-0412 from a made-up biofuel lab and asks to see
how the moisture result of 7.74 % was produced.

| Step | Record | Where it is |
|---|---|---|
| Receipt | Sample log entry with condition and photo | LIMS, sample 26-0412 |
| Test | Worksheet MO-02 rev. 3: tray IDs, three weighings for each duplicate, oven ID, oven-in and oven-out times, analyst, date | Paper worksheet, scanned to job file |
| Equipment | Balance B-03 calibration certificate and daily check record; oven O-01 temperature log | Equipment files |
| QC | Control sample result for the run, plotted on the moisture chart | QC chart, run 10 |
| Calculation | Results calculated in the validated moisture spreadsheet v2.1 | Job file |
| Check | Second analyst checked transcription and calculation | Initials and date on worksheet |
| Correction | One weighing changed from 312.46 to 312.64 g: crossed through, initialled and dated, reason "transposed digits, checked against balance printout" | Worksheet |
| Approval | Report authorised by the technical manager | LIMS audit trail |

From these records, the assessor can recalculate the result, see that the
balance and oven were in control, and follow the correction.

## Common findings

- **Results recorded without raw data**, or raw data on loose paper that was
  thrown away after entry.
- **Corrections that hide the original**: overwriting, correction fluid,
  rewritten clean copies.
- **No link to equipment**, so it cannot be shown which balance or oven was
  used.
- **No record of who checked or authorised** the result.
- **Electronic records changed without an audit trail**, for example
  spreadsheets saved over.
- **Records that cannot be found** within a reasonable time.

## Templates

No template is planned for this clause; method worksheets are specific to
each lab. The SOP template (version 0.4) includes a worksheet section.

## Tools

No calculation is needed for this clause.

## Related clauses

- [8.4 Records](../management/8-4-records.md): retention, protection and
  access for all records.
- [7.11 Data management](7-11-data-management.md): electronic records and
  audit trails.
- [7.8 Reporting](7-8-reporting.md): the report the records support.
