---
clause: "7.2"
description: How a lab selects methods, verifies standard methods and validates its own, with a worked verification of the ash test in wood pellets.
---

# 7.2 Selecting, verifying and validating methods

## In one sentence

Use methods that suit the job, prove that you can get the method's
performance in your own lab before you use it, and fully validate any
method you wrote or changed yourself.

## What an assessor looks for

- **Up-to-date methods** that fit the customer's need, normally published
  standards in their current edition, available to the staff who use them.
- **Verification records for standard methods**: evidence that your lab
  reaches the performance the method states, before reporting results.
  Repeat it when the method's edition changes.
- **Validation records for everything else**: in-house methods, standard
  methods used outside their intended scope, and standard methods you
  changed. A validation plan made before the work, the data, and a
  conclusion that the method is fit for purpose.
- **Deviations from methods** that were justified, documented, technically
  sound, authorised and agreed with the customer.
- **Planned method development** by competent people, with records.

## Verification or validation?

| Situation | What you need |
|---|---|
| Published standard method, used as written, within its scope | **Verification**: show you can meet its stated performance |
| New edition of a standard you already use | Verification of what changed |
| Standard method used on a new matrix or range | **Validation** of the extended use |
| Standard method with your own changes | **Validation** of the changes |
| Method you developed, or took from a paper or an instrument manual | **Full validation** |

## How to do it in a small lab

1. **Pick the method with the customer** at contract review
   ([7.1](7-1-contract-review.md)). Default to the current edition of a
   recognised standard.
2. **Write a plan before collecting data.** State which performance
   characteristics you will check, how, with which materials, and what
   counts as acceptable. Acceptance criteria decided after you see the data
   are not convincing.
3. **Choose the characteristics that matter for the method.**
    - Almost always: precision (repeatability and intermediate precision)
      and trueness (bias).
    - For instrumental and trace methods: working range, linearity, limit of
      detection (LOD) and limit of quantification (LOQ).
    - For extraction or digestion methods: recovery.
    - For methods sensitive to conditions: robustness. Deliberately vary
      the oven temperature, the reagent batch or the analyst and see what
      changes.
    - Selectivity, where other substances could interfere.
4. **Design the experiments for real conditions.** Spread replicates over
   different days and analysts so the precision includes normal variation.
   Use a certified reference material (CRM) or a PT material with a known
   value to check bias.
5. **Compare with the criteria and conclude.** Write a short report:
   method, scope, data, results against criteria, conclusion, sign-off.
6. **Keep the data working for you.** The precision and bias you found are
   the starting point for your uncertainty budget
   ([7.6](7-6-measurement-uncertainty.md)) and your QC limits
   ([7.7](7-7-validity-of-results.md)).

## Worked example

A made-up biofuel lab adds the standard method for ash content of solid
biofuels (ashing at 550 °C) to its scope. It is a published standard used as
written, so the lab **verifies** it.

**Plan.** Precision from duplicate tests on an in-house pellet material on
five different days, by two analysts. Trueness from six tests on a biomass
CRM. Acceptance criteria, set before testing:

- the repeatability standard deviation is no larger than the one the method
  states;
- the bias against the CRM is within its expanded uncertainty
  (|bias| ≤ *U*<sub>bias</sub>).

**Precision data** (ash, % dry basis):

| Day | Result 1 | Result 2 |
|---|---|---|
| 1 | 0.48 | 0.50 |
| 2 | 0.52 | 0.51 |
| 3 | 0.47 | 0.49 |
| 4 | 0.50 | 0.53 |
| 5 | 0.51 | 0.49 |

A one-way analysis of variance by day gives:

| | Value |
|---|---|
| Mean | 0.500 % |
| Repeatability SD | 0.015 % |
| Between-day SD | 0.011 % |
| Intermediate precision SD | 0.019 % (3.7 % relative) |
| Day effect significant? | No (p = 0.21) |

**Trueness data.** Six results on a CRM certified at 1.20 % ash with
*U* = 0.03 % (k = 2): 1.21, 1.25, 1.19, 1.24, 1.22 and 1.26 %.

| | Value |
|---|---|
| Mean | 1.228 % |
| Bias | +0.028 % (recovery 102 %) |
| *U*<sub>bias</sub> = 2 × √(s²/n + u<sub>CRM</sub>²) | 0.037 % |
| Criterion: bias within ±*U*<sub>bias</sub> | **Met** |

!!! note "Why a t-test alone would mislead here"
    A simple t-test of the six results against 1.20 % gives p = 0.047,
    which looks like a significant bias. But that test ignores the
    uncertainty of the certified value itself. Once that is included, the
    bias is within what the CRM and the lab's precision can tell apart.
    The lab records the bias and keeps watching it through PT, rather than
    correcting results.

**Conclusion.** Both criteria are met. The method is verified for wood
pellets and the lab adds it to its scope. The intermediate precision SD
becomes the starting point for the ash QC chart and uncertainty budget.

**The same calculation in labqc**

```python
import pandas as pd
from labqc.validation import intermediate_precision, trueness

df = pd.DataFrame({
    "day":   [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
    "value": [0.48, 0.50, 0.52, 0.51, 0.47, 0.49, 0.50, 0.53, 0.51, 0.49],
})
ip = intermediate_precision(df)
print(ip.sd_repeatability, ip.sd_intermediate, ip.p_value)   # 0.015 0.019 0.21

t = trueness([1.21, 1.25, 1.19, 1.24, 1.22, 1.26], crm_value=1.20, crm_u=0.03 / 2)
print(t.bias, t.U_bias, t.passed)                            # 0.028 0.037 True
```

## Common findings

- **No verification** of standard methods, or a "verification" that is only
  a statement that the method is a standard.
- **Acceptance criteria written after the data**, or no criteria at all.
- **All replicates on one day by one analyst**, so the precision looks
  better than it is.
- **New editions of standards adopted without checking** what changed.
- **Small in-house changes treated as "the standard method"**: a different
  crucible, a shorter drying time, a different sample mass. Each one needs
  validation or must be removed.
- **Validation done but not linked** to the uncertainty budget or QC limits.

## Templates

The validation plan and report template arrives in version 0.4.

## Tools

- [`labqc.validation.intermediate_precision`](https://mantas123456.github.io/lab-quality-toolkit/api/validation/#labqc.validation.intermediate_precision)
  and [`trueness`](https://mantas123456.github.io/lab-quality-toolkit/api/validation/#labqc.validation.trueness):
  the calculations in this example.
- [`labqc.validation.linearity`](https://mantas123456.github.io/lab-quality-toolkit/api/validation/#labqc.validation.linearity)
  and [`lod_loq`](https://mantas123456.github.io/lab-quality-toolkit/api/validation/#labqc.validation.lod_loq):
  for instrumental methods with a calibration line.
- [The labqc web app, Method validation page](https://lab-quality-toolkit-3go33hyzzwjhwpktn8tles.streamlit.app/Method_validation).

## Related clauses

- [7.6 Measurement uncertainty](7-6-measurement-uncertainty.md) and
  [7.7 Validity of results](7-7-validity-of-results.md): validation data
  feeds both.
- [6.2 Personnel](../resources/6-2-personnel.md): analysts are authorised
  for a method only after it is verified and they have shown they can run
  it.
