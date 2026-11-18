---
clause: "7.6"
description: How a testing or calibration lab estimates, documents and uses measurement uncertainty, with a worked moisture-in-wood-pellets budget.
---

# 7.6 Measurement uncertainty

## In one sentence

For every result you report, know how far from the true value it could
reasonably be, show how you worked that out, and use it when you report a
result or say whether a sample passes.

## What an assessor looks for

- **A list of methods in your scope, each with an uncertainty estimate.**
  Calibration labs need one for every calibration they do, including
  calibrations of their own equipment. Testing labs need one for every
  test, or a clear reason why a full estimate is not possible.
- **The budget behind each estimate.** The sources of uncertainty you
  considered, the data you used for each one, how you turned each into a
  standard uncertainty, how you combined them, and the coverage factor.
- **Real data, not guesses.** The numbers should trace back to validation
  data, QC charts, proficiency testing results and calibration
  certificates. An assessor will often compare your budget with your own
  control chart.
- **Evidence it is kept up to date.** A review date, and a new version
  after a change of equipment, method or staff, or when QC data shows the
  method is noisier than the budget says.
- **People who understand it.** Expect the question "What is the biggest
  contributor for this test?" to an analyst, not only to the quality
  manager.
- **Where it is used.** In reports when the customer asks for it or when it
  affects whether a result meets a limit, and in your decision rule (see
  [7.8 Reporting](7-8-reporting.md)).

Some test methods are written so tightly that they fix the main sources of
variation and say how to present results. For those, the method's own
precision data can carry much of the estimate, but you still need to show
that your lab performs at least as well as the method claims.

## How to do it in a small lab

1. **Define exactly what you measure.** "Moisture" is not enough. Write
   "moisture content of wood pellets as received, mass fraction in %,
   by oven drying at 105 °C". Many arguments about uncertainty are really
   arguments about the measurand.
2. **Write down the equation** that turns your readings into the result.
   Every quantity in it is a possible source of uncertainty.
3. **List the sources.** Draw a cause-and-effect (fishbone) diagram with
   the analysts: sample preparation, weighing, instrument, environment,
   operator, reference values, sampling if you do it. Doing this as a
   team also helps with [6.2 competence](../resources/6-2-personnel.md).
4. **Pick an approach.**
    - *Bottom-up (GUM)*: quantify each source separately and combine them.
      Best for calibrations and simple methods with a clear equation.
    - *Top-down*: use long-term data that already contains most sources:
      within-lab reproducibility from your QC chart, plus a bias term from
      proficiency testing or certified reference materials. The Nordtest
      TR 537 handbook describes this approach. It is the practical choice
      for most testing labs.
    - Many labs mix the two: top-down for the bulk, plus a few bottom-up
      terms for anything the long-term data misses.
5. **Turn each source into a standard uncertainty.**
    - From a certificate quoting *U* and *k*: divide *U* by *k*.
    - From a "±a" limit with no more information (a tolerance, a
      specification): treat it as rectangular, divide *a* by √3.
    - From repeated measurements: the standard deviation, divided by √n if
      you report the mean of n results.
6. **Combine.** For independent sources, square each contribution, add
   them and take the square root:

    \[
    u_c = \sqrt{\sum_i \left(c_i\, u_i\right)^2}
    \]

    where *c<sub>i</sub>* is the sensitivity coefficient (how much the
    result changes per unit change in that input; 1 when the source is
    already in result units).
7. **Expand.** Multiply by a coverage factor *k* to get the expanded
   uncertainty *U* = *k* × *u<sub>c</sub>*. *k* = 2 gives about 95 %
   coverage when there is plenty of data. When a large share of the budget
   rests on few data points, use the effective degrees of freedom
   (Welch–Satterthwaite) to choose *k*; it will be a little above 2. Many
   testing labs simply use *k* = 2, following the EA-4/02 guidance; that is
   fine when the main contributions rest on enough data.
8. **Check it against reality.** If *U* is smaller than the scatter on
   your own control chart, or your PT z-scores often exceed what *U*
   predicts, a source is missing.
9. **Record and review it.** Keep one budget per method, version it under
   document control ([8.3](../management/8-3-document-control.md)), and
   review it at least once a year and after any change.
10. **Decide where it matters.** Compare *U* with the limits your customers
    test against. If results near a limit are common, you need a documented
    decision rule.

!!! tip "Spend your effort where the variance is"
    Sort the budget by contribution. In most testing methods one or two
    sources make up most of the total. Improving a source that contributes
    1 % of the variance changes nothing a customer will notice.

## Worked example

A made-up solid biofuel lab measures the moisture content of wood pellets
by oven drying at 105 °C, following a standard oven-drying method for solid
biofuels. Each sample is tested in duplicate and the mean is reported.

**Equation**

\[
M = \frac{m_2 - m_3}{m_2 - m_1} \times 100
\]

where *m*<sub>1</sub> is the empty tray, *m*<sub>2</sub> the tray with the
sample before drying, and *m*<sub>3</sub> the tray with the sample after
drying. (The full method also corrects with an empty reference tray for
buoyancy; it is left out of the equation here to keep it short.) The sample
is dried until a further hour in the oven no longer changes its mass by more
than a small set amount. The result for this sample is **M = 7.74 %**.

**Sources and data**

