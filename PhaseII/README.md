# Phase-II Tau Trigger Efficiency Studies (TauFW Integration)

This directory contains the plotting and analysis tools for Phase-II HLT tau trigger
efficiency studies. The analysis module and configuration live inside `PicoProducer/python/analysis/PhaseII/`, following the same convention as `Tau_trig_SF_studies`.

---

## Supported Channels

| Channel    | Gen Selection | HLT Path | L1 Seed | Status |
|------------|--------------|----------|---------|--------|
| **MuTau**     | 1 GenVisTau + 1 gen μ | `HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1` | `L1T_PuppiTauTkMuon_42_18` | ✅ Working |
| **DiTau**     | 2 GenVisTau | `HLT_DoubleMediumDeepTauPFTauHPS35_eta2p1` | `L1T_DoublePuppiTau_52_52` | ✅ Working |
| **ETau**      | 1 GenVisTau + 1 gen e | `HLT_Ele30_WPTight_L1Seeded_LooseDeepTauPFTauHPS30_eta2p1_CrossL1` | `L1T_PuppiTauTkIsoEle_45_22` | ✅ Working |
| **SingleTau** | 1 GenVisTau (pT>130) | Not in menu | Not in menu | ⚠️ Trigger not defined |

---

## Input Data

The framework takes **Phase-II HLT NanoAOD** as input, produced via a
two-step `cmsDriver.py` pipeline:

1. **Step 1:** L1T rerun (GEN-SIM-DIGI-RAW → + L1T objects)
2. **Step 2:** HLT + NanoAOD (+ L1T → NANOAODSIM with HLT + L1T trigger branches)

The NanoAOD contains:
- `hltHpsPFTau_*` — HLT tau objects (pT, η, φ, deepTau scores, etc.)
- `hltMuon_*` — HLT muon objects
- `hltElectron_*` — HLT electron objects (pT, η, φ, isolation, etc.)
- `hltAK4PuppiJet_*` — HLT jet objects
- `L1T_*` — L1 trigger seed decisions (from the NanoAOD alias fix)
- `HLT_*` — HLT path decisions
- `GenVisTau_*`, `GenPart_*` — Generator-level objects

---

## Installation and Setup

### 1. Create and initialize CMSSW environment

```bash
cmsrel CMSSW_16_0_0_pre2
```
```bash
cd CMSSW_16_0_0_pre2/src
```
```bash
cmsenv
```

### 2. Clone NanoAOD-tools (if not already present)

```bash
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
```
```bash
scram b -j4
```

### 3. Clone TauFW and switch to the Phase-II branch

> **Important:** The Phase-II trigger efficiency code is on the
> `PhaseII_integration` branch, **not** on `main`. You must switch to it
> after cloning.

```bash
git clone https://github.com/neeraj-1729/TauFW.git TauFW
```
```bash
cd TauFW
```
```bash
git checkout PhaseII_integration
```
```bash
cd ..
```
```bash
scram b -j4
```
```bash
cmsenv
```

### 4. Verify installation

```bash
python3 -c "
from TauFW.PicoProducer.analysis.PhaseII.ModulePhase2TrigEff import ModulePhase2TrigEff
print('Import OK')
"
```

---

## Environment Setup (New Sessions)

```bash
cd CMSSW_16_0_0_pre2/src
```
```bash
cmsenv
```
```bash
export X509_USER_PROXY=/afs/cern.ch/user/<username>/x509up_proxy
```
```bash
voms-proxy-init --voms cms --valid 192:00 --out $X509_USER_PROXY
```
```bash
cd TauFW/PicoProducer
```

> **Note:** The proxy must be on AFS (not `/tmp/`) so that HTCondor worker
> nodes can access it. Add the `export X509_USER_PROXY=...` line to your
> `~/.bashrc` for convenience.

---

## Workflow Overview

The analysis follows a two-step workflow:

```
Phase-II HLT NanoAOD ──→ [Skim Module] ──→ pico.root ──→ [Plotter --channel] ──→ plots/
     (full NanoAOD)     ModulePhase2TrigEff   (flat tree)     (channel cuts)
```

1. **Skim:** Run the unified `ModulePhase2TrigEff` module on the full HLT NanoAOD.
   This saves all gen-level and HLT reco objects + trigger decisions into a flat tree.
   **No channel-specific cuts** — the same output works for ALL channels.

2. **Plot:** Run the plotter with `--channel` to select MuTau, DiTau, ETau, or
   SingleTau. Channel-specific selections are applied at this stage.

