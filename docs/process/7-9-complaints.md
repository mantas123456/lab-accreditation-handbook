---
clause: "7.9"
description: How a lab receives, investigates and closes complaints fairly, with a worked example of a disputed ash result.
---

# 7.9 Complaints

## In one sentence

Have a fair, documented way to receive, check, investigate and answer
complaints, make it available to anyone who asks, and make sure the person
who decides the outcome was not involved in the work complained about.

## What an assessor looks for

- **A written complaints process** that the public can see on request,
  covering how complaints are received, checked, investigated and decided.
- **A complaints log** with every complaint, including the ones you think
  are unjustified, and its status.
- **Confirmation first**: the lab checks whether the complaint is about
  work it is responsible for before investigating.
- **Records of the investigation**, the decision and the action taken.
- **Impartial decisions**: the outcome is reviewed or approved by someone
  not involved in the activity complained about ([4.1](../general/4-1-impartiality.md)).
- **Communication with the complainant**: an acknowledgement, progress
  updates where useful, and a formal answer when the complaint is closed.
- **Links to the rest of the system**: complaints that reveal nonconforming
  work go to [7.10](7-10-nonconforming-work.md) and corrective action
  ([8.7](../management/8-7-corrective-action.md)), and complaint trends go
  to management review.

## How to do it in a small lab

1. **Define a complaint broadly.** Any expression of dissatisfaction that
   asks for a response, by phone, email or in person. Log it even if it
   turns out to be a misunderstanding: the log is evidence the process
   works.
2. **Acknowledge quickly** and tell the complainant what happens next.
3. **Check that it is about your work.** A complaint about a result the
   customer's other supplier produced is not yours to investigate, but
   still answer it.
4. **Investigate with facts.** Look at the records, the QC data for that
   run and the retained sample. Retest if the question is about a result.
5. **Separate doing from deciding.** In a lab of three people, the person
   who did the test can collect facts, but someone else should decide the
   outcome and sign the reply.
6. **Close formally.** Write to the complainant with the outcome. If the
   complaint was justified, open a nonconformity and corrective action.
7. **Review trends.** Count complaints by type at management review
   ([8.9](../management/8-9-management-review.md)).

## Worked example

A pellet producer complains to a made-up biofuel lab: the lab reported
0.52 % ash on a batch, but the buyer's lab found 0.71 %, and the buyer
wants a price reduction because of the difference.

| Step | What the lab did |
|---|---|
| Log | Complaint C-26-07 logged; acknowledged by email the same day |
| Confirm | The 0.52 % result is from the lab's own report 26-0388: within its responsibility |
| Investigate | Records checked: method followed, crucibles weighed correctly, QC sample in control. Retained sample retested in duplicate by a different analyst: 0.50 % and 0.53 %. Uncertainty for ash at this level: ± 0.04 % |
| Look wider | The two labs' samples were taken at different times from different parts of the batch; the buyer's lab dried at a different temperature before ashing |
| Decide | Reviewed and decided by the quality manager, who was not involved in the test: the lab's result is confirmed; the difference is more likely due to sampling and method differences than to a testing error |
| Respond | Letter to the producer with the retest results and the possible reasons for the difference, and an offer to test a sample split under agreed conditions |
| Close | Complaint closed as "not justified"; trend noted for management review: second complaint this year involving split samples between labs |

The lab also adds a note to its sampling advice for customers about
splitting samples for comparison tests.

## Common findings

- **Complaints handled informally** by phone and not logged.
- **The same person investigates and decides** the outcome of a complaint
  about their own work.
- **No formal reply** to the complainant, or no record that it was sent.
- **Justified complaints not linked** to a nonconformity or corrective
  action.
- **Process not available to the public** on request.

## Templates

The complaint form arrives in version 0.4.

## Tools

No calculation is required. To check whether two labs' results agree within
their uncertainties, use the E<sub>n</sub> number:
[`labqc.proficiency.en_number`](https://mantas123456.github.io/lab-quality-toolkit/api/proficiency/).
In this example, 0.52 ± 0.04 % against 0.71 % would need the other lab's
uncertainty before a fair comparison can be made.

## Related clauses

- [7.10 Nonconforming work](7-10-nonconforming-work.md) and
  [8.7 Corrective action](../management/8-7-corrective-action.md): what
  follows a justified complaint.
- [4.1 Impartiality](../general/4-1-impartiality.md): why the decision
  must be independent.
