# Electrical Conductivity Measurement Protocol

## Overview

This protocol defines two complementary methods for measuring the electrical
conductivity (or resistivity) of low-alloy steel specimens used in the
machinability study. Both methods are applied to every specimen so that results
can be cross-validated and method-specific uncertainties can be compared
(addresses RQ3).

| Method | Standard | Measured quantity | Primary output |
|--------|----------|-------------------|----------------|
| Four-probe DC resistivity | ASTM B193 | Electrical resistivity (micro-ohm-cm) | Converted to %IACS and MS/m |
| Eddy current conductivity | ASTM E1004 | Apparent conductivity (%IACS) | Converted to MS/m and micro-ohm-cm |

All measurements shall be performed at controlled room temperature
(23 +/- 2 degC) unless a temperature study is explicitly being conducted.

---

## 1 Specimen Preparation

### 1.1 Geometry

| Method | Specimen shape | Nominal dimensions | Tolerance |
|--------|---------------|--------------------|-----------|
| Four-probe DC | Rectangular bar | 100 mm x 10 mm x 5 mm (L x W x T) | +/- 0.05 mm |
| Eddy current | Disc or flat face of bar | Min 25 mm diameter, min 5 mm thick | Thickness > 3x skin depth at lowest test frequency |

Each specimen shall be permanently engraved with a unique ID using the
convention: `<steel grade>-<heat treatment code>-<specimen number>`,
e.g., `4140-QT-03`.

### 1.2 Surface Preparation

1. **Grinding** -- Wet-grind all measurement surfaces using SiC paper through
   180, 320, 600, and 1200 grit sequentially. Use fresh paper for each grit
   step. Apply light, uniform pressure; do not allow the specimen to overheat.
2. **Cleaning** -- Ultrasonically clean specimens in acetone for 5 min, then
   in isopropanol for 5 min. Dry with filtered compressed air.
3. **Demagnetisation** -- Pass each specimen through a commercial AC
   demagnetiser (peak field >= 100 mT) at a withdrawal rate <= 0.1 m/s.
   Verify residual field < 0.5 mT with a gaussmeter. This step is critical
   for eddy current measurements on ferromagnetic steels.
4. **Surface roughness check** -- Measure Ra on each measurement face.
   Accept only if Ra <= 0.8 um.  Record the value.
5. **Dimensional measurement** -- Measure length, width, and thickness at
   three locations each using a calibrated micrometer (resolution 0.001 mm).
   Record all values and compute the mean cross-sectional area A and gauge
   length L.
6. **Rest period** -- Allow specimens to equilibrate at 23 +/- 2 degC for at
   least 2 h before measurement.

### 1.3 Specimen Tracking Log

For every specimen, record:

| Field | Example |
|-------|---------|
| Specimen ID | 4140-QT-03 |
| Steel grade | AISI 4140 |
| Heat treatment | Q&T 850 degC / oil / 550 degC temper |
| Hardness (HRC) | 32.5 |
| Dimensions (L x W x T, mm) | 100.02 x 10.01 x 5.003 |
| Surface roughness Ra (um) | 0.45 |
| Residual magnetic field (mT) | 0.3 |
| Date prepared | 2026-xx-xx |

---

## 2 Method A: Four-Probe DC Resistivity (ASTM B193)

### 2.1 Principle

A known DC current I is passed through the specimen via two outer (current)
contacts. The voltage drop V is measured between two inner (potential) contacts
separated by a known distance l. Resistivity is computed as:

    rho = (V / I) * (A / l)

where A is the cross-sectional area.  The four-probe configuration eliminates
contact resistance from the measurement.

### 2.2 Equipment

| Item | Specification |
|------|--------------|
| DC current source | Programmable, 0 -- 10 A, stability < 0.01% over 1 h |
| Nanovoltmeter | Resolution <= 10 nV, input impedance > 1 GOhm (e.g., Keithley 2182A) |
| Current reversal switch | Low-thermal-EMF type; reversal time < 1 s |
| Specimen fixture | Spring-loaded knife-edge contacts, PTFE insulation, potential tap spacing 50 +/- 0.1 mm |
| Temperature sensor | Calibrated Pt100 RTD, accuracy +/- 0.1 degC, mounted on specimen surface |
| Calibrated reference bar | NIST-traceable Cu or Fe reference with certificate |
| Shielded cables | Low-thermoelectric-EMF (Cu-Cu), guarded |

### 2.3 Equipment Setup

