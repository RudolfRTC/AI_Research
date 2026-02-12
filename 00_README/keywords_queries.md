# Search Keywords and Query Strings

## Databases
- Google Scholar (broad coverage)
- Scopus (engineering focus)
- Web of Science (citation tracking)
- IEEE Xplore (sensors, measurement)
- ASTM / ISO standards portals

---

## Pillar A: Machinability of Low-Alloy Steels

### Core queries
```
"machinability" AND "low-alloy steel"
"machinability" AND ("AISI 4140" OR "AISI 4340" OR "AISI 1045")
"tool wear" AND "steel" AND ("cutting forces" OR "surface roughness")
"machinability index" AND "steel"
"machining" AND "hardened steel" AND "tool life"
```

### Extended queries
```
"chip formation" AND "steel" AND "microstructure"
"specific cutting energy" AND "steel grade"
"machinability rating" AND "AISI" AND "B1112"
"turning" AND "low-alloy steel" AND "flank wear"
```

### Scopus field-coded
```
TITLE-ABS-KEY("machinability" AND "low-alloy steel" AND ("tool wear" OR "cutting force"))
TITLE-ABS-KEY("machining" AND "AISI 4140" AND "surface roughness")
```

---

## Pillar B: Electrical Conductivity and Microstructure

### Core queries
```
"electrical conductivity" AND "steel" AND "microstructure"
"electrical resistivity" AND "low-alloy steel"
"resistivity" AND ("grain size" OR "phase" OR "precipitate") AND "steel"
"eddy current" AND "microstructure" AND "steel"
"Matthiessen's rule" AND "steel"
```

### Extended queries
```
"electrical resistivity" AND ("martensite" OR "pearlite" OR "bainite" OR "ferrite")
"conductivity" AND "heat treatment" AND "steel"
"electron scattering" AND "grain boundary" AND "metal"
"resistivity" AND "carbon content" AND "steel"
```

### Scopus field-coded
```
TITLE-ABS-KEY("electrical resistivity" AND "microstructure" AND "steel")
TITLE-ABS-KEY("conductivity" AND ("grain size" OR "phase fraction") AND "steel")
```

---

## Pillar C: Measurement Methods

### Core queries
```
"four-probe" AND "resistivity" AND "metal"
"eddy current" AND "conductivity measurement" AND "ferromagnetic"
"ASTM B193" AND "resistivity"
"ASTM E1004" AND "eddy current" AND "conductivity"
"contactless" AND "conductivity" AND "steel"
```

### Extended queries
```
"Kelvin" AND "four-point probe" AND "metal"
"eddy current" AND "frequency" AND "permeability" AND "steel"
"impedance" AND "eddy current" AND "ferromagnetic"
"calibration" AND "conductivity" AND "reference standard"
"measurement uncertainty" AND "resistivity" AND "metal"
```

### IEEE Xplore specific
```
("eddy current" AND "conductivity" AND "steel") in All Metadata
("four point probe" AND "resistivity" AND "measurement") in All Metadata
```

---

## Pillar D: Bridging and Predictive Models

### Core queries
```
"machine learning" AND "machinability" AND "prediction"
"neural network" AND "tool wear" AND "prediction"
"conductivity" AND "mechanical properties" AND "prediction" AND "steel"
"support vector" AND "machining" AND "prediction"
"random forest" AND "surface roughness" AND "prediction"
```

### Extended queries
```
"online monitoring" AND "tool wear" AND "sensor"
"indirect measurement" AND "machinability"
"non-destructive" AND "machinability" AND "steel"
"artificial intelligence" AND "cutting" AND "steel"
"regression" AND "tool life" AND "steel"
```

### Scopus field-coded
```
TITLE-ABS-KEY("machine learning" AND "machinability" AND "steel")
TITLE-ABS-KEY("prediction" AND "tool wear" AND ("neural network" OR "SVM" OR "random forest"))
```

---

## Cross-Pillar / Novel Combinations

```
"electrical conductivity" AND "machinability"
"resistivity" AND "machinability" AND "steel"
"eddy current" AND "machinability"
"non-destructive testing" AND "machinability" AND "prediction"
"conductivity" AND "tool wear" AND "steel"
"electrical properties" AND "cutting" AND "steel"
```

---

## Alert Setup

Set Google Scholar alerts for the top 5 cross-pillar queries above. Review monthly. See `06_NEWS_WATCH/alerts.md` for detailed alert configuration.
