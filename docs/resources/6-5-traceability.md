---
clause: "6.5"
description: How a lab links its results to SI units through an unbroken chain of calibrations, and what to do when that is not possible, with a worked chain for a moisture result.
---

# 6.5 Metrological traceability

## In one sentence

Be able to show an unbroken, documented chain of calibrations from each
result back to a recognised reference, normally the SI units, with an
uncertainty at every step.

## What an assessor looks for

- **A chain for each measurement that matters**: which equipment and
  reference materials carry traceability into each result.
- **Calibrations from competent providers**: usually calibration labs
  accredited to ISO/IEC 17025 for that calibration, or national
  metrology institutes. The certificate should show the results, their
  uncertainty and a traceability statement.
- **Certified reference materials from competent producers**: usually
  producers accredited to ISO 17034, with certified values and
  uncertainties.
- **When SI traceability is not possible** (some chemical and physical
  properties), evidence of traceability to another suitable reference:
  certified values of reference materials, or results of a reference
  method or a well-described agreed method.
- **Your accreditation body's traceability policy** followed. Many follow
  the ILAC policy on traceability (ILAC P10).

*Calibration labs:* your own reference standards and calibration hierarchy
are part of the chain the assessor follows, which is the main way this
clause differs for you (see
[testing labs and calibration labs](../start-here/how-to-use.md#testing-labs-and-calibration-labs)).

## How to do it in a small lab

1. **Map the chain for each method.** List every input in the method's
   equation (mass, temperature, volume, a reference material value) and
   which item of equipment or material provides it.
2. **Choose providers carefully.** Prefer calibration labs accredited for
   exactly that calibration and range. Check their scope, not only that
   they are accredited ([6.6](6-6-external-providers.md)).
3. **Check each certificate on arrival**: the right item, the right range,
   results with uncertainty, a traceability statement, and (if you use the
   accreditation body's policy) the accreditation mark.
4. **Use the uncertainty from the certificate** in your budget
   ([7.6](../process/7-6-measurement-uncertainty.md)). Divide the expanded
   uncertainty by its *k*.
5. **Keep reference materials traceable too**: certificate on file, stored
   as the certificate says, used before expiry.
6. **Explain the chain to the assessor** in one or two sentences per method.
   If you cannot, there is probably a gap.

## Worked example

The traceability chain for a total moisture result at a made-up biofuel
lab:

| Input in the equation | Provided by | Calibrated by | Traceable to |
|---|---|---|---|
| Masses before and after drying | Balance B-03 | Accredited calibration lab, with calibrated weights | National mass standard, SI kilogram |
| Oven temperature (105 °C) | Oven O-01, checked with thermometer T-02 | Thermometer T-02 calibrated by an accredited calibration lab | National temperature standard, SI kelvin |
| Drying time | Lab timer | A timer's accuracy is far better than the method needs; no calibration required, as the lab's risk assessment records | – |

For calorific value, the chain also includes the benzoic acid reference
material used to calibrate the calorimeter. Its certified heat of
combustion comes from a producer accredited to ISO 17034, and the
certificate states its uncertainty.

**A gap found.** At an internal audit, the auditor asks how the oven
temperature is known. T-02's certificate covers 0 to 100 °C, but the oven
runs at 105 °C. The lab asks the calibration lab to extend the range to
150 °C at the next calibration, and in the meantime records why the error
at 105 °C is small (from the certificate's results near 100 °C and the
maker's specification).

## Common findings

- **Calibrations by providers not accredited for that calibration**, with
  no other evidence of competence.
- **Certificates that do not cover the range used**, as in the example.
- **No traceability for reference materials**: in-house materials used as
  if they were certified.
- **Uncertainty from certificates not used** in the uncertainty budget.
- **Equipment that carries traceability missing from the chain**:
  thermometers, timers, volumetric glassware nobody thought about.

## Templates

<!-- templates -->

## Tools

No calculation tool is needed for the chain itself. Certificate
uncertainties feed the budget in
[`labqc.uncertainty.combine`](https://mantas123456.github.io/lab-quality-toolkit/api/uncertainty/#labqc.uncertainty.combine).

## Related clauses

- [6.4 Equipment](6-4-equipment.md): calibration programmes and
  certificate review.
- [7.6 Measurement uncertainty](../process/7-6-measurement-uncertainty.md):
  each link in the chain adds uncertainty.
- [7.2 Methods](../process/7-2-methods.md): CRMs for trueness checks.
