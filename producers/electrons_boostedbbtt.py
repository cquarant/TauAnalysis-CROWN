from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for loosest selection of electrons
####################

ElectronPtCut = Producer(
    name="ElectronPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {LooseEle_pt})",
    input=[nanoAOD.Electron_pt],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)

ElectronEtaCut = Producer(
    name="ElectronEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {LooseEle_eta})",
    input=[nanoAOD.Electron_eta],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
ElectronDxyCut = Producer(
    name="ElectronDxyCut",
    call="physicsobject::CutDxy({df}, {input}, {output}, {LooseEle_dxy})",
    input=[nanoAOD.Electron_dxy],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
ElectronDzCut = Producer(
    name="ElectronDzCut",
    call="physicsobject::CutDz({df}, {input}, {output}, {LooseEle_dz})",
    input=[nanoAOD.Electron_dz],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
ElectronIDCut = Producer(
    name="ElectronIDCut",
    call='physicsobject::electron::CutID({df}, {output}, "{ele_id}")',
    input=[],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
ElectronIsoCut = Producer(
    name="ElectronIsoCut",
    call="physicsobject::electron::CutIsolation({df}, {output}, {input}, {LooseEle_miniPFRelIso_all})",
    input=[nanoAOD.Electron_miniPFRelIso_all],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
BaseElectrons = ProducerGroup(
    name="BaseElectrons",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.base_electrons_mask],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
    subproducers=[
        ElectronPtCut,
        ElectronEtaCut,
        ElectronDxyCut,
        ElectronDzCut,
        ElectronIDCut,
        ElectronIsoCut,
    ],
)

LooseElectronsVeto = Producer(
    name="LooseElectronsVeto",
    call="physicsobject::LeptonVetoFlag({df}, {output}, {input})",
    input=[q.base_electrons_mask],
    output=[q.Loose_electron_veto_flag],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)

NumberOfLooseElectrons = Producer(
    name="NumberOfLooseElectrons",
    call="quantities::NumberOfGoodLeptons({df}, {output}, {input})",
    input=[q.base_electrons_mask],
    output=[q.n_Loose_electrons],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
