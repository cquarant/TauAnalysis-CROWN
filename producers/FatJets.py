from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup, Filter

####################
# Set of producers used for loosest selection of FatJets
####################

FatJetPtCut = Producer(
    name="FatJetPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_FatJet_pt})",
    input=[nanoAOD.FatJet_pt],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)
FatJetEtaCut = Producer(
    name="FatJetEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_FatJet_eta})",
    input=[nanoAOD.FatJet_eta],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)
FatJetIDCut = Producer(
    name="FatJetIDCut",
    call='physicsobject::jet::CutID({df}, {output}, "{FatJet_id}")',
    input=[nanoAOD.FatJet_jetId],
    output=[q.FatJet_id_mask],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)
## 2022preEE fatjet id UChar_t 
FatJetIDCut_UChar = Producer(
    name="FatJetIDCut_UChar",
    call="physicsobject::jet::CutUCharID({df}, {output}, {input}, {FatJet_id})",
    input=[nanoAOD.FatJet_jetId],
    output=[q.FatJet_id_mask],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

GoodFatJets = ProducerGroup(
    name="GoodFatJets",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.good_FatJets_mask],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
    subproducers=[
        FatJetPtCut, 
        FatJetEtaCut,
        FatJetIDCut_UChar,
    ],
)
NumberOfGoodFatJets = Producer(
    name="NumberOfGoodFatJets",
    call="quantities::NumberOfGoodObjects({df}, {output}, {input})",
    input=[q.good_FatJets_mask],
    output=[q.nfatjets],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)
NFatjetFlag = Producer(
    name="NFatjetFlag",
    call='physicsobject::flagNumObject({df}, {output}, {input}, {FullyBoosted_good_nfatjets}, ">=")',
    input=[q.nfatjets],
    output=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)
# call='basefunctions::FilterThreshold({df}, {input}, {FullyBoosted_good_nfatjets}, ">=", "Number of fatjets >= 1")',
FilterNFatJets = Filter(
    name="FilterNFatJets",
    call='basefunctions::FilterFlagsAny({df}, "Number of fatjets >= 1", {input})',
    input=[],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
    subproducers=[NFatjetFlag]
)
# fatjet collection with pt
FatJetCollection = Producer(
    name="FatJetCollection",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[nanoAOD.FatJet_pt, q.good_FatJets_mask],
    output=[q.good_fatjet_collection],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)


