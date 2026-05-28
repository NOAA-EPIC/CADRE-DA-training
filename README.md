# CADRE DA Training — Year 2 (2026)

This repository provides the **Year‑2 CADRE Data Assimilation (DA) training workflow**, designed
for execution on the **NOAA RDHPCS Hercules** system. It includes:

- FV3‑JEDI case setups for each daily experiment  
- Hercules‑ready job cards  
- Full diagnostics generation using the UFS‑DA Diagnostics Toolkit  
- Example outputs and reproducible experiment structure  

The Year‑2 workflow follows the UFS-DA Diagnostics CADRE 2026 session guideline and documentation:

👉 https://ufs-da-diagnostics.readthedocs.io/en/latest/cadre2026_epic.html

## EPIC Session Training Slide (PDF)

- [CADRE Year‑2 EPIC FV3‑JEDI Session Slides](docs/CADREYR2-EPIC-UFS-FV3-JEDI-sessions.pdf)

# ⚠️ Hercules System Access Before EPIC Sessions

Before the EPIC training sessions begin, please make sure you can successfully log into the
NOAA RDHPCS Hercules system. All hands‑on FV3‑JEDI and diagnostics exercises will be run on
Hercules, so having access ahead of time will make the sessions smoother.

If you run into **any system access issues** — login problems, SSH configuration, X11 setup,
module loading, or anything else — please leave a message in the CADRE Slack channel so the
instructors can help you:

Slack support for the training program:

👉 https://epicworkshops-pza9734.slack.com/archives/C0B3J9BC93Pis

### Login command

```bash
ssh -X YOUR_USERID@hercules-login.hpc.msstate.edu
```
### Verify Project Access

After logging into Hercules, confirm that your account is part of the **epic-explorer** project:

```bash
groups
```

You should see **epic-explorer** in the output.  
If it is missing, please notify the instructors via the CADRE Slack channel.

### Create Your Project Workspace

Each user should be able to create their own working directory under the project space:

```bash
mkdir -p /work2/noaa/epic-explorer/$USER
```

Verify that it exists and is writable:

```bash
ls -ld /work2/noaa/epic-explorer/$USER
```

This directory will be used for all FV3‑JEDI runs and diagnostics during the training.


# Control Case Summary (Hybrid 3DVar, C96/C48) and Quick Overview of Session Scope

**Purpose**  
Baseline *hybrid* 3DVar analysis using FV3‑JEDI for the Day‑1 training session.  
This configuration is **one of the GDASApp UFS FV3‑JEDI global‑workflow canned cases**, adapted for stand‑alone execution.

---

## 1. Core Configuration
- **DA Method:** Hybrid 3DVar  
- **Hybrid B Weights:** **12.5% static B**, **87.5% ensemble B**  
- **Analysis Resolution:** **C96**  
- **Background Resolution:** **C96**  
- **Ensemble Perturbation Resolution:** **C48**  
- **Cycle Time:** 2024‑02‑24 00Z  
- **Assimilation Window:** **6 hours** (±3 hours)  
- **Model:** FV3‑JEDI (UFS)

---

## 2. Observations Assimilated
- **Surface pressure** (SYNOP/METAR/ships/buoys)  
- **Satellite Winds:** SATWND, SCATWND  
- **GNSSRO:** bending angle  
- **ATMS Radiances:** all channels (QC‑filtered)

---

## 3. QC and Bias Correction
- Universal QC  
- Radiance QC  
- CRTM bias correction for ATMS  
- Gross check + buddy check  

---

## 4. Outputs
- Analysis increments (**C96**)  
- OMB/OMA diagnostics  
- Scan‑position diagnostics  
- Latitude‑binned statistics  
- Pre‑computed plots (increments, zonal means, histograms, scatter maps, spectra)

---

## 5. Training Focus (Day‑1 → Day‑3)

### **Day‑1: Control Experiment**
We begin with the baseline hybrid 3DVar configuration.  
This serves as the reference for all diagnostics and comparisons in Days 2–3.

---

### **Day‑2: Background‑Error Modeling**
We explore:
- Hybrid B weights (static vs ensemble contribution)  
- NICAS horizontal length‑scale parameters  
- How background‑error structure shapes increment patterns and flow dependence  

---

### **Day‑3: ATMS Observation Thinning & Error Inflation**
We examine:
- ATMS Gaussian thinning  
- ATMS observation‑error inflation  
- Channel grouping and error specification  
- Jo/p and chi‑squared diagnostics  

---

## 6. ATMS Single‑Observation Case
A dedicated **single‑observation experiment** is also provided:

- One randomly selected **tropical** ATMS footprint  
- **22 ATMS channels** assimilated  
- Input FV3‑JEDI and GDASApp YAMLs are prepared under: year2_cases/input_yaml/single_obs/
- 
The **experiment procedure is identical** to the full‑observation cases.

This single‑obs setup provides a **direct, intuitive view** of:
- How the **background‑error model (B‑model)** controls the *horizontal and vertical spread* of increments  
- How **observation‑error settings** (per‑channel error, inflation) control the *magnitude* of increments  
- How a single radiance produces a physically interpretable increment pattern  

This case is used in Days 2–3 to illustrate the impact of:
- Hybrid B weights and NICAS length scales  
- ATMS thinning and observation‑error inflation  

---

## 7. Pre‑Run Diagnostic Outputs (Reference)

Pre‑computed diagnostic outputs for all Year‑2 cases are available in the feature branch:

https://github.com/jkbk2004/CADRE-DA-training/tree/diag-results/diagnostic/results/year2_cases

These include:
- **Spectral analysis**  
- **Increment maps**  
- **Observation‑space diagnostics** (OMB/OMA, scan‑position, lat‑binned)  
- **OMB scatter plots**  
- **JEDI log summaries** (Jo/Jb breakdown, QC counts)

These reference outputs allow participants to:
- Verify their own runs  
- Compare Day‑1 control results with Days 2–3 sensitivity experiments  
- Understand how B‑model settings and observation‑error choices affect increments and diagnostics  

---

