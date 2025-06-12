from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List

from .producers import event as event
from .producers import genparticles as genparticles
from .producers import muons as muons

#for fullyboosted
from .producers import jets as jets
from .producers import FatJets as FatJets
from .producers import electrons_boostedbbtt as electrons_boostedbbtt
from .producers import muons_boostedbbtt as muons_boostedbbtt
from .producers import boostedtau_boostedbbtt as boostedtau_boostedbbtt
from .producers import subjet_boostedbbtt as subjet_boostedbbtt

from .producers import pairquantities as pairquantities
from .producers import pairselection as pairselection
from .producers import scalefactors as scalefactors
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q
from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier
from code_generation.rules import RemoveProducer
from code_generation.systematics import SystematicShift


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
):
    configuration = Configuration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
    )

    # first add default parameters necessary for all scopes
    configuration.add_config_parameters(
        "global",
        {
            # for LHE weights
            "muR": 1.0,
            "muF": 1.0,
            "PU_reweighting_file": EraModifier(
                {
                    "2022EE": "data/jsonpog-integration/POG/LUM/2022_Summer22/puWeights.json.gz", 
                }
            ),
            "PU_reweighting_era": EraModifier(
                {
                    "2022EE": "Collisions2022_355100_357900_eraBCD_GoldenJson",  
                }
            ),
            "PU_reweighting_variation": "nominal",
            "PU_reweighting_hist": "pileup",
            "golden_json_file": EraModifier(
                {
                    "2022EE": "data/golden_json/Cert_Collisions2022_355100_362760_Golden.json.txt",
                }
            ),
            "met_filters": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        #"Flag_BadPFMuonDzFilter",  # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        ## new filters for 2022/23
                        "Flag_BadPFMuonDzFilter",
                        "Flag_hfNoisyHitsFilter",
                        "Flag_ecalBadCalibFilter",

                    ], 
        },
    )
    # FatJet base selection:
    configuration.add_config_parameters(
        ["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
        {
            
            "FatJet_id": EraModifier(
                {
                    # Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto
                    "2016preVFP": 1,  # 1==pass(loose)
                    "2016postVFP": 1,  # 1==pass(loose)
                    "2017": 2,  # 2==pass(tight)
                    "2018": 2,  # 2==pass(tight)
                    "2022EE": 2,  # 2==pass(tight)
                    "2022postEE": 2,  # 2==pass(tight)
                    "2023preBPix": 2,  # 2==pass(tight)
                    "2023postBPix": 2,  # 2==pass(tight)
                }
            )
        },
    )


    # FatJet base selection for boostedbb:
    configuration.add_config_parameters(
        ["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet"],
        {
            "min_FatJet_pt": 200,
            "max_FatJet_eta": 2.4,
            "FullyBoosted_good_nfatjets" : 2,
        },
    )

    # AK4Jet base selection for resbb:
    configuration.add_config_parameters(
        ["resbb_boostedtt"],
        {
            "min_FatJet_pt": 200,
            "max_FatJet_eta": 2.4,
            "FullyBoosted_good_nfatjets" : 1,
            "min_jet_pt": 20,
            "max_jet_eta": 2.5,
            "jet_puid_max_pt": 50,  # recommended to apply puID only for jets below 50 GeV
            "jet_reapplyJES": False,
            "jet_jes_sources": '{""}',
            "jet_jes_shift": 0,
            "jet_jer_shift": '"nom"',  # or '"up"', '"down"'
            "jet_jec_file": EraModifier(
                {
                    "2016preVFP": '"data/jsonpog-integration/POG/JME/2016preVFP_UL/jet_jerc.json.gz"',
                    "2016postVFP": '"data/jsonpog-integration/POG/JME/2016postVFP_UL/jet_jerc.json.gz"',
                    "2017": '"data/jsonpog-integration/POG/JME/2017_UL/jet_jerc.json.gz"',
                    "2018": '"data/jsonpog-integration/POG/JME/2018_UL/jet_jerc.json.gz"',
                    "2022EE": '"data/jsonpog-integration/POG/JME/2022_Summer22EE/jet_jerc.json.gz"',
                }
            ),
            "jet_jer_tag": EraModifier(
                {
                    "2016preVFP": '"Summer20UL16APV_JRV3_MC"',
                    "2016postVFP": '"Summer20UL16_JRV3_MC"',
                    "2017": '"Summer19UL17_JRV2_MC"',
                    "2018": '"Summer19UL18_JRV2_MC"',
                    "2022EE": '"Summer22EE_22Sep2023_JR"',
                }
            ),
            "jet_jes_tag": EraModifier(
                {
                    "2016preVFP": '"Summer19UL16APV_V7_MC"',
                    "2016postVFP": '"Summer19UL16_V7_MC"',
                    "2017": '"Summer19UL17_V5_MC"',
                    "2018": '"Summer19UL18_V5_MC"',
                    "2022EE": '"Summer22EE_22Sep2023"',
                }
            ),
            "jet_jec_algo": '"AK4PFchs"',
            "jet_veto_map": EraModifier(
                {
                    "2022EE": '"data/jsonpog-integration/POG/JME/2022_Summer22EE/jetvetomaps.json.gz"',
                }
            ),
            "jet_veto_tag": EraModifier(
                {
                    "2022EE": '"Summer22EE_23Sep2023"',
                }
            ),
            "jet_id": 2,  # or "JET_tightId"
            "deltaR_jet_veto": 0.4,  # deltaR between the jet and the vetoed objects
        },
    )

    # Muon base selection parameters:
    configuration.add_config_parameters(
        ["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
        {
            "LooseMuon_eta": 2.4,
            "LooseMuon_dxy": 0.05,
            "LooseMuon_dz": 0.2,
            "LooseMuon_pt": 10,
            "LooseMuon_miniPFRelIso_all": 0.2,
            "muon_id": EraModifier(
                { 
                    "2022EE": "Muon_looseId", 
                },
            )
        }
    )

    # Electron base selection parameters:
    configuration.add_config_parameters(
        ["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
        {
            "LooseEle_eta": 2.5,
            "LooseEle_dxy": 0.05,
            "LooseEle_dz": 0.2,
            "LooseEle_pt": 20,
            "LooseEle_miniPFRelIso_all": 0.2,
            "ele_id": EraModifier(
                { 
                    "2022EE": "Electron_mvaNoIso_WP90", 
                },
            )
        }
    )

    configuration.add_config_parameters(
        ["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
        {
            "PNet_xbb":0.7,
            "PNet_xtt":0.7,
            "min_fatjet_dR":0.8,
            "nBoostedTau_min":2,
            "nSubJet_min":2,
        }
    )

    ##### Add producers #####

    configuration.add_producers(
        "global",
        [
            event.SampleFlags,
            event.PUweights,
            event.Lumi,
            event.MetFilter,
        ],
    )

    configuration.add_producers(
        ["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
        [

            FatJets.GoodFatJets,
            FatJets.NumberOfGoodFatJets,   

            electrons_boostedbbtt.BaseElectrons,
            muons_boostedbbtt.BaseMuons,

            electrons_boostedbbtt.NumberOfLooseElectrons,
            electrons_boostedbbtt.LooseElectronsVeto,
            
            muons_boostedbbtt.NumberOfLooseMuons,
            muons_boostedbbtt.LooseMuonsVeto,   
        ]
    )

    configuration.add_producers(
        ["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
        [
            FatJets.FatJetCollection_Xtt,
            FatJets.FilterNFatJets,

            FatJets.LVFatJet0,
            FatJets.LVFatJet1,
            FatJets.FatJetSFMass0,
            FatJets.FatJetSFMass1,
            FatJets.FatJetMass0,
            FatJets.FatJetMass1,
            FatJets.FatJet0_PNet_QCD,
            FatJets.FatJet1_PNet_QCD,
            FatJets.FatJet0_PNet_xbb_vs_QCD,
            FatJets.FatJet1_PNet_xbb_vs_QCD,
            FatJets.FatJet0_PNet_xtt_vs_QCD,
            FatJets.FatJet1_PNet_xtt_vs_QCD,

            FatJets.FatJet0_9X_ttvsqcd,
            FatJets.FatJet1_9X_bbvsqcd,

            FatJets.FatJet0_PNet_xtt,
            FatJets.FatJet1_PNet_xbb,
            FatJets.FatJet0_9X_tt,
            FatJets.FatJet1_9X_bb,

            FatJets.FatJetdR,
            FatJets.FatJetdphi,


            boostedtau_boostedbbtt.TauFatJetdR,
            boostedtau_boostedbbtt.BaseBoostedTaus,
            boostedtau_boostedbbtt.NumberOfBoostTaus,
            boostedtau_boostedbbtt.BoosetedTauCollection,

            subjet_boostedbbtt.SubJetFatJetdR,
            subjet_boostedbbtt.BaseSubJets,
            subjet_boostedbbtt.NumberOfSubJets,
            subjet_boostedbbtt.SubJetCollection,

            subjet_boostedbbtt.SubJet0_ifcannotfoundbydR,
            subjet_boostedbbtt.SubJet1_ifcannotfoundbydR,
            
        ]
        

    )


    configuration.add_producers(
        ["boostedbb_boostedtt"],
        [
            boostedtau_boostedbbtt.FilterNBoostTaus,

            subjet_boostedbbtt.MatchSubJet_fake,
            
            boostedtau_boostedbbtt.LVBoostedTau0,
            boostedtau_boostedbbtt.LVBoostedTau1,

            boostedtau_boostedbbtt.SFMass0,
            boostedtau_boostedbbtt.SFMass1,

            boostedtau_boostedbbtt.Nu_tau_x12,

            FatJets.Mass_CA,
            FatJets.Mass_CA_SF,
        ]
        
    )

    configuration.add_producers(
        ["boostedbb_boostedtt_subjet"],
        [
            boostedtau_boostedbbtt.FilterNBoostTaus_veto,
            subjet_boostedbbtt.FilterNSubJets,

            subjet_boostedbbtt.MatchSubJet,

            subjet_boostedbbtt.LVSubJet0,
            subjet_boostedbbtt.LVSubJet1,

            subjet_boostedbbtt.SFMass0,
            subjet_boostedbbtt.SFMass1,

            subjet_boostedbbtt.Nu_tau_x12,
            FatJets.Mass_CA,
            FatJets.Mass_CA_SF,
        ]
        
    )

    configuration.add_producers(
        ["boostedbb_boostedtt_fatjet"],
        [
            boostedtau_boostedbbtt.FilterNBoostTaus_veto,
            subjet_boostedbbtt.FilterNSubJets_veto,

            subjet_boostedbbtt.MatchSubJet_fake,

            FatJets.LV0,
            FatJets.LV1,

            # subjet_boostedbbtt.LVSubJet0_ifcannotfoundbydR,
            # subjet_boostedbbtt.LVSubJet1_ifcannotfoundbydR,

            FatJets.Mass999_0,
            FatJets.Mass999_1,

            FatJets.Fake_x12,
            FatJets.Mass_CA_FatJet,#需要改写
            FatJets.Mass_CA_FatJet_SF,
            # subjet_boostedbbtt.Nu_tau_x12,
            # FatJets.Mass_CA,
            # FatJets.Mass_CA_SF,
        ]
        
    )

    # Add resbb producers
    configuration.add_producers(
        ["resbb_boostedtt"],
        [
            #Copied from boostedbb_boostedtt
            boostedtau_boostedbbtt.FilterNBoostTaus,

            subjet_boostedbbtt.MatchSubJet_fake,
            
            boostedtau_boostedbbtt.LVBoostedTau0,
            boostedtau_boostedbbtt.LVBoostedTau1,

            boostedtau_boostedbbtt.SFMass0,
            boostedtau_boostedbbtt.SFMass1,

            boostedtau_boostedbbtt.Nu_tau_x12,

            FatJets.Mass_CA,
            FatJets.Mass_CA_SF,
            
            #AK4 jet for resolved bb part starts here
            jets.JetPtCorrection,
            # jets.JetMassCorrection,
            
            # jets.LVJet1,
            # jets.LVJet2,

            # jets.GoodJets_2022,
            # jets.JetCollection,
        ]
    )

    configuration.add_outputs(
        "global",
        [
            q.is_data,
            q.is_embedding,
            q.is_ttbar,
            q.is_dyjets,
            q.is_wjets,
            q.is_diboson,
            nanoAOD.run,
            q.lumi,
            nanoAOD.genWeight,
            nanoAOD.event,
            q.puweight,
            nanoAOD.Jet_pt,
            nanoAOD.Jet_eta,
            nanoAOD.FatJet_pt,
            nanoAOD.FatJet_eta,
            nanoAOD.HLT_AK8PFHT800_TrimMass50,
            nanoAOD.HLT_AK8PFJet400_TrimMass30,
            nanoAOD.HLT_AK8PFJet500,
            nanoAOD.HLT_PFJet500,
            nanoAOD.HLT_PFHT1050,
            nanoAOD.HLT_PFHT500_PFMET100_PFMHT100_IDTight,
            nanoAOD.HLT_PFHT700_PFMET85_PFMHT85_IDTight,
            nanoAOD.HLT_PFHT800_PFMET75_PFMHT75_IDTight,

        ],
    )

    # configuration.add_outputs(
    #     ["notwofatjet"],
    #     [
    #         q.base_electrons_mask,
    #         q.base_muons_mask,
    #         q.Loose_muon_veto_flag,
    #         q.Loose_electron_veto_flag,
    #         q.n_Loose_muons,
    #         q.n_Loose_electrons,
    #         q.FatJet_id_mask,
    #         q.good_FatJets_mask,
    #         q.nfatjets,
    #     ],
    # )

    configuration.add_outputs(
        ["boostedbb_boostedtt",  "boostedbb_boostedtt_subjet", "boostedbb_boostedtt_fatjet", "resbb_boostedtt"],
        [
            q.base_electrons_mask,
            q.base_muons_mask,

            q.FatJet_id_mask,
            q.good_FatJets_mask,
            q.nfatjets,
            q.good_Xbbtt_fatjet_collection,
            q.fatjet_p4_0,
            q.fatjet_p4_1,
            q.FatJet_bb_SFMass_1,
            q.FatJet_tt_SFMass_0,
            q.FatJet_tt_Mass_0,
            q.FatJet_bb_Mass_1,
            q.FatJet0_PNet_xttvsQCD,
            q.FatJet1_PNet_xttvsQCD,
            q.FatJet0_PNet_xbbvsQCD,
            q.FatJet1_PNet_xbbvsQCD,
            q.FatJet0_PNetQCD,
            q.FatJet1_PNetQCD,

            q.FatJet0_9X_xttvsQCD,
            q.FatJet1_9X_xbbvsQCD,

            q.FatJet0_PNet_xtt,
            q.FatJet1_PNet_xbb,
            q.FatJet0_9X_xtt,
            q.FatJet1_9X_xbb,

            q.dR_Fatjet,
            q.dphi_Fatjet,

            q.Loose_muon_veto_flag,
            q.Loose_electron_veto_flag,
            q.n_Loose_muons,
            q.n_Loose_electrons,
            
            q.dR_tau_Fatjet,
            q.base_BoostedTau_mask,
            q.nBoostTaus,
            q.base_BoostedTau_collection,

            q.dR_SubJet_Fatjet,
            q.base_SubJet_mask,
            q.nSubJets,
            q.base_SubJet_collection,

            q.SubJet1_ifcannotfoundbydR,
            q.SubJet0_ifcannotfoundbydR,

            q.BoostedTau0_p4_0,
            q.BoostedTau0_p4_1,
            q.BoostedTau0_SFMass_0,
            q.BoostedTau0_SFMass_1,

            q.x0x1,
            q.tautau_SFMAss_CA,
            q.tautau_MAss_CA,

            q.MatchedSubinfo,
        ],
    )

    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[event.PUweights],
            samples=["data"],
        ),
    )


    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