FatJetCollection_Xtt = Producer(
    name="FatJetCollection_Xtt",
    call="jet::OrderJetsByCustomCriteria({df}, {output}, {input})",
    input=[
        nanoAOD.FatJet_particleNet_XttVsQCD,
        nanoAOD.FatJet_particleNet_XbbVsQCD, 
        q.good_FatJets_mask],
    output=[q.good_Xbbtt_fatjet_collection],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

#ttFatjet 
LVFatJet0 = Producer(
    name="LVFatJet0",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_pt,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        nanoAOD.FatJet_mass,
    ],
    output=[q.fatjet_p4_0],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

LVFatJet1 = Producer(
    name="LVFatJet1",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_pt,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        nanoAOD.FatJet_mass,
    ],
    output=[q.fatjet_p4_1],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJetdR = Producer(
    name="FatJetdR",
    call="quantities::boostedbbtt::dR_fatjet({df}, {output}, {input})",
    input=[
        q.fatjet_p4_0, 
        q.fatjet_p4_1,
        ],
    output=[q.dR_Fatjet],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJetdphi = Producer(
    name="FatJetdphi",
    call="quantities::boostedbbtt::dphi_fatjet({df}, {output}, {input})",
    input=[
        q.fatjet_p4_0, 
        q.fatjet_p4_1,
        ],
    output=[q.dphi_Fatjet],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJetSFMass0 = Producer(
    name="FatJetSFMass0",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 0, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_msoftdrop,
    ],
    output=[q.FatJet_tt_SFMass_0],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJetSFMass1 = Producer(
    name="FatJetSFMass1",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 1, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_msoftdrop,
    ],
    output=[q.FatJet_bb_SFMass_1],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJetMass0 = Producer(
    name="FatJetMass0",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 0, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_mass,
    ],
    output=[q.FatJet_tt_Mass_0],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJetMass1 = Producer(
    name="FatJetMass1",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 1, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_mass,
    ],
    output=[q.FatJet_bb_Mass_1],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet0_PNet_xtt_vs_QCD = Producer(
    name="FatJet0_PNet_xtt_vs_QCD",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 0, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_particleNet_XttVsQCD,
    ],
    output=[q.FatJet0_PNet_xttvsQCD],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet1_PNet_xtt_vs_QCD = Producer(
    name="FatJet0_PNet_xtt_vs_QCD",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 1, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_particleNet_XttVsQCD,
    ],
    output=[q.FatJet1_PNet_xttvsQCD],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet0_PNet_xbb_vs_QCD = Producer(
    name="FatJet0_PNet_xbb_vs_QCD",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 0, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_particleNet_XbbVsQCD,
    ],
    output=[q.FatJet0_PNet_xbbvsQCD],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet1_PNet_xbb_vs_QCD = Producer(
    name="FatJet0_PNet_xbb_vs_QCD",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 1, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_particleNet_XbbVsQCD,
    ],
    output=[q.FatJet1_PNet_xbbvsQCD],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet0_PNet_QCD = Producer(
    name="FatJet0_PNet_QCD",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 0, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_particleNet_QCD,
    ],
    output=[q.FatJet0_PNetQCD],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet1_PNet_QCD = Producer(
    name="FatJet0_PNet_QCD",
    call="lorentzvectors::buildSFMass({df}, {input_vec}, 1, {output})",
    input=[
        q.good_Xbbtt_fatjet_collection,
        nanoAOD.FatJet_particleNet_QCD,
    ],
    output=[q.FatJet1_PNetQCD],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet0_9X_ttvsqcd = Producer(
    name="FatJet0_9X_ttvsqcd",
    call="quantities::boostedbbtt::Score_9X({df}, {input}, {output})",
    input=[
        q.FatJet0_PNet_xttvsQCD,
    ],
    output=[q.FatJet0_9X_xttvsQCD],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet1_9X_bbvsqcd = Producer(
    name="FatJet1_9X_bbvsqcd",
    call="quantities::boostedbbtt::Score_9X({df}, {input}, {output})",
    input=[
        q.FatJet1_PNet_xbbvsQCD,
    ],
    output=[q.FatJet1_9X_xbbvsQCD],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet0_PNet_xtt = Producer(
    name="FatJet0_PNet_xtt",
    call="quantities::boostedbbtt::Score_original({df}, {input}, {output})",
    input=[
        q.FatJet0_PNet_xttvsQCD,
        q.FatJet0_PNetQCD,
    ],
    output=[q.FatJet0_PNet_xtt],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet1_PNet_xbb = Producer(
    name="FatJet1_PNet_xbb",
    call="quantities::boostedbbtt::Score_original({df}, {input}, {output})",
    input=[
        q.FatJet1_PNet_xbbvsQCD,
        q.FatJet1_PNetQCD,
    ],
    output=[q.FatJet1_PNet_xbb],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet0_9X_tt = Producer(
    name="FatJet0_9X_tt",
    call="quantities::boostedbbtt::Score_9X({df}, {input}, {output})",
    input=[
        q.FatJet0_PNet_xtt,
    ],
    output=[q.FatJet0_9X_xtt],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

FatJet1_9X_bb = Producer(
    name="FatJet1_9X_bb",
    call="quantities::boostedbbtt::Score_9X({df}, {input}, {output})",
    input=[
        q.FatJet1_PNet_xbb,
    ],
    output=[q.FatJet1_9X_xbb],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

LV0 = Producer(
    name="LV0",
    call="lorentzvectors::buildSafeP4({df},{output})",
    input=[],
    output=[q.BoostedTau0_p4_0],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

LV1 = Producer(
    name="LV1",
    call="lorentzvectors::buildSafeP4({df},{output})",
    input=[],
    output=[q.BoostedTau0_p4_1],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

Mass999_0 = Producer(
    name="Mass999_0",
    call="lorentzvectors::buildSafe999({df}, {output})",
    input=[],
    output=[q.BoostedTau0_SFMass_0],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

Mass999_1 = Producer(
    name="Mass999_1",
    call="lorentzvectors::buildSafe999({df}, {output})",
    input=[],
    output=[q.BoostedTau0_SFMass_1],
        scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

Fake_x12 = Producer(
    name="Fake_x12",
    call="lorentzvectors::buildSafe999({df}, {output})",
    input=[],
    output=[q.x0x1],
    scopes=["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

Mass_CA = Producer(
    name="Mass_CA",
    call="quantities::boostedbbtt::CA_ttMAss({df}, {input}, {output})",
    input=[
        q.x0x1,
        q.FatJet_tt_Mass_0,
    ],
    output=[q.tautau_MAss_CA],
    scopes=["boostedbb_boostedtt", "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

Mass_CA_SF = Producer(
    name="Mass_CA_SF",
    call="quantities::boostedbbtt::CA_ttMAss({df}, {input}, {output})",
    input=[
        q.x0x1,
        q.FatJet_tt_SFMass_0,
    ],
    output=[q.tautau_SFMAss_CA],
    scopes=["boostedbb_boostedtt", "boostedbb_boostedtt_subjet" , "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

Mass_CA_FatJet = Producer(
    name="Mass_CA_FatJet",
    call="quantities::boostedbbtt::CA_ttMAss_fatjet({df}, {input}, {output})",
    input=[
        q.fatjet_p4_0,
        nanoAOD.PFMET_pt,
        nanoAOD.PFMET_phi,
    ],
    output=[q.tautau_MAss_CA],
    scopes=["boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)

Mass_CA_FatJet_SF = Producer(
    name="Mass_CA_FatJet_SF",
    call="quantities::boostedbbtt::CA_ttMAss_fatjet({df}, {input}, {output})",
    input=[
        q.fatjet_p4_0,
        nanoAOD.PFMET_pt,
        nanoAOD.PFMET_phi,
    ],
    output=[q.tautau_SFMAss_CA],
    scopes=["boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
)