| Source | Data used | Type | Value | Standard uncertainty (% moisture) | Degrees of freedom |
|---|---|---|---|---|---|
| Repeatability | 10 duplicate pairs on routine samples, s<sub>r</sub> = 0.10 %; mean of two reported, so 0.10 / √2 | A, normal | 0.071 | 0.071 | 10 |
| Balance | Calibration certificate, U = 0.010 g (k = 2). Passed through the equation for a ~300 g test portion, the three weighings move M by less than 0.010 % (k = 2); that value is used, rounded up | B, normal | 0.010 (k = 2) | 0.005 | ∞ |
| Drying temperature | Oven allowed 105 ± 2 °C; in-house study showed results move by up to ±0.05 % across that range | B, rectangular | ±0.05 | 0.029 | ∞ |
| Weighing hot | Trays are weighed within seconds of leaving the oven, and an empty reference tray dried alongside corrects for air buoyancy. An in-house study put what that correction misses at up to ±0.06 % | B, rectangular | ±0.06 | 0.035 | ∞ |
| Laboratory bias | Last six PT rounds: root mean square of differences from the assigned values, combined with the uncertainty of the assigned values | A, normal | 0.080 | 0.080 | 5 |

All sensitivity coefficients are 1 because every source is already
expressed in % moisture.

**Result**

| | |
|---|---|
| Combined standard uncertainty *u<sub>c</sub>* | 0.116 % |
| Effective degrees of freedom | 17 |
| Coverage factor *k* (95 %) | 2.11 |
| Expanded uncertainty *U* | 0.25 % |
| Relative expanded uncertainty | 3.2 % |

The lab reports: **moisture 7.74 % ± 0.25 % (k = 2.11, about 95 % coverage)**.

**What the budget tells the lab**

| Source | Share of variance |
|---|---|
| Laboratory bias | 47 % |
| Repeatability | 37 % |
| Weighing hot | 9 % |
| Drying temperature | 6 % |
| Balance | 0.2 % |

- Bias and repeatability together are 85 % of the total. To reduce *U*, the
  lab should look at its PT results and its sample division, not at the
  balance.
- The balance contributes 0.2 %. A more expensive balance would not change
  the reported uncertainty at all.
- The pellet quality class this customer works to has a moisture limit of
  10 %. A result of 7.74 ± 0.25 % is far from it, so the decision is clear.
  For results within about 0.3 % of the limit, the lab's decision rule
  ([7.8](7-8-reporting.md)) applies.

**The same calculation in labqc**

```python
from labqc.uncertainty import Component, combine

budget = [
    Component("Repeatability (mean of duplicate)", 0.071, dof=10),
    Component("Balance calibration", 0.010, k=2),
    Component("Drying temperature 105 ± 2 °C", 0.05, "rectangular"),
    Component("Weighing hot (buoyancy residual)", 0.06, "rectangular"),
    Component("Laboratory bias (PT history)", 0.08, dof=5),
]
result = combine(budget, value=7.74)
print(result.summary(relative=True))
# u_c = 0.1162, v_eff = 17.0, k = 2.11, U (95%) = 0.2452 | u_c/|y| = 1.501%, U/|y| = 3.167%
print(result.table)  # contributions, sorted largest first
```

## Common findings

- **Budgets for some methods only.** Often the ones that were easy, or the
  ones from the first assessment. Check every method in your scope.
- **A budget made once and never reviewed**, while the QC chart shows the
  method has become noisier.
- **An uncertainty smaller than the lab's own QC scatter.** The assessor
  compares the two; so should you.
- **A certificate's expanded uncertainty used as if it were a standard
  uncertainty**, without dividing by *k*. Or a full range used where the
  half-width belongs.
- **Mixed units.** Relative and absolute uncertainties added together, or
  grams mixed with percent, without sensitivity coefficients.
- **Repeatability from two or three results.** A standard deviation from so
  few values is itself very uncertain. Use long-term duplicate or QC data
  instead.
- **No bias term.** A budget built only from repeatability and equipment
  ignores how far the lab's results sit from the true value. PT or CRM data
  fixes that.
- **Sampling left out** when the lab takes the samples itself and the
  customer's question is about the batch, not the test portion.
- **Uncertainty ignored in pass/fail statements**, with no decision rule
  agreed with the customer.
- **Staff who cannot explain it.** If only the quality manager understands
  the budget, the assessor will notice.

## Templates

<!-- templates -->

The spreadsheet uses the same calculation as `labqc.uncertainty.combine`, and the tests in this handbook's repository check that the two agree.

## Tools

- [`labqc.uncertainty.combine`](https://mantas123456.github.io/lab-quality-toolkit/api/uncertainty/#labqc.uncertainty.combine):
  combines a budget, chooses *k* from the effective degrees of freedom and
  shows each source's share.
- [`labqc.uncertainty.monte_carlo`](https://mantas123456.github.io/lab-quality-toolkit/api/uncertainty/#labqc.uncertainty.monte_carlo):
  checks the result by simulation when the equation is strongly non-linear.
- [The labqc web app, Uncertainty budget page](https://lab-quality-toolkit-3go33hyzzwjhwpktn8tles.streamlit.app/Uncertainty_budget):
  the same calculation in the browser, no Python needed.

## Related clauses

- [7.2 Methods](7-2-methods.md): validation data feeds the budget.
- [7.7 Validity of results](7-7-validity-of-results.md): the QC chart and PT
  results are the reality check for the budget.
- [7.8 Reporting](7-8-reporting.md): how *U* appears on the report and in
  decision rules.
- [6.5 Traceability](../resources/6-5-traceability.md): calibration
  certificates supply several of the inputs.