1. Mount the specimen horizontally in the four-probe fixture. Ensure the two
   current contacts make firm, symmetric contact on the specimen ends and the
   two potential taps sit on the measurement surface with the calibrated
   spacing l.
2. Attach the Pt100 sensor to the specimen surface between the potential taps
   using thermal paste.
3. Connect current source to the outer contacts; nanovoltmeter to the inner
   potential contacts. Use shielded, twisted-pair cables.
4. Allow system to thermally stabilise for >= 15 min after powering on
   instruments.
5. Verify system by measuring the calibrated reference bar. Confirm agreement
   within +/- 0.5% of the certified value before proceeding.

### 2.4 Measurement Procedure

For each specimen, perform the following:

1. **Set current.** Select a DC current that produces a measurable voltage
   drop without Joule heating > 0.1 degC.  Typical starting current: 1 A for
   steel bars of the specified dimensions.
2. **Current reversal sequence.** For each reading, apply the following
   four-step delta method to eliminate thermal EMF offsets:
   - +I: record V_1
   - -I: record V_2
   - -I: record V_3
   - +I: record V_4

   Compute corrected voltage:

       V_corr = (V_1 - V_2 - V_3 + V_4) / 4

3. **Repeat.** Perform 10 independent current-reversal cycles without
   removing or repositioning the specimen.
4. **Reposition.** Remove the specimen, rotate 180 deg about its long axis,
   remount, and perform another 10 cycles. This guards against asymmetric
   contact effects.
5. **Record temperature.** Log the Pt100 reading at the start, midpoint, and
   end of each set of 10 cycles.

### 2.5 Data Recording

For each specimen, record:

| Column | Units | Description |
|--------|-------|-------------|
| specimen_id | -- | Unique specimen identifier |
| current_A | A | Applied DC current |
| V_corr_uV | uV | Corrected voltage from delta method |
| rho_raw_uOhm_cm | micro-ohm-cm | Calculated resistivity (uncorrected) |
| T_specimen_degC | degC | Specimen temperature at time of reading |
| rho_20C_uOhm_cm | micro-ohm-cm | Temperature-corrected resistivity (see Section 4) |
| sigma_IACS_pct | %IACS | Converted conductivity |
| sigma_MS_per_m | MS/m | Converted conductivity |
| orientation | -- | 0 deg or 180 deg rotation |
| reading_number | -- | 1..10 within each orientation |
| date_time | ISO 8601 | Timestamp |

### 2.6 Uncertainty Estimation

Identify and quantify the following uncertainty components (k = 1):

| Source | Typical magnitude | Evaluation method |
|--------|-------------------|-------------------|
| Nanovoltmeter accuracy | 0.05% of reading + 20 nV | Type B, manufacturer spec |
| Current source accuracy | 0.01% of setting | Type B, manufacturer spec |
| Potential tap spacing l | 0.1 mm / 50 mm = 0.2% | Type B, micrometer calibration |
| Cross-sectional area A | 0.05 mm / 10 mm ~ 0.5% (dominant) | Type B, micrometer calibration |
| Temperature correction | 0.1 degC * alpha ~ 0.05% | Type B, RTD calibration |
| Repeatability | ~0.1 -- 0.3% | Type A, std dev of 20 readings |
| Thermal EMF residual | < 0.02% after delta method | Type A, zero-current test |

Combine by root-sum-square (RSS) per GUM (JCGM 100:2008). Report expanded
uncertainty U with coverage factor k = 2 (95% confidence).

Expected combined standard uncertainty for steel: u_c(rho) ~ 0.5 -- 1.0%.

---

## 3 Method B: Eddy Current Conductivity (ASTM E1004)

### 3.1 Principle

An alternating current in a coil probe induces eddy currents in the specimen
surface. The impedance change of the coil depends on the specimen's electrical
conductivity and magnetic permeability. For non-ferromagnetic materials,
conductivity is read directly. For ferromagnetic steels (the case here),
special procedures are required to separate conductivity and permeability
effects.

### 3.2 Equipment

| Item | Specification |
|------|--------------|
| Eddy current instrument | Multi-frequency, impedance-plane display, operating range 1 kHz -- 10 MHz (e.g., Nortec 600 or equivalent) |
| Probe | Absolute pencil probe, tip diameter 5 -- 12 mm, frequency matched |
| Conductivity reference standards | Certified set covering 1 -- 60 MS/m (%IACS range 1.7 -- 103%), traceable to NIST or PTB |
| Lift-off spacers | Non-conductive shims: 0.05, 0.10, 0.20, 0.50 mm |
| Temperature sensor | Calibrated Pt100 RTD, accuracy +/- 0.1 degC |
| Probe stand | Spring-loaded holder with adjustable normal force (1 -- 5 N) to ensure consistent lift-off |

