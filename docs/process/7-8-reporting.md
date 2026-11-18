---
clause: "7.8"
description: What a lab report must contain, how to state conformity with a decision rule, and how to amend a report, with a worked boiler emissions example.
---

# 7.8 Reporting results

## In one sentence

Give the customer results that are accurate, clear and complete enough to
use correctly. When you say "pass" or "fail", base it on a decision rule
agreed beforehand, and never change an issued report without a traceable
amendment.

## What an assessor looks for

- **Reports reviewed and authorised** before release, by someone
  authorised to do so.
- **The information a reader needs**, normally:
    - a title, the lab's name and address, and where the work was done;
    - a unique report number on every page, page numbering ("page 2 of 4")
      and a clear end of report;
    - the customer, the method used, a description and identification of
      the item, and the dates of receipt, sampling and testing;
    - results with units and, where relevant, measurement uncertainty;
    - who authorised the report;
    - a statement when the results apply only to the item as received;
    - any deviation, addition or exclusion from the method, and anything
      unusual about the item ([7.4](7-4-item-handling.md));
    - clearly marked results from subcontractors.
- **Sampling information**, when the lab sampled ([7.3](7-3-sampling.md)).
- **Uncertainty reported** when the customer asks for it, when it affects
  whether a result meets a limit, or when the method requires it.
- **Statements of conformity** that name the specification and the decision
  rule used, with the rule agreed at contract review
  ([7.1](7-1-contract-review.md)).
- **Opinions and interpretations** clearly marked as such, given by
  authorised staff, with the basis recorded.
- **Amended reports** that are clearly identified, give the reason for the
  change, and refer to the report they replace.

## Decision rules

A decision rule says how uncertainty is taken into account when you state
whether a result meets a limit. Two common rules for an upper limit:

| Rule | Pass when | Risk carried by |
|---|---|---|
| **Simple acceptance** (shared risk) | result ≤ limit | Shared: up to about 50 % chance a result just below the limit is really above it |
| **Guarded acceptance** | result ≤ limit − *U* | Mostly the producer: a pass is clear, but some good items will not pass |

With guarded acceptance, a result between (limit − *U*) and the limit is
neither a clear pass nor a clear fail. The report must say what that means,
as agreed with the customer. ILAC G8 is the usual guidance document on
decision rules; your accreditation body may have its own policy.

## How to do it in a small lab

1. **Build one report template per kind of work**, with every field above,
   so nothing depends on memory.
2. **Report what was measured.** Units, the basis (as received or dry),
   reference conditions, and a sensible number of significant figures, in
   line with the uncertainty.
3. **Agree the decision rule at contract review**, write it on the report,
   and apply it the same way every time.
4. **Review before release.** A second person checks results against the
   records ([7.5](7-5-technical-records.md)) and authorises the report.
5. **Amend, never overwrite.** Issue a new report number, mark it
   "Replaces report X", state what changed and why, and keep both.

## Worked example

A made-up lab tests two pellet boilers for carbon monoxide (CO). The emission
limit the customer works to is 500 mg/m³ (dry flue gas, standard conditions,
10 % O<sub>2</sub>). The agreed decision rule is **guarded acceptance** with
the lab's expanded uncertainty (k = 2).

The analyser measures CO in ppm at the actual O<sub>2</sub> level. The lab
converts each result to mg/m³ and corrects it to 10 % O<sub>2</sub>:

\[
C_{\text{ref}} = C_{\text{meas}} \times \frac{20.9 - 10}{20.9 - O_{2,\text{meas}}}
\]

Uncertainty inputs: 4 % of reading for the CO measurement (standard
uncertainty, from validation), and 0.15 % O<sub>2</sub> for the oxygen
measurement.

| | Boiler A | Boiler B |
|---|---|---|
| CO measured | 300 ppm | 315 ppm |
| O<sub>2</sub> measured | 12.0 % | 12.0 % |
| CO, mg/m³ dry, standard conditions | 375 | 394 |
| Correction factor to 10 % O<sub>2</sub> | 1.225 | 1.225 |
| **CO at 10 % O<sub>2</sub>** | **459 mg/m³** | **482 mg/m³** |
| Expanded uncertainty *U* (k = 2) | 40 mg/m³ | 42 mg/m³ |
| Percentage of limit | 92 % | 96 % |
| Limit − *U* | 460 | 458 |
| Simple acceptance | Pass | Pass |
| **Guarded acceptance (agreed)** | **Pass** (459 ≤ 460) | **Not a clear pass** (482 > 458) |

**Report wording for boiler B:**

> CO at 10 % O<sub>2</sub>: 482 mg/m³ ± 42 mg/m³ (k = 2, about 95 %
> coverage). Limit 500 mg/m³. Decision rule: guarded acceptance, as agreed
> in contract 26-118. The result is below the limit, but the margin is
> smaller than the expanded uncertainty, so conformity cannot be confirmed
> with the agreed confidence.

The uncertainty budget shows 85 % of the variance comes from the CO
measurement and 15 % from the oxygen correction, so the lab knows where
to work if customers often land close to the limit.

**The same calculation in labqc**

```python
from labqc.emissions import correct_emission, corrected_uncertainty

for name, ppm in [("A", 300), ("B", 315)]:
    r = correct_emission(ppm, "CO", "ppm", o2_measured=12.0, o2_ref=10.0, limit=500)
    c_ref, unc = corrected_uncertainty(r.mg_m3_dry, 0.04 * r.mg_m3_dry, 12.0, 0.15, k=2)
    guarded_pass = c_ref <= 500 - unc.expanded
    print(name, round(c_ref), round(unc.expanded), guarded_pass)
# A 459 40 True
# B 482 42 False
```

## Common findings

- **Missing basic information**: no page numbering, no unique ID on every
  page, no method or date of testing.
- **"Pass" or "complies" without a stated specification or decision rule.**
- **Uncertainty left out** when a result is close to a limit.
- **Subcontracted results not marked**, or shown under the accreditation
  mark when the subcontractor's work is outside the lab's scope.
- **Opinions mixed with results**, without being marked as opinions.
- **Reports changed and re-sent under the same number**, with no record of
  what changed.
- **Too many digits**: results reported to four decimals with an
  uncertainty in the first.

## Templates

<!-- templates -->

## Tools

- [`labqc.emissions.correct_emission`](https://mantas123456.github.io/lab-quality-toolkit/api/emissions/#labqc.emissions.correct_emission):
  unit, water, temperature, pressure and O<sub>2</sub> corrections in one
  call, with percentage of limit.
- [`labqc.emissions.corrected_uncertainty`](https://mantas123456.github.io/lab-quality-toolkit/api/emissions/#labqc.emissions.corrected_uncertainty):
  uncertainty through the O<sub>2</sub> correction.
- [The labqc web app, Emissions page](https://lab-quality-toolkit-3go33hyzzwjhwpktn8tles.streamlit.app/Emissions).

## Related clauses

- [7.6 Measurement uncertainty](7-6-measurement-uncertainty.md): where *U*
  comes from.
- [7.1 Contract review](7-1-contract-review.md): where the decision rule is
  agreed.
- [7.5 Technical records](7-5-technical-records.md): every reported value
  must be traceable to the records.
