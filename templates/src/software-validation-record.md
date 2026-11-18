---
title: Software and spreadsheet validation record
type: Record
description: Validate a spreadsheet, script or software configuration with known-answer test cases, and record the version, protection and approval.
---

| | |
|---|---|
| **System / file name** | |
| **Version validated** | |
| **Used for** (methods, results) | |
| **Owner** | |
| **Type** | ☐ Spreadsheet ☐ Script or code ☐ Instrument software (configuration) ☐ LIMS ☐ Other: |

# 1. What it must do

List each calculation or function the lab relies on, and the input and
output units.

# 2. Test cases

Include typical values, edge cases (zero, very high, at a limit) and bad
input (a missing or impossible value). Expected answers come from hand
calculation, the standard's worked example or a second independent tool.

| # | Description | Inputs | Expected result | Source of expected result | Actual result | Pass? |
|---|---|---|---|---|---|---|
| 1 | Worked example from the standard | | | Standard, annex ___ | | ☐ |
| 2 | Typical sample | | | Hand calculation by ___ | | ☐ |
| 3 | Edge case: | | | | | ☐ |
| 4 | Missing input | | Clear error, no result | | | ☐ |
| 5 | | | | | | ☐ |

# 3. Protection and control

| Check | Done |
|---|---|
| Formula cells locked; inputs only in marked cells | ☐ |
| Master copy read-only; users work on copies or a protected template | ☐ |
| Version number visible in the file | ☐ |
| Version recorded on each worksheet or result | ☐ |
| Backup in place | ☐ |
| Access limited to authorised users (for software) | ☐ |

# 4. Conclusion and approval

☐ Validated for the uses in section 1.

| | |
|---|---|
| Tested by / date | |
| Approved by / date | |

# 5. Changes

Any change to the calculation gets a new version, a re-run of the test
cases and a new approval.

| Version | Date | Change | Test cases re-run | Approved by |
|---|---|---|---|---|
| | | | ☐ All ☐ Affected only: | |
