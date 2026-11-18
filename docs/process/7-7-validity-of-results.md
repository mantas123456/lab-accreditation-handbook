---
clause: "7.7"
description: How a lab plans and runs internal quality control and proficiency testing, with a worked control-chart example for moisture in wood pellets.
---

# 7.7 Ensuring the validity of results

## In one sentence

Check your results all the time, in a planned way, both inside the lab and
against other labs, and act as soon as the checks say a result may be wrong.

## What an assessor looks for

- **A monitoring plan for each method**: which checks you run, how often,
  and what counts as a pass. Typical internal checks are control samples,
  certified or in-house reference materials, blanks, duplicates, retests of
  retained samples, intermediate checks on equipment, and comparing results
  for related properties of the same sample.
- **External checks**: a plan for proficiency testing (PT) or
  interlaboratory comparisons that covers your whole scope over the
  accreditation cycle. Your accreditation body will have a PT policy that
  sets the minimum; read it.
- **Evidence the data is used, not just stored.** Control charts that are
  plotted before results go out, reviewed for trends, and signed or
  otherwise recorded as reviewed.
- **Action when a check fails.** Results held back, the cause found, the
  effect on reported results assessed, and a nonconformity raised where
  needed (see [7.10](7-10-nonconforming-work.md)).
- **Follow-up of every questionable or unsatisfactory PT result**, with a
  root cause, not only "random error".

## How to do it in a small lab

1. **Choose internal checks per method.** A sensible starting point for a
   routine test: one control sample in every batch, a duplicate on one
   sample in ten, a blank where it applies, and a certified reference
   material a few times a year to check bias.
2. **Make a control sample.** Take a homogeneous batch of a real sample
   type, split it into portions and store them so they do not change
   (airtight, cool, dark, as the property needs). Check stability by
   testing it over time.
3. **Set limits from your own data.** Test the control sample about 20
   times over several weeks, with different analysts and days, so the
   spread includes normal day-to-day variation. The mean is the centre
   line; ±2 SD are warning limits and ±3 SD are action limits. Do not use
   a manufacturer's specification or a method's precision figure as your
   limits.
4. **Write the rules down.** In the method SOP, say which control-chart
   rules mean "warning" and which mean "stop and investigate". Westgard
   rules are a common set (see the table below).
5. **Plot before you release.** The analyst plots the control result
   before the batch results leave the lab. A rejected run means the batch
   is held.
6. **Review the chart regularly.** Once a month, look for slow drifts and
   shifts that single points do not show. Record the review.
7. **Recalculate limits on purpose, not by habit.** Do it once a year or
   after a known change (new control batch, new instrument), and record
   why. Recalculating every month lets a drift slowly become the new
   normal.
8. **Plan PT.** List every method in scope, find a PT scheme for each, and
   set a frequency based on risk: more often for high-volume or
   high-consequence tests, at least once per accreditation cycle for every
   method. Where no scheme exists, arrange a comparison with another lab.
9. **Track PT scores over time.** Treat |z| between 2 and 3 as a warning to
   investigate and |z| of 3 or more as a nonconformity. Several z-scores of
   the same sign, even small ones, point to a bias worth a look.

| Rule | Meaning | Usual action |
|---|---|---|
| 1<sub>2s</sub> | One result beyond ±2 SD | Warning: check the other rules |
| 1<sub>3s</sub> | One result beyond ±3 SD | Reject: likely random error or a gross mistake |
| 2<sub>2s</sub> | Two results in a row beyond 2 SD on the same side | Reject: systematic error |
| R<sub>4s</sub> | One result above +2 SD and the next below −2 SD | Reject: random error |
| 4<sub>1s</sub> | Four results in a row beyond 1 SD on the same side | Reject: systematic shift |
| 10<sub>x</sub> | Ten results in a row on the same side of the centre | Reject: drift or shift |

## Worked example

The made-up solid biofuel lab from [7.6](7-6-measurement-uncertainty.md)
keeps a control sample of wood pellets for its moisture test. It ran the
control sample 20 times over four weeks to set limits:

| | Moisture, % |
|---|---|
| Centre line (mean) | 8.19 |
| Standard deviation | 0.10 |
| Warning limits (±2 SD) | 7.98 to 8.40 |
| Action limits (±3 SD) | 7.88 to 8.50 |

The next 13 runs:

| Run | Result, % | z | Rules broken | Status |
|---|---|---|---|---|
| 1 | 8.15 | −0.39 | – | accept |
| 2 | 8.27 | 0.76 | – | accept |
| 3 | 8.09 | −0.97 | – | accept |
| 4 | 8.24 | 0.47 | – | accept |
| 5 | 8.31 | 1.14 | – | accept |
| 6 | 8.33 | 1.33 | – | accept |
| 7 | 8.32 | 1.24 | – | accept |
| **8** | **8.36** | **1.62** | **4<sub>1s</sub>** | **reject** |
| 9 | 8.18 | −0.11 | – | accept |
| 10 | 8.22 | 0.28 | – | accept |
| 11 | 8.12 | −0.68 | – | accept |
| **12** | **8.42** | **2.19** | **1<sub>2s</sub>** | **warning** |
| 13 | 8.20 | 0.09 | – | accept |