---

## Running the Analysis

### 1. Configure the era and channel

Update `PicoProducer/samples/PhaseII/samples_PhaseII.py` — set `storage` to your EOS path
or keep `None` for DAS/xrootd access.

Then register:

```bash
pico.py set era PhaseII PhaseII/samples_PhaseII.py
```
```bash
pico.py set channel phase2_trigeff PhaseII.ModulePhase2TrigEff
```

### 2. Local test run

```bash
pico.py run -y PhaseII -c phase2_trigeff -m 1000
```

### 3. Submit batch jobs

```bash
pico.py submit -y PhaseII -c phase2_trigeff
```

### 4. Monitor job status

```bash
pico.py status -y PhaseII -c phase2_trigeff
```

### 5. Resubmit failed jobs

```bash
pico.py resubmit -y PhaseII -c phase2_trigeff
```

### 6. Merge output files

```bash
pico.py hadd -y PhaseII -c phase2_trigeff
```

---

Now lets move to the plotting part. Lets move to the working directory of the Plotting tools.
```bash
cd ../PhaseII
```

## Plotting Trigger Efficiencies

Generate efficiency plots from the merged output. The **same pico file works for
all channels** — just change `--channel`:

```bash
# MuTau
python3 plot_phase2_trigeff.py \
  --input /eos/user/<username>/analysis/Phase2/Zprime/ZprimeToTauTau_M500_phase2_trigeff.root \
  --channel mutau \
  --outdir plots_mutau/ \
  --sample-label "Z'→ττ M500 (Phase-II)"
```
```bash
# DiTau (same input!)
python3 plot_phase2_trigeff.py \
  --input /eos/user/<username>/analysis/Phase2/Zprime/ZprimeToTauTau_M500_phase2_trigeff.root \
  --channel ditau \
  --outdir plots_ditau/
```

### Output Plots

| Plot | Description |
|------|-------------|
| `cutflow_<ch>.png` | Step-by-step cutflow bar chart |
| `eff_<ch>_vs_<var>_pt.png` | pT turn-on curve (no pT cut on plotted leg) |
| `eff_<ch>_vs_<var>_eta.png` | η efficiency |
| `eff_<ch>_vs_<var>_phi.png` | φ efficiency |
| `trigeff_<ch>.pdf` | **Combined PDF** with all plots for the channel in order: HLT eff → L1 eff → HLT fakes → L1 fakes |

> **Note:** The combined PDF is generated automatically alongside the PNGs.
> Use `--no-pdf` to skip it.

---

## File Structure

```
TauFW/
├── PicoProducer/
│   ├── python/analysis/PhaseII/          # ★ Analysis module + config
│   │   ├── __init__.py
│   │   ├── ModulePhase2TrigEff.py        # Unified skim module (all channels)
│   │   └── Phase2TriggerConfig.py        # Central config: channels, L1, HLT, binning
│   └── samples/PhaseII/
│       └── samples_PhaseII.py            # Sample definitions (used by pico.py)
├── PhaseII/                              # ★ Plotting tools + documentation
│   ├── plot_phase2_trigeff.py            # Efficiency plotter (--channel at plot time)
│   └── README.md                         # This file
```

---

## Efficiency Definition

```
Efficiency = (Gen Sel. + Reco Sel. + Trigger + Gen-Reco Match)
           / (Gen Sel. + Reco Sel.)
```

- **Gen Sel.:** Channel-specific gen-level selection (GenVisTau, GenPart)
- **Reco Sel.:** Channel-specific HLT object selection (hltHpsPFTau, hltMuon, hltElectron)
- **Trigger:** HLT path fires
- **Matching:** dR(gen, reco) < 0.1 for all legs

### Turn-on Curve Convention

For pT turn-on plots: do NOT apply the pT cut on the leg being plotted,
DO apply it for the other leg(s).

---

## Notes

- The skim module runs on **full Phase-II HLT NanoAOD** — no pre-slimming needed.
- Missing HLT branches (e.g., SingleTau) are automatically
  detected and skipped with a warning.
- The unified module applies only a loose |η| < 2.5 preselection. All physics
  cuts (pT, η=2.1, dR, matching) are applied at the plotting stage.
- Replace `<username>` with your CERN username in all EOS paths.
- Ensure your grid proxy is valid and on AFS for batch job access.

---

## Contact

**Author:** Neeraj  
For questions, please contact: neeraj.neeraj@cern.ch
