from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup, Filter

####################
# Set of producers used for loosest selection of electrons
####################

##need to add call
SubJetFatJetdR = Producer(
    name="SubJetFatJetdR",
    call="quantities::boostedbbtt::dR_tau_fatjet0({df}, {output}, {input})",
    input=[
        q.fatjet_p4_0, 
        nanoAOD.SubJet_pt,
        nanoAOD.SubJet_eta, 
        nanoAOD.SubJet_phi,
        nanoAOD.SubJet_mass,
        ],
    output=[q.dR_SubJet_Fatjet],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)

SubJetFatJetdRCut = Producer(
    name="SubJetFatJetdRCut",
    call="physicsobject::CutVarMax({df}, {input}, {output}, {min_fatjet_dR})",
    input=[q.dR_SubJet_Fatjet],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)

BaseSubJets = ProducerGroup(
    name="BaseSubJets",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.base_SubJet_mask],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
    subproducers=[
        SubJetFatJetdRCut,
    ],
)

SubJetCollection = Producer(
    name="SubJetCollection",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[
        nanoAOD.SubJet_pt, 
        q.base_SubJet_mask,
        ],
    output=[q.base_SubJet_collection],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)

NumberOfSubJets = Producer(
    name="NumberOfSubJets",
    call="quantities::NumberOfGoodObjects({df}, {output}, {input})",
    input=[q.base_SubJet_mask],
    output=[q.nSubJets],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
NSubJetFlag = Producer(
    name="NSubJetFlag",
    call='physicsobject::flagNumObject({df}, {output}, {input}, {nSubJet_min}, ">=")',
    input=[q.nSubJets],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
# call='basefunctions::FilterThreshold({df}, {input}, {FullyBoosted_good_nfatjets}, ">=", "Number of fatjets >= 1")',
FilterNSubJets = Filter(
    name="FilterNSubJets",
    call='basefunctions::FilterFlagsAny({df}, "Number of SubJets >= 2", {input})',
    input=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
    subproducers=[NSubJetFlag]
)

NSubJetFlag_veto = Producer(
    name="NSubJetFlag_veto",
    call='physicsobject::flagNumObject({df}, {output}, {input}, {nSubJet_min}, "<")',
    input=[q.nSubJets],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)
# call='basefunctions::FilterThreshold({df}, {input}, {FullyBoosted_good_nfatjets}, ">=", "Number of fatjets >= 1")',
FilterNSubJets_veto = Filter(
    name="FilterNSubJets_veto",
    call='basefunctions::FilterFlagsAny({df}, "Number of SubJets < 2", {input})',
    input=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
    subproducers=[NSubJetFlag_veto]
)

LVSubJet0 = Producer(
    name="LVSubJet0",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.base_SubJet_collection,
        nanoAOD.SubJet_pt,
        nanoAOD.SubJet_eta,
        nanoAOD.SubJet_phi,
        nanoAOD.SubJet_mass,
    ],
    output=[q.BoostedTau0_p4_0],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet"],
)

LVSubJet1 = Producer(
    name="LVSubJet1",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.base_SubJet_collection,
        nanoAOD.SubJet_pt,
        nanoAOD.SubJet_eta,
        nanoAOD.SubJet_phi,
        nanoAOD.SubJet_mass,
    ],
    output=[q.BoostedTau0_p4_1],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet"],
)

SFMass0 = Producer(
    name="SFMass0",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 0, {output})",
    input=[
        q.base_SubJet_collection,
        nanoAOD.SubJet_mass,
    ],
    output=[q.BoostedTau0_SFMass_0],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"]
)

SFMass1 = Producer(
    name="SFMass1",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 1, {output})",
    input=[
        q.base_SubJet_collection,
        nanoAOD.SubJet_mass,
    ],
    output=[q.BoostedTau0_SFMass_1],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"]
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
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)



SubJet0_ifcannotfoundbydR = Producer(
    name="SubJet0_ifcannotfoundbydR",
    call="lorentzvectors::build_subjet_postion({df}, {input_vec}, 0, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_subJetIdx1, 
        ],
    output=[q.SubJet0_ifcannotfoundbydR],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)

SubJet1_ifcannotfoundbydR = Producer(
    name="SubJet1_ifcannotfoundbydR",
    call="lorentzvectors::build_subjet_postion({df}, {input_vec}, 0, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_subJetIdx2, 
        ],
    output=[q.SubJet1_ifcannotfoundbydR],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
)

LVSubJet0_ifcannotfoundbydR = Producer(
    name="LVSubJet0_ifcannotfoundbydR",
    call="lorentzvectors::build_input_index({df}, {input}, {output})",
    input=[
        q.SubJet0_ifcannotfoundbydR,
        nanoAOD.SubJet_pt,
        nanoAOD.SubJet_eta,
        nanoAOD.SubJet_phi,
        nanoAOD.SubJet_mass,
    ],
    output=[q.BoostedTau0_p4_0],
    scopes=["boostedbb_boostedtt_fatjet"],
)

LVSubJet1_ifcannotfoundbydR = Producer(
    name="LVSubJet1_ifcannotfoundbydR",
    call="lorentzvectors::build_input_index({df}, {input}, {output})",
    input=[
        q.SubJet1_ifcannotfoundbydR,
        nanoAOD.SubJet_pt,
        nanoAOD.SubJet_eta,
        nanoAOD.SubJet_phi,
        nanoAOD.SubJet_mass,
    ],
    output=[q.BoostedTau0_p4_1],
    scopes=["boostedbb_boostedtt_fatjet"],
)


MatchSubJet = Producer(
    name="MatchSubJet",
    call="lorentzvectors::matchSubJet({df}, {input_vec}, 0, 1, {output})",
    input=[
        q.base_SubJet_collection,
        q.SubJet0_ifcannotfoundbydR,
        q.SubJet1_ifcannotfoundbydR,
    ],
    output=[q.MatchedSubinfo],
    scopes=["boostedbb_boostedtt_subjet"],
)

MatchSubJet_fake = Producer(
    name="MatchSubJet_fake",
    call="lorentzvectors::buildSafem1({df}, {output})",
    input=[],
    output=[q.MatchedSubinfo],
    scopes=["boostedbb_boostedtt", "boostedbb_boostedtt_fatjet"],
)