# Evidence Matrix Data Dictionary

This document defines the columns in `evidence_matrix.csv`. Each row represents one paper's contribution of experimental data. A single paper may contribute multiple rows if it reports data for multiple steel grades or conditions.

## Column Definitions

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `paper_id` | String | BibTeX key from `library.bib`. Primary key linking to notes and citations. | `han_2010_conductivity` |
| `year` | Integer | Publication year. | `2010` |
| `steel_grade` | String | Standard steel designation (AISI/SAE, EN, DIN, or generic). | `AISI 4140` |
| `composition` | String | Key alloying elements as reported (wt.%). | `0.40C-0.80Mn-1.0Cr-0.20Mo` |
| `heat_treatment` | String | Condition: annealed, normalised, Q&T with temperature, as-rolled, etc. | `Q&T 600C` |
| `microstructure` | String | Dominant phase(s): ferrite, pearlite, bainite, martensite, tempered martensite. | `tempered martensite` |
| `conductivity_method` | String | Measurement method: `4-probe DC`, `eddy current`, `PEC`, `calculated`, `literature`. | `eddy current` |
| `conductivity_value_units` | String | Measured conductivity or resistivity with units. Use %IACS, MS/m, or micro-ohm-cm. | `3.1 %IACS` |
| `temp_C` | Integer | Measurement temperature in degrees Celsius. Blank if not reported. | `20` |
| `uncertainty` | String | Measurement uncertainty as reported (absolute, %, or confidence interval). | `+/- 0.1 %IACS` |
| `machining_process` | String | Process type: turning, milling, drilling, or N/A if no machining data. | `turning` |
| `tool` | String | Tool material and geometry (ISO designation if available). | `coated carbide CNMG 120408` |
| `cutting_params` | String | Cutting speed (m/min), feed (mm/rev), depth (mm). Format: `v=X f=Y d=Z`. | `v=200 f=0.15 d=1.5` |
| `machinability_metric` | String | Metric reported: VB (mm), Ra (um), Fc (N), tool life (min), machinability index (%). | `VB=0.3mm at T=18min` |
| `key_findings` | String | 1-3 sentence summary of main result from this data row. | `Conductivity correlated with hardness (R^2=0.92)` |
| `tags` | String | Comma-separated tags: pillar, steel family, method, etc. | `pillar_B, pillar_D, eddy_current, Q&T` |
| `link_or_doi` | String | DOI (preferred) or URL. | `10.1007/s11665-010-9596-x` |

## Notes

- **Partial data is expected.** Not all papers report all columns. Empty cells are acceptable.
- **Multiple rows per paper:** If a paper tests multiple conditions, create one row per condition.
- **Conductivity vs. resistivity:** Record as reported; note units clearly. Conversion: conductivity (MS/m) = 1 / resistivity (micro-ohm-m).
- **Machinability metric:** Record the primary metric. If multiple metrics are reported, list the most relevant one and note others in `key_findings`.
- **Literature values:** If conductivity or machinability data is compiled from other sources rather than measured, set `conductivity_method` to `literature`.