### 3.3 Ferromagnetic Steel Considerations

For ferromagnetic low-alloy steels (AISI 1045, 4140, 4340 in non-austenitic
conditions), magnetic permeability complicates eddy current conductivity
measurement.  The following mitigation strategies shall be applied:

1. **DC magnetic saturation.** Where feasible, use a probe with integrated
   DC magnetisation to locally saturate the specimen surface (driving relative
   permeability mu_r close to 1). This is the preferred approach.
2. **Multi-frequency impedance analysis.** If saturation is not available,
   measure at multiple frequencies (e.g., 60 kHz, 120 kHz, 480 kHz,
   1 MHz) and use established impedance-plane separation algorithms to
   decouple sigma and mu_r.
3. **Empirical calibration.** Calibrate against four-probe DC values from
   Method A on the same specimens. Build a correction curve specific to
   each steel grade and heat treatment.

Document which strategy is used for each specimen set.

### 3.4 Equipment Setup and Calibration

1. Power on the instrument and allow >= 30 min warm-up.
2. Select the operating frequency. Start with 60 kHz (standard for steel).
   Record the calculated skin depth delta:

       delta = 1 / sqrt(pi * f * mu_0 * mu_r * sigma)

   Ensure specimen thickness >= 3 * delta.
3. Perform a two-point (or multi-point) calibration using certified reference
   standards that bracket the expected conductivity range of the test
   specimens (typically 2 -- 8 MS/m for low-alloy steels).
4. Verify calibration by measuring a third reference standard not used for
   calibration.  Accept if within +/- 1% IACS of the certified value.
5. Perform a lift-off compensation routine using the 0.05 mm and 0.20 mm
   spacers, following the instrument manufacturer's procedure.

### 3.5 Measurement Procedure

For each specimen:

1. Place the specimen on a non-conductive, non-magnetic surface (e.g., PTFE
   block) away from metallic objects (minimum 150 mm clearance).
2. Position the probe at the centre of the measurement face using the
   spring-loaded stand. Ensure normal contact with consistent force.
3. Wait for the reading to stabilise (typically 2 -- 5 s).  Record the
   conductivity value.
4. Lift the probe, reposition at the same spot, and repeat. Perform
   10 readings without moving the specimen.
5. Rotate the specimen 90 deg, and perform another 10 readings at the centre
   of the measurement face. This checks for directional anisotropy (e.g.,
   from rolling texture).
6. Record specimen surface temperature at start and end of measurement.
7. If using multi-frequency analysis, repeat steps 2 -- 6 at each selected
   frequency.

### 3.6 Data Recording

| Column | Units | Description |
|--------|-------|-------------|
| specimen_id | -- | Unique specimen identifier |
| frequency_kHz | kHz | Operating frequency |
| sigma_reading_pct_IACS | %IACS | Instrument reading (uncorrected) |
| sigma_reading_MS_per_m | MS/m | Converted conductivity |
| T_specimen_degC | degC | Specimen temperature |
| sigma_20C_pct_IACS | %IACS | Temperature-corrected value (see Section 4) |
| saturation_method | -- | DC_sat / multi_freq / empirical |
| lift_off_mm | mm | Estimated or measured lift-off |
| orientation_deg | deg | 0 or 90 specimen rotation |
| reading_number | -- | 1..10 within each orientation |
| date_time | ISO 8601 | Timestamp |

### 3.7 Uncertainty Estimation

| Source | Typical magnitude | Evaluation method |
|--------|-------------------|-------------------|
| Instrument accuracy | 0.5 -- 1.0% IACS | Type B, manufacturer spec |
| Reference standard uncertainty | 0.3% | Type B, calibration certificate |
| Lift-off variation | 0.2 -- 0.5% | Type A, lift-off sensitivity study |
| Permeability residual (ferromagnetic) | 1 -- 5% (without saturation) | Type A/B, multi-frequency analysis |
| Temperature correction | 0.05% per 0.1 degC | Type B, RTD calibration |
| Repeatability | 0.3 -- 0.8% | Type A, std dev of 20 readings |
| Edge effect | < 0.1% if probe > 2x diameter from edge | Type B, positioning check |

