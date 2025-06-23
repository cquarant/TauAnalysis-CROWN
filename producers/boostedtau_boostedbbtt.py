from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup, Filter

####################
# Set of producers used for loosest selection of electrons
####################

##need to add call
TauFatJetdR = Producer(
    name="TauFatJetdR",
    call="quantities::boostedbbtt::dR_tau_fatjet0({df}, {output}, {input})",
    input=[
        q.fatjet_p4_0, 
        nanoAOD.boostedTau_pt,
        nanoAOD.boostedTau_eta, 
        nanoAOD.boostedTau_phi,
        nanoAOD.boostedTau_mass,
        ],
    output=[q.dR_tau_Fatjet],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

TauFatJetdRCut = Producer(
    name="TauFatJetdRCut",
    call="physicsobject::CutVarMax({df}, {input}, {output}, {min_fatjet_dR})",
    input=[q.dR_tau_Fatjet],
    output=[],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

BaseBoostedTaus = ProducerGroup(
    name="BaseBoostedTaus",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.base_BoostedTau_mask],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
    subproducers=[
        TauFatJetdRCut,
    ],
)

BoosetedTauCollection = Producer(
    name="BoosetedTauCollection",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[
        nanoAOD.boostedTau_pt, 
        q.base_BoostedTau_mask,
        ],
    output=[q.base_BoostedTau_collection],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

NumberOfBoostTaus = Producer(
    name="NumberOfBoostTaus",
    call="quantities::NumberOfGoodObjects({df}, {output}, {input})",
    input=[q.base_BoostedTau_mask],
    output=[q.nBoostTaus],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)
NBoostTauFlag = Producer(
    name="NBoostTauFlag",
    call='physicsobject::flagNumObject({df}, {output}, {input}, {nBoostedTau_min}, ">=")',
    input=[q.nBoostTaus],
    output=[],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)
# call='basefunctions::FilterThreshold({df}, {input}, {FullyBoosted_good_nfatjets}, ">=", "Number of fatjets >= 1")',
FilterNBoostTaus = Filter(
    name="FilterNBoostTaus",
    call='basefunctions::FilterFlagsAny({df}, "Number of BoostTaus >= 2", {input})',
    input=[],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
    subproducers=[NBoostTauFlag]
)


NBoostTauFlag_veto = Producer(
    name="NBoostTauFlag_veto",
    call='physicsobject::flagNumObject({df}, {output}, {input}, {nBoostedTau_min}, "<")',
    input=[q.nBoostTaus],
    output=[],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)
FilterNBoostTaus_veto = Filter(
    name="FilterNBoostTaus_veto",
    call='basefunctions::FilterFlagsAny({df}, "Number of BoostTaus < 2", {input})',
    input=[],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
    subproducers=[NBoostTauFlag_veto]
)

LVBoostedTau0 = Producer(
    name="LVBoostedTau0",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.base_BoostedTau_collection,
        nanoAOD.boostedTau_pt,
        nanoAOD.boostedTau_eta,
        nanoAOD.boostedTau_phi,
        nanoAOD.boostedTau_mass,
    ],
    output=[q.BoostedTau0_p4_0],
    scopes=["boostedbb_boostedtt", "resbb_boostedtt"],
)

LVBoostedTau1 = Producer(
    name="LVBoostedTau1",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.base_BoostedTau_collection,
        nanoAOD.boostedTau_pt,
        nanoAOD.boostedTau_eta,
        nanoAOD.boostedTau_phi,
        nanoAOD.boostedTau_mass,
    ],
    output=[q.BoostedTau0_p4_1],
    scopes=["boostedbb_boostedtt", "resbb_boostedtt"],
)

SFMass0 = Producer(
    name="SFMass0",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 0, {output})",
    input=[
        q.base_BoostedTau_collection,
        nanoAOD.boostedTau_mass,
    ],
    output=[q.BoostedTau0_SFMass_0],
    scopes=["boostedbb_boostedtt", "resbb_boostedtt"]
)

SFMass1 = Producer(
    name="SFMass1",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 1, {output})",
    input=[
        q.base_BoostedTau_collection,
        nanoAOD.boostedTau_mass,
    ],
    output=[q.BoostedTau0_SFMass_1],
    scopes=["boostedbb_boostedtt", "resbb_boostedtt"]
)

Nu_tau_x12 = Producer(
    name="Nu_tau_x12",
    call="quantities::boostedbbtt::Mass_CA({df}, {input}, {output})",
    input=[
        q.BoostedTau0_p4_0,
        q.BoostedTau0_p4_1,
        nanoAOD.PFMET_pt,
        nanoAOD.PFMET_phi,
    ],
    output=[q.x0x1],
    scopes=["boostedbb_boostedtt", "resbb_boostedtt"],
)