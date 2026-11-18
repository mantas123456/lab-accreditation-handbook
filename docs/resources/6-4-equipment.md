---
clause: "6.4"
description: How a lab controls its equipment, from acceptance and calibration to intermediate checks, labels, records and taking items out of service, with a worked balance example.
---

# 6.4 Equipment

## In one sentence

Have the equipment each method needs, prove it is good enough before you
use it, calibrate what affects your results, check it between
calibrations, know its status at a glance, and stop using it as soon as you
doubt it.

## What an assessor looks for

- **Equipment that fits the methods**: instruments, software, measurement
  standards, reference materials, reagents and consumables that can reach
  the accuracy and uncertainty the method needs.
- **Checks before first use** (and after repair or return from outside the
  lab) that the equipment meets the requirements.
- **A calibration programme** for every item whose accuracy or uncertainty
  affects results, or which is needed for traceability
  ([6.5](6-5-traceability.md)). Reviewed and adjusted when needed.
- **Intermediate checks** between calibrations where needed to keep
  confidence in the equipment.
- **Status visible**: labels or another clear way to see calibration
  status and the next due date.
- **Out-of-service rules**: equipment that is faulty, overloaded, mishandled
  or giving doubtful results is taken out of use, labelled and isolated,
  and the effect on past results is checked.
- **Records for each important item**: identity, maker and model, serial
  number, location, calibration and check results with acceptance criteria
  and due dates, reference material documents, maintenance plan and
  history, damage and repairs.
- **Correction factors** from calibrations applied and kept up to date.
- **Protection against adjustments** that would invalidate results.

## How to do it in a small lab

1. **Keep an equipment register**: one row per important item, with an ID
   you also use on labels, worksheets and records.
2. **Accept equipment formally.** Before use, check it against what the
   method needs (range, resolution, accuracy) and record the check.
3. **Decide what needs calibration** and how often. Base the interval on
   the maker's advice, how much the item is used, how stable it has been,
   and how critical it is. Lengthen or shorten it based on history.
4. **Read every calibration certificate.** Do not just file it. Check the
   results against your acceptance criteria (is the error and its
   uncertainty small enough for your method?), and apply corrections if
   needed.
5. **Plan intermediate checks**: a daily check weight on the balance, a
   weekly reference material burn on the calorimeter, a monthly
   thermometer check in the oven. Plot the results so drift shows
   ([7.7](../process/7-7-validity-of-results.md)).
6. **Label status** on the item: ID, calibration date, next due date, and a
   clear "Out of service" label when needed.
7. **When in doubt, take it out.** Label it, stop using it, and look back
   at results since the last good check
   ([7.10](../process/7-10-nonconforming-work.md)).

## Worked example

A made-up biofuel lab's analytical balance B-03:

**Register entry.** B-03; maker and model; serial number; balance room;
range 0–220 g, readability 0.1 mg; used for ash, moisture of the analysis
sample and calorific value; calibrated yearly by an accredited calibration
lab; daily check with a 200 g check weight; maintenance: cleaned weekly.

**Acceptance criteria**, set by the technical manager from the methods:

| Check | Criterion |
|---|---|
| Calibration: error at each test point, plus its expanded uncertainty | Within ±0.5 mg up to 200 g |
| Daily check: 200 g check weight | Within ±0.3 mg of its calibrated value |
| Level bubble centred | Before each use |

**Calibration review.** The new certificate shows an error of +0.2 mg at
200 g with U = 0.1 mg. Total 0.3 mg is within ±0.5 mg. The technical
manager signs the certificate as reviewed and the label is updated.

**Doubtful result.** One morning the daily check reads +0.6 mg. A repeat
reads +0.5 mg. The analyst labels B-03 "Out of service" and uses the second
balance. A service engineer finds a draught from a newly installed air
conditioning vent. The vent is redirected; three checks pass; the
technical manager returns B-03 to service. Results since the previous good
check (one day) are assessed: the possible error is far below the
uncertainty of the ash and moisture results, so no action on reports is
needed. Everything is recorded in B-03's history.

## Common findings

- **Certificates filed but never reviewed** against acceptance criteria.
- **No acceptance criteria** at all for calibrations or checks.
- **Calibration intervals not justified**, or overdue items still in use.
- **Intermediate checks done but not trended**, so slow drift is missed.
- **Faulty equipment not labelled**, and no look back at results.
- **Reference materials and reagents past their expiry date.**
- **Equipment records incomplete**: no serial number, no location, no
  repair history.

## Templates

The equipment register and calibration schedule arrive in version 0.4.

## Tools

- [`labqc.control_charts.westgard`](https://mantas123456.github.io/lab-quality-toolkit/api/control_charts/#labqc.control_charts.westgard):
  apply control-chart rules to intermediate check results, so a slow drift
  shows before a check fails.
- [The labqc web app, QC charts page](https://lab-quality-toolkit-3go33hyzzwjhwpktn8tles.streamlit.app/QC_charts).

## Related clauses

- [6.5 Traceability](6-5-traceability.md): calibrations that link results
  to SI units.
- [7.7 Validity of results](../process/7-7-validity-of-results.md):
  intermediate checks are part of monitoring.
- [7.11 Data management](../process/7-11-data-management.md): instrument
  software is equipment too.
