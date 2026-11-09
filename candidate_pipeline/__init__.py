"""
Candidate Pipeline: Computational materials candidate generation and verification.
Bridges Layer 2 discovery gaps into physically plausible, synthesized candidate materials
with stoichiometry balancing, crystal lattice assignment, and experimental synthesis protocols.
"""

from candidate_pipeline.generator import CandidateGenerator, MaterialCandidate
from candidate_pipeline.verifier import CandidateVerifier
from candidate_pipeline.protocol_designer import ProtocolDesigner

__all__ = [
    "CandidateGenerator",
    "MaterialCandidate",
    "CandidateVerifier",
    "ProtocolDesigner",
]
