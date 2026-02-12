# Turning Test Protocol (ISO 3685)

## Overview

This protocol defines a standardised longitudinal turning procedure for
evaluating the machinability of three low-alloy steel grades (AISI 1045, 4140,
4340). The procedure follows ISO 3685:1993 *Tool-life testing with single-point
turning tools* and provides the machining data required to correlate with
electrical conductivity measurements (RQ1).

---

## 1 Steel Grades and Heat Treatments

### 1.1 Materials

| Grade | UNS | Nominal composition (wt%) | Supply form |
|-------|-----|--------------------------|-------------|
| AISI 1045 | G10450 | 0.43-0.50 C, 0.60-0.90 Mn | Hot-rolled bar, dia 80-100 mm |
| AISI 4140 | G41400 | 0.38-0.43 C, 0.75-1.0 Mn, 0.80-1.10 Cr, 0.15-0.25 Mo | Hot-rolled bar, dia 80-100 mm |
| AISI 4340 | G43400 | 0.38-0.43 C, 0.60-0.80 Mn, 0.70-0.90 Cr, 0.20-0.30 Mo, 1.65-2.00 Ni | Hot-rolled bar, dia 80-100 mm |

### 1.2 Heat Treatment Conditions

Each grade shall be tested in at least three conditions to span a range of
microstructures and hardness values:

| Condition code | Treatment | Target microstructure |
|---------------|-----------|----------------------|
| AR | As-received (hot-rolled) | Ferrite + pearlite (1045); ferrite + pearlite/bainite (4140, 4340) |
| N | Normalised: austenitise at grade-specific T_aust, air cool | Refined ferrite + pearlite |
| QT | Quench and temper: austenitise, oil quench, temper at T_temper | Tempered martensite |

Specific austenitising and tempering temperatures:

| Grade | T_aust (degC) | Soak time (min) | Quench medium | T_temper (degC) | Temper time (min) |
|-------|---------------|-----------------|---------------|-----------------|-------------------|
| AISI 1045 | 850 | 45 | Oil (60 degC) | 550 | 60 |
| AISI 4140 | 845 | 45 | Oil (60 degC) | 550 | 90 |
| AISI 4340 | 845 | 45 | Oil (60 degC) | 540 | 120 |

After heat treatment, verify hardness (3 measurements at 120 deg spacing on
the cross-section) and record mean HRC +/- std dev.

### 1.3 Specimen Preparation for Turning

1. Machine each bar to a uniform diameter of 80.0 +/- 0.1 mm and overall
   length of 300 mm (minimum).
2. Face both ends and centre-drill (BS1 centre) for tailstock support.
3. Remove the decarburised surface layer: take a clean-up cut of >= 2 mm
   depth over the full test length before any data-generating passes.
4. From each bar, cut two conductivity test coupons (see
   `conductivity_protocol.md`) from the end off-cut so that conductivity
   and machinability data are from the same material batch and heat treatment.

---

## 2 Tool Selection

### 2.1 Insert Specification

