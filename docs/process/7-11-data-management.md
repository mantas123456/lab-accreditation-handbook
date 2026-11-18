---
clause: "7.11"
description: How a lab controls the software, spreadsheets and systems that hold and calculate its data, with a worked validation of a calculation spreadsheet.
---

# 7.11 Control of data and information management

## In one sentence

Make sure every system that collects, calculates, stores or reports your
data, from a LIMS to a single spreadsheet, does what you think it does, is
protected from unauthorised change, and keeps data intact.

## What an assessor looks for

- **An inventory of systems** that touch results: LIMS, instrument
  software, calculation spreadsheets, databases, scripts.
- **Validation before use** for each system, and again after changes,
  including spreadsheets you built yourself. Commercial software used as
  supplied can be treated as validated for its intended use, but your
  configuration, templates and custom calculations still need checking.
- **Access control**: who can enter, change, approve and delete data, and
  how that is enforced (accounts, passwords, locked cells).
- **Protection against tampering and loss**: backups that have been tested
  by restoring, audit trails, and controlled versions.
- **Suitable operating conditions** for the systems, as the supplier
  specifies or as you have decided.
- **Records of system failures** and of what was done about them.
- **Checks on data transfers and calculations**, by design or by review.
- **External systems** (cloud LIMS, outsourced IT) covered by the same
  requirements through the agreement with the provider.

## How to do it in a small lab

1. **List everything.** A one-page register: system, what it does, version,
   owner, validation status, where it runs, backup arrangement.
2. **Validate by testing with known answers.** For each calculation, prepare
   a few test cases with results worked out by hand or from a textbook,
   including edge cases (zero, a missing value, a value at a limit). Run
   them, compare, and record the result with the version tested.
3. **Lock what should not change.** Protect formula cells, keep the master
   copy read-only, and give each released version a number.
4. **Control changes.** Any change to a validated calculation gets a new
   version, a re-run of the test cases, and a record of who approved it.
5. **Check transfers.** If results move by hand from an instrument to a
   spreadsheet to a report, check a sample of transfers at review
   ([7.5](7-5-technical-records.md)). Better: transfer files, not
   keystrokes.
6. **Back up and test the backup.** Restore a file from backup once a year
   and record that it worked.

## Worked example

A made-up biofuel lab calculates calorific value in a spreadsheet: gross
calorific value at constant volume from the calorimeter, then corrections
for moisture and hydrogen to give the net calorific value as received.

**Inventory entry.** "CV calc, spreadsheet, v2.0, owner: technical manager,
used for every calorific value report."

**Validation plan.** Five test cases with known answers:

| Test case | Source of expected answer | Result |
|---|---|---|
| Worked example from the calorific value standard's annex | Standard | Matches to 0.001 MJ/kg |
| Typical pellet, all inputs normal | Hand calculation, checked by a second person | Matches |
| Moisture 0 % | Hand calculation | Matches |
| Moisture 60 % (wet wood chips) | Hand calculation | Matches |
| Missing hydrogen value | Expected: clear error, no result | **Failed**: sheet used 0 and gave a result |

**Fix and re-test.** A check is added so that a missing input shows an
error and no result. All five cases are re-run on v2.1 and pass. The formula
cells are locked; the master file is read-only; the validation record names
v2.1, the date, the tester and the approver.

**In use.** Each worksheet records the spreadsheet version used. When the
standard is revised next year, v2.1 is reviewed against the new edition
before use ([7.2](7-2-methods.md)).

!!! tip "Your own code counts too"
    If you write scripts or use a library such as labqc for calculations,
    the same approach applies: known-answer tests, version control and a
    record of the version used. labqc's own
    [validation report](https://mantas123456.github.io/lab-quality-toolkit/validation/)
    shows one way to document this for a Python library.

## Common findings

- **Spreadsheets never validated**, or validated once and changed since
  without re-testing.
- **Unlocked formulas** that anyone can overwrite.
- **No version recorded**, so it cannot be shown which calculation produced
  an old result.
- **Shared logins**, so the audit trail cannot say who changed what.
- **Backups never tested** by restoring.
- **Manual transcription not checked.**

## Templates

<!-- templates -->

## Tools

No calculation tool is needed. See the labqc
[validation report](https://mantas123456.github.io/lab-quality-toolkit/validation/)
for an example of a documented software validation.

## Related clauses

- [7.5 Technical records](7-5-technical-records.md): electronic records and
  corrections.
- [8.4 Records](../management/8-4-records.md): retention and protection.
- [4.2 Confidentiality](../general/4-2-confidentiality.md): protecting
  customer data held in your systems.
