from TauFW.PicoProducer.storage.Sample import MC as M
from TauFW.PicoProducer.storage.Sample import Data as D

# ============================================================================
# Phase-II MC samples for HLT trigger efficiency studies
# ============================================================================
#
# Input: Full Phase-II HLT NanoAOD from the 2-step cmsDriver pipeline
#   Step 1: L1T rerun  (GEN-SIM-DIGI-RAW -> + L1T objects)
#   Step 2: HLT + Nano (+ L1T -> NANOAODSIM with trigger branches)
#
# Usage:
#   pico.py set era PhaseII PhaseII/samples_PhaseII.py
#   pico.py set channel phase2_trigeff PhaseII.ModulePhase2TrigEff
#   pico.py run -y PhaseII -c phase2_trigeff -m 1000
#   pico.py submit -y PhaseII -c phase2_trigeff
#
# NOTE: Update 'storage' path to your EOS location, or set to None to
#       fetch files from DAS/xrootd directly.
# ============================================================================

storage  = "/eos/user/n/nneeraj/phase2_data"
url      = "root://eoshome-n.cern.ch/"
filelist = None
opts     = "useT1=False"

samples  = [

  # ── Z' -> tt (M=500 GeV, PU200) ──────────────────────────────────────
  M('Zprime','ZprimeToTauTau_M500',
    "zprime_full",
    store=storage, url=url, files=[storage+"/zprime_merged.root"], opts=opts,
    nfilesperjob=1),

  # ── gg -> H -> tt ─────────────────────────────────────────────────────
  # M('ggH','ggHToTauTau',
  #   "/GluGluHToTauTau_M-125_TuneCP5_14TeV-powheg-pythia8/CAMPAIGN/NANOAODSIM",
  #   store=storage, url=url, files=filelist, opts=opts),

  # ── VBF H -> tt ──────────────────────────────────────────────────────
  # M('VBF','VBFHToTauTau',
  #   "/VBFHToTauTau_M125_TuneCP5_14TeV-powheg-pythia8/CAMPAIGN/NANOAODSIM",
  #   store=storage, url=url, files=filelist, opts=opts),

  # ── DY -> tt -> mt_h (filtered) ───────────────────────────────────────
  # M('DY','DYToTauTau_MuTauh',
  #   "/DYToTauTau_MuTauh_M-50_TuneCP5_14TeV-pythia8/CAMPAIGN/NANOAODSIM",
  #   store=storage, url=url, files=filelist, opts=opts),

]
