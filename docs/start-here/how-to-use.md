# How to use this handbook

## One clause, one page

Every chapter covers one clause of ISO/IEC 17025:2017, so you can send a
colleague a link to exactly the page that matches an audit finding or a
question. The clause number is in the page title and in the badge at the top
of the side panel.

## Testing labs and calibration labs

!!! info "Written mainly for testing labs"
    The worked examples and the tools look at things mainly from a testing
    lab's point of view. Calibration labs work to the same clauses, but
    three of them play out quite differently:

    - **[6.5 Traceability](../resources/6-5-traceability.md):** a
      calibration lab is itself a link in the chain. It must be able to show
      how each calibration it offers descends, step by step, from its own
      reference standards back to national standards: its calibration
      hierarchy.
    - **[7.6 Measurement uncertainty](../process/7-6-measurement-uncertainty.md):**
      every calibration needs its own uncertainty, not one estimate per
      method. The scope of accreditation states the lab's calibration and
      measurement capability (CMC), the smallest uncertainty it may claim
      for each quantity and range, and no certificate may claim better.
    - **[7.8 Reporting](../process/7-8-reporting.md):** a calibration
      certificate has its own list of content, with the uncertainty given
      alongside the results. A statement that an instrument is within
      specification has to allow for that uncertainty, and the certificate
      should not recommend when to recalibrate unless the customer has
      agreed to it.

## The same headings on every page

1. **In one sentence:** the requirement in plain English.
2. **What an assessor looks for:** the evidence you will be asked to show.
3. **How to do it in a small lab:** practical steps.
4. **Worked example:** from a fuel, environmental or calibration lab, with
   made-up but realistic numbers.
5. **Common findings:** typical nonconformities and how to avoid them.
6. **Templates:** editable Word and Excel downloads (see the
   [templates library](../template-library/index.md)).
7. **Tools:** the matching [labqc](https://github.com/mantas123456/lab-quality-toolkit)
   function or web-app page, where a calculation is involved.
8. **Related clauses.**

## The side panel

On a wide screen the panel sits to the right of each chapter; on a phone it
sits at the top. It shows the clause, its status, the templates, the labqc
tools and the related clauses. It is built from one data file, so it is
always the same as the [clause map](../clause-map.md).

**Status** tells you how far a chapter has come:

- **Planned**: not written yet.
- **Draft**: written, not yet reviewed by a second practitioner.
- **Examples checked**: still a draft, but every number in the worked
  example is re-run by code on every build of the site.
- **Reviewed**: checked by a practising quality manager or assessor. No
  chapter has reached this yet.

The same status shows as a small icon next to each chapter in the
navigation; hover over it for its meaning.

## Where to begin

- **Preparing for a first assessment:** start with the
  [accreditation journey](journey.md), then work through Parts 4 to 8 in
  order.
- **Already accredited:** go straight to the clause behind your latest
  finding, or to [7.7 Ensuring the validity of results](../process/7-7-validity-of-results.md).
- **Need a calculation:** [7.6 Measurement uncertainty](../process/7-6-measurement-uncertainty.md)
  and the labqc links in each side panel.

## What this handbook is not

It does not reproduce the standard. You still need your own copy of
ISO/IEC 17025 and your accreditation body's documents, which always take
priority over anything here.