**Note:** For ferromagnetic steels without DC saturation, the permeability
residual dominates.  In that case, the expanded uncertainty (k = 2) may
reach 5 -- 10%.  With DC saturation, expect U ~ 1.5 -- 3%.

---

## 4 Temperature Correction

Both methods require correction to a common reference temperature
(T_ref = 20 degC) to enable meaningful comparison across specimens measured
at slightly different ambient temperatures.

### 4.1 Correction Formula

For metals with a linear temperature coefficient of resistivity alpha
(valid over small temperature ranges):

    rho_20 = rho_T / (1 + alpha * (T - 20))

or equivalently for conductivity:

    sigma_20 = sigma_T * (1 + alpha * (T - 20))

where T is the actual specimen temperature in degC.

### 4.2 Temperature Coefficients

| Steel grade | Approximate alpha (1/degC) | Source |
|-------------|---------------------------|--------|
| AISI 1045 (normalised) | 0.0045 -- 0.0050 | Literature / to be measured |
| AISI 4140 (Q&T) | 0.0040 -- 0.0048 | Literature / to be measured |
| AISI 4340 (Q&T) | 0.0038 -- 0.0045 | Literature / to be measured |

If literature values are unavailable or insufficient for a particular heat
treatment condition, measure alpha experimentally by performing conductivity
measurements at 15, 20, 25, and 30 degC (controlled thermal chamber) and
fitting a linear regression.

### 4.3 Acceptable Temperature Range

Measurements shall be taken only when T_specimen is between 18 and 28 degC.
If the specimen temperature drifts outside this range during a measurement
series, discard the affected readings and allow re-equilibration.

---

## 5 Calibration Verification and Quality Checks

### 5.1 Daily Checks

- **Four-probe DC:** Measure the calibrated reference bar at the start and
  end of each measurement session. Record values. If either reading differs
  from the certified value by more than 1%, investigate and recalibrate.
- **Eddy current:** Measure the calibration verification standard at the
  start and end of each session and once every 10 specimens. If the reading
  drifts by more than 0.5% IACS, recalibrate the instrument.

### 5.2 Gauge R&R Study

Before commencing the main experimental campaign, conduct a Gauge R&R study
per AIAG MSA 4th edition:

- 3 operators
- 10 specimens spanning the expected conductivity range
- 3 repetitions per operator per specimen per method
- Acceptance: %GRR < 10% of the total observed variation (acceptable);
  10 -- 30% (marginal, may be acceptable with justification); > 30%
  (unacceptable, improve method).

### 5.3 Cross-Method Comparison

For every specimen in the study, both methods shall be applied.  Plot
Method A vs. Method B results and fit a linear regression. Report the
slope, intercept, R-squared, and bias. Investigate any specimen where the
two methods disagree by more than 3 times the combined expanded uncertainty.

---

## 6 Data Management

- All raw readings are stored in CSV files under `03_METHODS/data/raw/`.
- Processed (temperature-corrected, averaged) values are stored in
  `03_METHODS/data/processed/`.
- File naming: `<method>_<steel_grade>_<heat_treatment>_<date>.csv`,
  e.g., `fourprobe_4140_QT_20260315.csv`.
- A measurement log notebook (physical or electronic) shall accompany
  every session, recording operator, ambient conditions, any anomalies,
  and instrument serial numbers.
- Back up all data to the project repository within 24 h of measurement.

---

## 7 Safety Notes

- **Electrical safety:** The four-probe system operates at low voltage
  (< 1 V) and moderate current (< 10 A). Standard laboratory electrical
  safety practices apply. Ensure instruments are properly grounded.
- **Chemical safety:** Acetone and isopropanol are flammable. Use in a
  well-ventilated area away from ignition sources. Wear nitrile gloves and
  safety glasses during specimen cleaning.
- **Magnetic fields:** The AC demagnetiser and DC saturation probes produce
  strong local fields. Keep magnetic media and credit cards at least 0.5 m
  away. Persons with pacemakers must not operate the demagnetiser.

---

## References

- ASTM B193-16, *Standard Test Method for Resistivity of Electrical Conductor
  Materials*
- ASTM E1004-17, *Standard Test Method for Determining Electrical Conductivity
  Using the Electromagnetic (Eddy-Current) Method*
- JCGM 100:2008, *Evaluation of measurement data -- Guide to the expression
  of uncertainty in measurement (GUM)*
- AIAG, *Measurement Systems Analysis Reference Manual*, 4th edition