**Run 8.** No single result was outside the warning limits, so a quick look
at the chart would miss it. But runs 5 to 8 were all more than 1 SD above
the centre line: a systematic shift. The lab held the batch and
investigated:

- A check with a calibrated thermometer showed the oven shelf used for the
  samples was at 108 °C instead of 105 °C. At the higher temperature some
  volatile compounds leave the pellets with the water, so results read high.
- The oven was adjusted and checked again; run 9 was back near the centre.
- **Effect on results already reported.** The shift was about +0.15 %,
  smaller than the expanded uncertainty of 0.25 %. The lab retested the
  retained portions from the batches of runs 5 to 8. None of the results
  changed a pass/fail statement, so no customer needed a corrected report.
  The lab recorded all of this as a nonconformity
  ([7.10](7-10-nonconforming-work.md)) and added a monthly oven
  temperature check to its equipment plan ([6.4](../resources/6-4-equipment.md)).

**Run 12.** One result just above +2 SD with no other rule broken: a
warning. The analyst checked the other rules, released the batch and noted
it on the chart. One warning in about 20 runs is what you expect by chance.

**PT round.** In the same quarter the lab took part in a PT round for
moisture in pellets. Its result was 7.95 %, the assigned value 7.80 %, and
the standard deviation for proficiency assessment 0.20 %:

\[
z = \frac{7.95 - 7.80}{0.20} = 0.75
\]

That is satisfactory (|z| ≤ 2). The lab adds it to its PT history, which
also feeds the bias term in its uncertainty budget.

**The same checks in labqc**

```python
from labqc.control_charts import limits_from_data, westgard
from labqc.proficiency import z_score, classify

baseline = [8.21, 8.05, 8.33, 8.17, 8.28, 8.02, 8.24, 8.11, 8.36, 8.19,
            8.30, 8.08, 8.20, 8.13, 8.27, 8.04, 8.25, 8.15, 8.34, 8.10]
limits = limits_from_data(baseline)          # centre 8.19, SD 0.10

runs = [8.15, 8.27, 8.09, 8.24, 8.31, 8.33, 8.32, 8.36,
        8.18, 8.22, 8.12, 8.42, 8.20]
print(westgard(runs, limits))                # run 8: 4_1s reject; run 12: warning

z = z_score(7.95, assigned=7.80, sigma_pt=0.20)
print(z, classify(z))                        # 0.75 satisfactory
```

## Common findings

- **QC data recorded but never reviewed.** Charts exist, but nobody looked
  for trends, and there is no record of a review.
- **Results released after a failed control**, with no record of why.
- **Limits that are not the lab's own**: taken from a kit insert or a
  method's precision data, or recalculated so often that a drift became
  the centre line.
- **A PT plan that leaves gaps**: methods in scope with no PT or comparison
  in the cycle, or no plan at all, only a list of past rounds.
- **Questionable PT results not followed up**, or closed as "random error"
  without any investigation.
- **No evidence the control sample is stable** over the period it is used.
- **No link to reported results.** When a check fails, the lab fixes the
  instrument but does not ask which reported results were affected.

## Templates

<!-- templates -->

## Tools

- [`labqc.control_charts.westgard`](https://mantas123456.github.io/lab-quality-toolkit/api/control_charts/#labqc.control_charts.westgard):
  flags each run with the rules it breaks.
- [`labqc.control_charts.limits_from_data`](https://mantas123456.github.io/lab-quality-toolkit/api/control_charts/#labqc.control_charts.limits_from_data):
  sets the centre line and SD from a baseline.
- [`labqc.proficiency.z_score`](https://mantas123456.github.io/lab-quality-toolkit/api/proficiency/)
  and `pt_history`: score PT rounds and track them over time.
- The labqc web app has [QC charts](https://lab-quality-toolkit-3go33hyzzwjhwpktn8tles.streamlit.app/QC_charts)
  and [Proficiency testing](https://lab-quality-toolkit-3go33hyzzwjhwpktn8tles.streamlit.app/Proficiency_testing)
  pages that do the same in the browser.

## Related clauses

- [7.6 Measurement uncertainty](7-6-measurement-uncertainty.md): QC and PT
  data check the budget and feed it.
- [7.10 Nonconforming work](7-10-nonconforming-work.md): what to do with
  results produced while a check was failing.
- [6.4 Equipment](../resources/6-4-equipment.md): intermediate checks on
  equipment between calibrations.
- [7.2 Methods](7-2-methods.md): validation data is the starting point for
  QC limits.
