---
clause: "8.9"
description: How a lab's top management reviews the whole system at planned intervals, what goes in, what must come out, with a worked agenda and decisions.
---

# 8.9 Management review

## In one sentence

At planned intervals, top management looks at all the evidence about how
the lab and its system are performing, and decides what to change, what to
improve and what resources are needed.

## What an assessor looks for

- **Reviews at planned intervals**, usually at least once a year.
- **All the required inputs covered**, with data, not just headings (see
  the agenda below).
- **Outputs recorded as decisions and actions**: about the effectiveness of
  the system, improvements, resources, and any changes needed.
- **Top management present** and taking the decisions.
- **Follow-up**: actions from the last review reported on.

## How to do it in a small lab

1. **Fix a date** each year, for example in January, so the data covers a
   calendar year.
2. **Prepare short summaries** for each input: one page or a few numbers
   each. The quality manager collects them two weeks before.
3. **Hold the meeting** with top management, the quality manager and the
   technical manager. Two hours is usually enough.
4. **Record decisions, not discussion.** Each output gets an owner and a
   date.
5. **Track the actions** like corrective actions, and report on them at the
   next review.

## Worked example

A made-up biofuel lab's management review agenda, with the input data and
decisions:

| # | Input | Data presented | Decision or action |
|---|---|---|---|
| 1 | Actions from last review | 6 of 7 done; LIMS upgrade delayed | Upgrade by June; owner: lab head |
| 2 | Changes inside and outside the lab | New edition of the ash standard; one analyst on leave in autumn | Verify changed steps ([7.2](../process/7-2-methods.md)); train a second CHNS analyst |
| 3 | Objectives | PT: 11 of 12 satisfactory; turnaround 10 days in 91 % (target 95 %) | Group calorimeter runs to cut turnaround |
| 4 | Policies and procedures still suitable? | Contract review form missing "basis" field | Already fixed by CA-26-04 |
| 5 | Internal audits | 8 audits; 5 nonconformities, all closed | Add a witness audit for ash |
| 6 | Corrective actions | 9 opened, 8 closed on time | None |
| 7 | External assessments | Accreditation body surveillance: 2 findings, closed | None |
| 8 | Changes in volume and type of work | Calorific value requests +30 % | Second calorimeter quote requested |
| 9 | Customer and staff feedback | Survey: report clarity 3.5/5 | New report template ([8.6](8-6-improvement.md)) |
| 10 | Complaints | 3; 1 justified | None beyond CA already taken |
| 11 | Effectiveness of improvements | Turnaround −5 days for calorific value | Continue |
| 12 | Resources | One single-point-of-failure method (CHNS) | Training funded |
| 13 | Risks | Register reviewed; 2 new risks | Register updated ([8.5](8-5-risks-and-opportunities.md)) |
| 14 | Validity of results (QC and PT) | One QC drift on moisture (oven); one questionable PT z = 2.3 on ash | Monthly oven check added; ash PT investigated |
| 15 | Other: training, monitoring, impartiality | All authorisations monitored; impartiality register reviewed | None |

**Conclusion recorded:** the management system is effective; three
improvements and two resource decisions agreed, each with an owner and a
date.

## Common findings

- **Inputs listed without data**: "Internal audits: discussed".
- **No decisions or actions** recorded, only minutes of discussion.
- **Top management absent.**
- **Actions from the last review not followed up.**
- **Inputs missing**, most often the validity of results (QC and PT),
  risks, and changes in workload.

## Templates

<!-- templates -->

## Tools

No calculation is needed for this clause. labqc's
[`pt_history`](https://mantas123456.github.io/lab-quality-toolkit/api/proficiency/#labqc.proficiency.pt_history)
gives a ready summary of PT scores for input 14.

## Related clauses

- [8.8 Internal audits](8-8-internal-audits.md): a required input.
- [8.5 Risks and opportunities](8-5-risks-and-opportunities.md) and
  [8.6 Improvement](8-6-improvement.md): reviewed here.