| Parameter | Specification |
|-----------|--------------|
| Insert geometry | CNMG 120408 (ISO designation) |
| Substrate | Cemented carbide, ISO P20-P30 grade |
| Coating | CVD TiCN/Al2O3/TiN multilayer, total thickness 10-15 um |
| Chipbreaker | Medium (manufacturer's general-purpose geometry for steel) |
| Manufacturer | Specify one manufacturer for the entire study to eliminate inter-brand variability (e.g., Sandvik Coromant, Kennametal, or equivalent) |

### 2.2 Tool Holder

| Parameter | Specification |
|-----------|--------------|
| Holder designation | DCLNR/L 2525M12 (ISO) |
| Approach angle (kappa_r) | 95 deg |
| Inclination angle (lambda_s) | -6 deg |
| Rake angle (gamma_o) | -6 deg |
| Overhang | <= 1.5x shank cross-section |

### 2.3 Tool Management

- Use a **fresh cutting edge** for every tool-life test. Each CNMG insert has
  8 usable edges (4 corners x 2 sides); track edge usage on a tool log sheet.
- Inspect each new edge under a stereo microscope (20x) before use. Reject
  edges with visible coating defects, chipping, or grinding marks.
- Store inserts in their original packaging to prevent damage.

---

## 3 Machine Tool and Setup

### 3.1 Lathe Requirements

| Parameter | Requirement |
|-----------|-------------|
| Type | CNC or engine lathe with infinitely variable speed |
| Spindle power | >= 15 kW (sufficient for highest v_c at full depth) |
| Speed range | 50 -- 3000 rpm (to cover all v_c values) |
| Feed drive | Servo or gearbox capable of 0.05 -- 0.50 mm/rev |
| Coolant | Dry cutting (no coolant) -- simplifies thermal analysis and is consistent with many machinability rating standards |
| Stiffness | Verify no chatter at highest cutting parameters before starting |

### 3.2 Workpiece Mounting

- Mount between centres with a face driver (preferred) or chuck-and-centre.
  If using a 3-jaw chuck, verify run-out < 0.02 mm TIR.
- Support with a live tailstock centre.
- Minimum unsupported length / diameter ratio: L/D < 4 to avoid flexure.
  If the test length exceeds L/D = 4, use a steady rest.

### 3.3 Dynamometer Setup (for Cutting Force Measurement)

| Parameter | Specification |
|-----------|--------------|
| Dynamometer type | Piezoelectric 3-component tool dynamometer (e.g., Kistler 9257B or equivalent) |
| Channels | Fc (cutting / tangential), Ff (feed), Fp (passive / radial) |
| Sensitivity | Sufficient for forces in range 100 -- 3000 N |
| Sampling rate | >= 5 kHz per channel |
| Charge amplifier | Matched to dynamometer, with low-pass filter at 1 kHz |
| Mounting | Dynamometer bolted to cross-slide; tool holder mounted on dynamometer |

Calibrate the dynamometer with certified weights before the first test series
and verify at least once per week during the campaign.

---

## 4 Cutting Parameters

### 4.1 Standard Parameter Set

All three grades shall be tested under a common set of cutting parameters to
enable direct comparison.

| Parameter | Symbol | Value(s) | Units |
|-----------|--------|----------|-------|
| Cutting speed | v_c | 150, 200, 250, 300 | m/min |
| Feed rate | f | 0.20 | mm/rev |
| Depth of cut | a_p | 1.5 | mm/rev |

This gives 4 speed levels x 3 grades x 3 heat treatments = 36 tool-life
tests at a minimum. If resources permit, an extended parameter set adds
additional feed and depth levels.

### 4.2 Extended Parameter Set (Optional)

| Parameter | Symbol | Additional values | Units |
|-----------|--------|-------------------|-------|
| Feed rate | f | 0.10, 0.30 | mm/rev |
| Depth of cut | a_p | 0.5, 2.5 | mm |

This allows investigation of RQ1d (effect of cutting parameters on the
conductivity-machinability relationship).

### 4.3 Calculating Spindle Speed

For each cutting speed and current workpiece diameter d:

    n = (1000 * v_c) / (pi * d)

Recalculate and update n as the workpiece diameter decreases with successive
passes. Maintain v_c within +/- 2% of the target value.

---

## 5 Measurement Procedures

### 5.1 Flank Wear (VB)

#### Equipment
- Stereo microscope or tool-maker's microscope, magnification >= 30x
- Calibrated reticle or digital image analysis software
- Specimen holder for inserts

#### Procedure
1. Stop the cut at predetermined intervals. For the initial pass, inspect at
   1 min, 2 min, 5 min, then every 5 min thereafter. Adjust intervals to
   capture the wear curve adequately (more frequent near end of life).
2. Remove the insert from the holder without rotating it or damaging the wear
   land.
3. Clean the insert with compressed air. Do not use abrasive cleaning.
4. Place the insert under the microscope with the flank face perpendicular to
   the optical axis.
5. Measure the **average flank wear VB** over the region of contact
   (Zone B per ISO 3685) -- typically the central third of the active cutting
   edge, excluding the nose radius zone and the notch wear zone.
6. Also record the **maximum flank wear VB_max** (anywhere on the flank face).
7. Photograph the wear land at each inspection interval for archival and
   potential re-analysis.
8. Re-mount the insert in the holder in the **same position and orientation**.
   Verify seating before resuming the cut.

#### Tool Life Criterion

| Criterion | Threshold | Definition |
|-----------|-----------|------------|
| Primary | VB = 0.3 mm | Average flank wear |
| Secondary | VB_max = 0.6 mm | Maximum flank wear at any point |
| Catastrophic | -- | Sudden fracture, chipping > 0.5 mm, or plastic deformation of the cutting edge |

Tool life T is the cutting time (min) at which the first criterion is reached.
If VB does not reach 0.3 mm within 45 min of cutting (at a given v_c), record
T > 45 min and use the final VB value for correlation analysis.

### 5.2 Surface Roughness (Ra)

#### Equipment
- Contact-type stylus profilometer (e.g., Mitutoyo SJ-410 or equivalent)
- Stylus tip radius: 2 um (per ISO 4287)
- Cutoff wavelength lambda_c: 0.8 mm
- Evaluation length: 4.0 mm (= 5 x lambda_c)

#### Procedure
1. Measure Ra on the freshly machined surface at each wear inspection
   interval (same stop points as for VB).
2. Take 3 measurements at circumferential positions spaced 120 deg apart,
   each along the axial direction of the workpiece.
3. Record individual values and compute the mean Ra for that inspection point.
4. Also record Rz (maximum height) as a secondary roughness metric.
5. Ensure the measurement is taken >= 5 mm from the workpiece edge to avoid
   end effects.

### 5.3 Cutting Forces (Fc, Ff, Fp)

#### Procedure
1. Record cutting forces continuously throughout each pass using the
   3-component dynamometer.
2. For analysis, extract a **steady-state segment** of at least 5 s duration,
   avoiding the entry and exit transients.
3. Compute the mean and standard deviation of Fc (tangential / main cutting
   force), Ff (feed force), and Fp (passive / radial force) over the
   steady-state segment.
4. Record forces at each wear inspection interval. As VB increases, forces
   are expected to rise; capturing this trend is essential for RQ1.
5. Compute specific cutting force k_c:

       k_c = Fc / (a_p * f)    [N/mm^2]

6. Store raw force-time data in binary or CSV format for possible
   re-analysis.

### 5.4 Chip Form (Supplementary)

At each wear inspection interval, collect a representative chip sample:
1. Photograph the chip against a millimetre-scale grid.
2. Classify chip type per ISO 3685 Annex A (continuous, segmented, spiral,
   arc, etc.).
3. Measure chip thickness t_c with a micrometer (for chip compression ratio
   calculation).

---

## 6 Test Execution Sequence

For each combination of steel grade, heat treatment, and cutting speed:

1. Mount a fresh workpiece (clean-up pass already completed).
2. Install a fresh, inspected cutting edge.
3. Set the spindle speed for the target v_c at the current workpiece diameter.
4. Start data acquisition (dynamometer, time).
5. Engage the feed and begin cutting.
6. At each predetermined stop time:
   a. Disengage feed and retract tool.
   b. Stop spindle.
   c. Measure VB and VB_max.
   d. Measure Ra (3 positions).
   e. Photograph tool and chip.
   f. Record forces from the preceding pass.
   g. If VB < 0.3 mm and no catastrophic failure: re-mount tool, update
      spindle speed for reduced diameter if needed, resume cutting.
   h. If VB >= 0.3 mm or VB_max >= 0.6 mm or catastrophic failure: record
      tool life T, stop test.
7. Record all data in the test log (see Section 7).
8. Proceed to the next cutting speed or specimen.

---

## 7 Data Recording

### 7.1 Test Log Entry (One Row per Inspection Interval)

| Column | Units | Description |
|--------|-------|-------------|
| test_id | -- | Unique test identifier: `<grade>-<HT>-<vc>-<rep>` |
| specimen_id | -- | Links to conductivity specimen ID |
| steel_grade | -- | AISI designation |
| heat_treatment | -- | AR / N / QT |
| hardness_HRC | HRC | Mean hardness of test bar |
| cutting_speed_m_min | m/min | Target v_c |
| feed_mm_rev | mm/rev | Feed rate f |
| depth_of_cut_mm | mm | Depth a_p |
| cutting_time_min | min | Cumulative cutting time at inspection |
| VB_mm | mm | Average flank wear |
| VB_max_mm | mm | Maximum flank wear |
| Ra_um | um | Mean surface roughness (3 measurements) |
| Ra_std_um | um | Std dev of Ra measurements |
| Rz_um | um | Mean maximum height |
| Fc_N | N | Mean tangential cutting force |
| Fc_std_N | N | Std dev of Fc |
| Ff_N | N | Mean feed force |
| Fp_N | N | Mean passive force |
| kc_N_mm2 | N/mm^2 | Specific cutting force |
| chip_type | -- | ISO 3685 classification |
| notes | -- | Anomalies, chatter, built-up edge, etc. |
| date_time | ISO 8601 | Timestamp |

### 7.2 Summary Table (One Row per Tool-Life Test)

| Column | Units | Description |
|--------|-------|-------------|
| test_id | -- | As above |
| specimen_id | -- | As above |
| steel_grade | -- | AISI designation |
| heat_treatment | -- | AR / N / QT |
| hardness_HRC | HRC | Mean hardness |
| sigma_IACS_pct | %IACS | Paired conductivity from `conductivity_protocol.md` |
| cutting_speed_m_min | m/min | v_c |
| feed_mm_rev | mm/rev | f |
| depth_of_cut_mm | mm | a_p |
| tool_life_min | min | T at VB = 0.3 mm |
| failure_mode | -- | VB / VB_max / catastrophic |
| Ra_at_end_um | um | Ra at final inspection |
| Fc_at_start_N | N | Fc at first inspection (fresh tool) |
| Fc_at_end_N | N | Fc at final inspection (worn tool) |

---

## 8 Repeatability

- Perform a minimum of **2 replicates** for every (grade, heat treatment,
  cutting speed) combination.
- If tool life results for the two replicates differ by more than 20%,
  conduct a third replicate. Report the median.
- Total minimum number of tool-life tests: 4 speeds x 3 grades x 3 heat
  treatments x 2 replicates = **72 tests**.

---

## 9 Safety

- **Machine safety:** Follow all lathe operating procedures. Use guards,
  interlocks, and appropriate PPE (safety glasses, face shield for dry
  cutting, steel-toed shoes). No loose clothing or jewellery.
- **Hot chips and workpieces:** Dry cutting produces hot chips and raises
  workpiece temperature. Use chip shields. Handle workpieces with heat-
  resistant gloves after cutting.
- **Dust and fumes:** Dry machining of steel may produce fine particles.
  Use local exhaust ventilation (LEV) or ensure adequate general ventilation.
- **Noise:** Machining can exceed 85 dB(A). Wear hearing protection in
  accordance with local regulations.

---

## References

- ISO 3685:1993, *Tool-life testing with single-point turning tools*
- ISO 4287:1997, *Geometrical product specifications (GPS) -- Surface texture:
  Profile method -- Terms, definitions and surface texture parameters*
- ASTM E112-13, *Standard Test Methods for Determining Average Grain Size*
- Kistler, *Multicomponent Dynamometer Type 9257B Data Sheet*
