---
clause: "7.10"
description: What a lab does when work does not meet its own requirements or the customer's, with a worked example of a failed calorimeter check.
---

# 7.10 Nonconforming work

## In one sentence

When any part of your work does not go as your procedures or the customer
require, stop or hold what is affected, work out how big the problem is and
what it has touched, fix the results, tell customers where needed, and
decide whether the cause needs corrective action.

## What an assessor looks for

- **A procedure** saying who can stop work, hold reports and allow work to
  restart, and how nonconforming work is recorded.
- **Nonconformities recorded**, including the small ones fixed at once.
  A lab with no records of nonconforming work is not believable.
- **An assessment of significance**: how serious it is, which results were
  affected, back to when.
- **Action on affected results**: retests, recalled or amended reports, and
  customers told when they need to know.
- **A decision on corrective action**: when the problem could happen again,
  or when it casts doubt on your procedures, it goes to
  [8.7](../management/8-7-corrective-action.md).
- **Links to where nonconformities are found**: QC failures
  ([7.7](7-7-validity-of-results.md)), complaints ([7.9](7-9-complaints.md)),
  audits ([8.8](../management/8-8-internal-audits.md)), equipment checks,
  report reviews, staff observations.

## How to do it in a small lab

1. **Make it easy to raise one.** One short form or LIMS entry, which anyone
   can open. Thank people for raising them: a lab that punishes reporting
   stops hearing about problems.
2. **Contain first.** Stop the affected test or hold the affected reports
   straight away. Label the instrument "Do not use" if it is the cause.
3. **Look back.** Find the last time you knew things were right (the last
   good QC result or check) and list everything done since.
4. **Assess the impact on each affected result.** Compare the possible
   error with the uncertainty and with any limits the customer works to.
   Retest retained samples where you can.
5. **Act on the results.** If a reported result is wrong by more than its
   uncertainty, or a pass/fail decision could change, issue an amended
   report ([7.8](7-8-reporting.md)) and contact the customer.
6. **Decide on restart.** The technical manager authorises restart once the
   cause is removed and a check passes.
7. **Ask "could it happen again?"** If yes, open a corrective action and
   find the root cause.

## Worked example

A made-up biofuel lab calibrates its bomb calorimeter with benzoic acid, a
reference material with a certified heat of combustion, from a series of
ten accepted burns. Between calibrations it burns one benzoic acid tablet
every week as a check. It set the acceptance limit for that check from the
spread of its calibration burns: the certified value ± 0.25 %.

**Detection.** On Monday, the check reads 0.9 % low. A repeat check is also
low. The analyst stops calorific value testing, labels the calorimeter and
raises nonconformity NC-26-14. Looking back, there had been an earlier
sign: twice in the past week, a sample's duplicate results differed by more
than the method's repeatability limit and had to be repeated.

**Look back.** The previous check, eight days earlier, passed. Since then,
the lab has tested 11 samples, and reports for 10 of them have been issued.

**Cause.** The technical manager finds a worn O-ring on the bomb head. A
small leak during combustion lets some heat escape, so results read low. The
O-ring is replaced; two benzoic acid checks pass; testing restarts with the
technical manager's sign-off.

**Impact.** Retained samples for all 11 jobs are retested:

| Result | Number of samples | Action |
|---|---|---|
| Change smaller than the expanded uncertainty | 8 | No change to reports; recorded in NC-26-14 |
| Change larger than the uncertainty, no effect on a pass/fail statement | 2 | Amended reports issued, customers told |
| Change moves a result from below to above a contract minimum | 1 (report not yet issued) | Report issued with the retest result only |

**Corrective action.** Could it happen again? Yes: the O-ring had no
replacement schedule, and nobody treated repeated duplicate failures as a
warning. Corrective action CA-26-06 adds a visual check of the seals to the
weekly check and replacement every six months to the equipment plan
([6.4](../resources/6-4-equipment.md)). It also adds a rule to the method:
two repeated duplicates in one week trigger an extra benzoic acid check.

## Common findings

- **Very few or no nonconformities recorded**, while QC charts and equipment
  records show problems.
- **The instrument fixed, but no look back** at results produced since the
  last good check.
- **Affected customers not told**, or reports changed without an amended
  report.
- **Work restarted without authorisation** or without a passing check.
- **Every nonconformity sent to corrective action** (the system drowns), or
  none (nothing improves). The decision should be recorded each time.

## Templates

<!-- templates -->

## Tools

No calculation tool is needed. To decide whether a retest differs from the
original by more than chance, compare the difference with the expanded
uncertainty from [7.6](7-6-measurement-uncertainty.md).

## Related clauses

- [7.7 Validity of results](7-7-validity-of-results.md): the most common
  source of nonconformities.
- [8.7 Corrective action](../management/8-7-corrective-action.md): when
  the cause must be removed.
- [7.9 Complaints](7-9-complaints.md): complaints often reveal
  nonconforming work.
