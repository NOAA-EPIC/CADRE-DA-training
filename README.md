# CADRE DA Training — Year 2 (2026)

This repository provides the **Year‑2 CADRE Data Assimilation (DA) training workflow**, designed
for execution on the **NOAA RDHPCS Hercules** system. It includes:

- FV3‑JEDI case setups for each daily experiment  
- Hercules‑ready job cards  
- Full diagnostics generation using the UFS‑DA Diagnostics Toolkit  
- Example outputs and reproducible experiment structure  

The Year‑2 workflow follows the UFS-DA Diagnostics CADRE 2026 session guideline and documentation:

👉 https://ufs-da-diagnostics.readthedocs.io/en/latest/cadre2026_epic.html

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


# Year‑1 (2024–2025) — Legacy Materials

The original CADRE Year‑1 training materials are preserved for reference and will be reorganized
into a dedicated section.

**Documentation:**
- Simplified [documentation for the CADRE DA Training 2025](https://cadre-da-training.readthedocs.io/en/main/BuildingRunningTesting/CADRE-Container.html)
- Commands listed in [cadre-epic-commands.md](https://github.com/NOAA-EPIC/CADRE-DA-training/blob/main/Day2/cadre-epic-commands.md)

**Hands-On Training Slides:**
- [SSH Slides (for Mac, Windows, PuTTy)](https://github.com/NOAA-EPIC/CADRE-DA-training/tree/main/Day1)
- [Containers](https://github.com/NOAA-EPIC/CADRE-DA-training/blob/main/Day1/CADRE_Workshop_Container.pdf)
- [Running the Land DA System](https://github.com/NOAA-EPIC/CADRE-DA-training/blob/main/Day2/LandDAPracticalTraining_Day2_Petro.pdf)

**Relevant Repositories:**
- CADRE-DA-training: https://github.com/NOAA-EPIC/CADRE-DA-training

