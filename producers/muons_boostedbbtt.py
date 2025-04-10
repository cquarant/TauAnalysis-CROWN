from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for loosest selection of Muons
####################

MuonPtCut = Producer(
    name="MuonPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {LooseMuon_pt})",
    input=[nanoAOD.Muon_pt],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)

MuonEtaCut = Producer(
    name="MuonEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {LooseMuon_eta})",
    input=[nanoAOD.Muon_eta],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
MuonDxyCut = Producer(
    name="MuonDxyCut",
    call="physicsobject::CutDxy({df}, {input}, {output}, {LooseMuon_dxy})",
    input=[nanoAOD.Muon_dxy],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
MuonDzCut = Producer(
    name="MuonDzCut",
    call="physicsobject::CutDz({df}, {input}, {output}, {LooseMuon_dz})",
    input=[nanoAOD.Muon_dz],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
MuonIDCut = Producer(
    name="MuonIDCut",
    call='physicsobject::muon::CutID({df}, {output}, "{muon_id}")',
    input=[],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
MuonIsoCut = Producer(
    name="MuonIsoCut",
    call="physicsobject::muon::CutIsolation({df}, {output}, {input}, {LooseMuon_miniPFRelIso_all})",
    input=[nanoAOD.Muon_miniPFRelIso_all],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
BaseMuons = ProducerGroup(
    name="BaseMuons",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.base_muons_mask],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
    subproducers=[
        MuonPtCut,
        MuonEtaCut,
        MuonDxyCut,
        MuonDzCut,
        MuonIDCut,
        MuonIsoCut,
    ],
)

LooseMuonsVeto = Producer(
    name="LooseMuonsVeto",
    call="physicsobject::LeptonVetoFlag({df}, {output}, {input})",
    input=[q.base_muons_mask],
    output=[q.Loose_muon_veto_flag],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)

NumberOfLooseMuons = Producer(
    name="NumberOfLooseMuons",
    call="quantities::NumberOfGoodLeptons({df}, {output}, {input})",
    input=[q.base_muons_mask],
    output=[q.n_Loose_muons],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
