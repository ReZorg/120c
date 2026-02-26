"""
120-Cell Egregore State Space Models

This package contains the core implementations for modeling self-organizing
movement ecosystems using the 120-cell polytope as a geometric substrate.
"""

from .hopf_decomposition import (
    HopfDecomposition,
    TwinPair,
    Ring,
    DodecahedralCell,
    PHI,
    compute_golden_ratio_properties,
    compute_factorial_structure,
)

from .twin_pair_lifecycle import (
    TwinPairLifecycle,
    LifecyclePhase,
    PhaseCell,
    VortexState,
    PentagonalInterface,
    CliffordTorusStructure,
)

__version__ = "0.1.0"

__all__ = [
    # Hopf decomposition
    "HopfDecomposition",
    "TwinPair",
    "Ring",
    "DodecahedralCell",
    "PHI",
    "compute_golden_ratio_properties",
    "compute_factorial_structure",
    # Twin pair lifecycle
    "TwinPairLifecycle",
    "LifecyclePhase",
    "PhaseCell",
    "VortexState",
    "PentagonalInterface",
    "CliffordTorusStructure",
]
