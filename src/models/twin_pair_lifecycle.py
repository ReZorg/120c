"""
Twin Pair Lifecycle Model

This module implements the DNA-like double helix structure of a twin pair,
where two rings run counter-rotating phases with phase-locked base pairing.

The twin pair is the fundamental lifecycle unit, with:
- 10 macro-phases per strand (developmental stages)
- 100 vortex-states total (vertices)
- 100 inter-strand rungs (shared pentagonal faces)
- 200 transition pathways (edges)
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


class LifecyclePhase(Enum):
    """
    The 10 macro-phases of the lifecycle.
    
    These map to developmental stages in a decagonal cycle,
    with phases 1-5 representing the ascending arc (increasing curvature)
    and phases 6-10 representing the descending arc (decreasing curvature).
    """
    INCEPTION = 1      # Inception - seed state
    FORMATION = 2      # Formation - initial structure
    STRUCTURING = 3    # Structuring - pattern emergence
    INTEGRATION = 4    # Integration - coherence building
    CULMINATION = 5    # Culmination - apex, maximum curvature
    DISTRIBUTION = 6   # Distribution - energy dispersal
    REFINEMENT = 7     # Refinement - optimization
    CONSOLIDATION = 8  # Consolidation - stabilization
    DISSOLUTION = 9    # Dissolution - release
    SEED_REBIRTH = 10  # Seed/Rebirth - feeds Phase 1 (closed loop)


@dataclass
class VortexState:
    """
    A vortex-state at a vertex carrying a local (COM, ORG, ENT) frame.
    
    Each vertex in the twin pair represents a distinct vortex-state
    with 3 coordinates: COM (complexity), ORG (organization), ENT (entropy).
    """
    vertex_id: int
    phase: LifecyclePhase
    strand: str  # "A" or "B"
    com: float = 0.0  # Complexity coordinate
    org: float = 0.0  # Organization coordinate
    ent: float = 0.0  # Entropy coordinate
    
    def __post_init__(self):
        """Validate vortex state."""
        assert self.strand in ["A", "B"]


@dataclass
class PentagonalInterface:
    """
    A pentagonal face interface between phases.
    
    Every interface is a pentagon with:
    - 5 vertices
    - 5 edges
    - Golden ratio φ in its geometry
    
    Each dodecahedral cell has 12 pentagonal faces:
    - 2 backbone faces (intra-ring: sequential phase transitions)
    - 10 cross-strand faces (inter-ring: base pairing with twin)
    """
    face_id: int
    vertices: List[int]  # 5 vertices
    edges: List[Tuple[int, int]]  # 5 edges
    interface_type: str  # "backbone" or "rung"
    phase_a: Optional[LifecyclePhase] = None
    phase_b: Optional[LifecyclePhase] = None
    
    def __post_init__(self):
        """Validate pentagonal structure."""
        assert len(self.vertices) == 5, "Pentagon must have 5 vertices"
        assert len(self.edges) == 5, "Pentagon must have 5 edges"
        assert self.interface_type in ["backbone", "rung"]
    
    @property
    def is_backbone(self) -> bool:
        """True if this is an intra-ring backbone interface."""
        return self.interface_type == "backbone"
    
    @property
    def is_rung(self) -> bool:
        """True if this is an inter-ring rung interface (base pair)."""
        return self.interface_type == "rung"


@dataclass
class PhaseCell:
    """
    A macro-phase cell representing one of the 10 developmental stages.
    
    Each phase contains:
    - 1 dodecahedral cell
    - ~10 vortex-states (vertices)
    - 12 pentagonal interfaces (2 backbone + 10 cross-strand)
    - 30 transition pathways (edges)
    """
    phase: LifecyclePhase
    strand: str  # "A" or "B"
    dodecahedron_id: int
    vortex_states: List[VortexState] = field(default_factory=list)
    interfaces: List[PentagonalInterface] = field(default_factory=list)
    
    @property
    def num_vortex_states(self) -> int:
        """Number of vortex-states in this phase."""
        return len(self.vortex_states)
    
    @property
    def num_interfaces(self) -> int:
        """Number of pentagonal interfaces (should be ~12)."""
        return len(self.interfaces)
    
    @property
    def backbone_interfaces(self) -> List[PentagonalInterface]:
        """The 2 backbone interfaces to sequential phases."""
        return [i for i in self.interfaces if i.is_backbone]
    
    @property
    def cross_strand_interfaces(self) -> List[PentagonalInterface]:
        """The 10 cross-strand interfaces to the twin phase."""
        return [i for i in self.interfaces if i.is_rung]


class TwinPairLifecycle:
    """
    The complete lifecycle of a twin pair double helix.
    
    Structure:
    - 2 strands (Ring A toroidal, Ring B poloidal)
    - 10 phases per strand (20 cells total)
    - 100 vortex-states (vertices)
    - 200 transition pathways (edges)
    - 120 pentagonal interfaces (20 backbone + 100 rungs)
    
    The phase-locked base pairing: Phase N on strand A interfaces
    with phase N on strand B through their 10 shared pentagonal faces.
    """
    
    def __init__(self, twin_pair_id: int):
        """
        Initialize a twin pair lifecycle.
        
        Args:
            twin_pair_id: ID of this twin pair (0-5)
        """
        self.twin_pair_id = twin_pair_id
        self.strand_a_phases: Dict[LifecyclePhase, PhaseCell] = {}
        self.strand_b_phases: Dict[LifecyclePhase, PhaseCell] = {}
        self.vortex_states: List[VortexState] = []
        self.interfaces: List[PentagonalInterface] = []
        
    def build_lifecycle(self):
        """Build the complete twin pair lifecycle structure."""
        vertex_counter = 0
        face_counter = 0
        
        # Create 10 phases for each strand
        # Each twin pair has 100 total vortex-states: 50 per strand
        # So each phase cell has 5 vortex-states (50 / 10 = 5)
        for phase_num in range(1, 11):
            phase = LifecyclePhase(phase_num)
            
            # Strand A cell
            cell_a = PhaseCell(
                phase=phase,
                strand="A",
                dodecahedron_id=phase_num - 1
            )
            
            # Add 5 vortex states for this phase
            for _ in range(5):
                vortex = VortexState(
                    vertex_id=vertex_counter,
                    phase=phase,
                    strand="A"
                )
                cell_a.vortex_states.append(vortex)
                self.vortex_states.append(vortex)
                vertex_counter += 1
            
            self.strand_a_phases[phase] = cell_a
            
            # Strand B cell
            cell_b = PhaseCell(
                phase=phase,
                strand="B",
                dodecahedron_id=phase_num + 9  # 10-19
            )
            
            # Add 5 vortex states for this phase
            for _ in range(5):
                vortex = VortexState(
                    vertex_id=vertex_counter,
                    phase=phase,
                    strand="B"
                )
                cell_b.vortex_states.append(vortex)
                self.vortex_states.append(vortex)
                vertex_counter += 1
            
            self.strand_b_phases[phase] = cell_b
        
        # Create backbone interfaces (2 per cell × 20 cells = 40 total,
        # but each is shared by 2 cells, so 20 unique)
        for phase_num in range(1, 11):
            phase = LifecyclePhase(phase_num)
            next_phase = LifecyclePhase((phase_num % 10) + 1)
            
            # Strand A backbone
            interface = PentagonalInterface(
                face_id=face_counter,
                vertices=[0, 1, 2, 3, 4],  # Placeholder
                edges=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)],
                interface_type="backbone",
                phase_a=phase,
                phase_b=next_phase
            )
            self.strand_a_phases[phase].interfaces.append(interface)
            self.interfaces.append(interface)
            face_counter += 1
            
            # Strand B backbone
            interface = PentagonalInterface(
                face_id=face_counter,
                vertices=[0, 1, 2, 3, 4],  # Placeholder
                edges=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)],
                interface_type="backbone",
                phase_a=phase,
                phase_b=next_phase
            )
            self.strand_b_phases[phase].interfaces.append(interface)
            self.interfaces.append(interface)
            face_counter += 1
        
        # Create inter-strand rungs (100 total)
        # Each phase on strand A connects to matching phase on strand B
        # with 10 pentagonal rungs (5 per cell × 2 cells / 2 since shared)
        for phase_num in range(1, 11):
            phase = LifecyclePhase(phase_num)
            
            # Create 10 rungs between matching phases
            for _ in range(10):
                interface = PentagonalInterface(
                    face_id=face_counter,
                    vertices=[0, 1, 2, 3, 4],  # Placeholder
                    edges=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)],
                    interface_type="rung",
                    phase_a=phase,
                    phase_b=phase  # Phase-locked: same phase on both strands
                )
                self.strand_a_phases[phase].interfaces.append(interface)
                self.strand_b_phases[phase].interfaces.append(interface)
                self.interfaces.append(interface)
                face_counter += 1
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get lifecycle statistics.
        
        Returns:
            Dictionary with counts of all elements
        """
        backbone_count = sum(
            1 for i in self.interfaces if i.is_backbone
        )
        rung_count = sum(
            1 for i in self.interfaces if i.is_rung
        )
        
        return {
            "twin_pair_id": self.twin_pair_id,
            "num_strands": 2,
            "phases_per_strand": 10,
            "total_phases": 20,
            "total_vortex_states": len(self.vortex_states),
            "total_interfaces": len(self.interfaces),
            "backbone_interfaces": backbone_count,
            "rung_interfaces": rung_count,
            "vortex_states_per_strand": len(self.vortex_states) // 2,
        }
    
    def get_phase_description(self, phase: LifecyclePhase) -> str:
        """
        Get a description of the given lifecycle phase.
        
        Args:
            phase: The lifecycle phase
            
        Returns:
            Textual description of the phase
        """
        descriptions = {
            LifecyclePhase.INCEPTION: (
                "Inception - The seed state where potential coalesces. "
                "Initial resonance attracts participants."
            ),
            LifecyclePhase.FORMATION: (
                "Formation - Initial structure emerges. "
                "Trust edges begin to form between vertices."
            ),
            LifecyclePhase.STRUCTURING: (
                "Structuring - Pattern crystallizes into recognizable form. "
                "Working groups solidify."
            ),
            LifecyclePhase.INTEGRATION: (
                "Integration - Coherence builds across components. "
                "Interfaces strengthen and communication flows increase."
            ),
            LifecyclePhase.CULMINATION: (
                "Culmination - The apex of the cycle, maximum curvature. "
                "Peak influence and energy concentration."
            ),
            LifecyclePhase.DISTRIBUTION: (
                "Distribution - Energy disperses outward from the apex. "
                "Influence spreads through the network."
            ),
            LifecyclePhase.REFINEMENT: (
                "Refinement - Optimization and fine-tuning occur. "
                "Non-essential elements are pruned."
            ),
            LifecyclePhase.CONSOLIDATION: (
                "Consolidation - Stabilization into sustainable form. "
                "Core patterns are locked in."
            ),
            LifecyclePhase.DISSOLUTION: (
                "Dissolution - Release and decomposition begin. "
                "Components return to the field for reuse."
            ),
            LifecyclePhase.SEED_REBIRTH: (
                "Seed/Rebirth - The distilled essence feeds the next cycle. "
                "Memory and learning transfer to Phase 1."
            ),
        }
        return descriptions.get(phase, "Unknown phase")
    
    def get_curvature_profile(self) -> Dict[LifecyclePhase, float]:
        """
        Get the curvature profile across phases.
        
        Phases 1-5: Ascending arc (increasing curvature)
        Phase 5: Maximum curvature at apex
        Phases 6-10: Descending arc (decreasing curvature)
        
        Returns:
            Dictionary mapping phase to normalized curvature (0-1)
        """
        # Simple model: sine wave peaking at phase 5
        profile = {}
        for phase_num in range(1, 11):
            phase = LifecyclePhase(phase_num)
            # Map 1-10 to 0-π for smooth curve peaking at 5
            angle = (phase_num - 1) * np.pi / 9
            curvature = np.sin(angle)
            profile[phase] = curvature
        
        return profile
    
    def compute_coordinate_degrees(self) -> int:
        """
        Compute total coordinate degrees.
        
        With 100 vortex-states and 3 coordinates per state (COM, ORG, ENT),
        there are 300 coordinate-degrees per lifecycle.
        
        Returns:
            Total number of coordinate degrees
        """
        return len(self.vortex_states) * 3
    
    def validate_structure(self) -> Dict[str, bool]:
        """
        Validate the twin pair lifecycle structure.
        
        Returns:
            Dictionary of validation checks
        """
        checks = {
            "100_vortex_states": len(self.vortex_states) == 100,
            "120_interfaces": len(self.interfaces) == 120,
            "20_backbone": sum(1 for i in self.interfaces if i.is_backbone) == 20,
            "100_rungs": sum(1 for i in self.interfaces if i.is_rung) == 100,
            "10_phases_strand_a": len(self.strand_a_phases) == 10,
            "10_phases_strand_b": len(self.strand_b_phases) == 10,
            "300_coordinate_degrees": self.compute_coordinate_degrees() == 300,
        }
        
        return checks


class CliffordTorusStructure:
    """
    The Clifford torus bridging structure connecting twin pairs.
    
    The 12 rings organize into a structure where each axial twin pair
    (2 rings threading through complementary solid tori) communicates
    through 5 bridging ring-pairs forming the ORG membrane.
    
    Structure:
    - 2 axial rings (Ring A and Ring B of a twin pair)
    - 5 bridging ring-pairs (10 rings total)
    - 100 cells in the connective tissue
    - Clifford torus (ORG membrane) between the strands
    """
    
    def __init__(self):
        """Initialize the Clifford torus structure."""
        self.axial_rings: List[int] = []  # 2 ring IDs
        self.bridging_pairs: List[Tuple[int, int]] = []  # 5 pairs of ring IDs
        
    def build_structure(self, twin_pair_id: int, all_ring_ids: List[int]):
        """
        Build the Clifford structure for a twin pair.
        
        Args:
            twin_pair_id: ID of the twin pair (0-5)
            all_ring_ids: List of all 12 ring IDs
        """
        # The two axial rings are the twin pair's rings
        self.axial_rings = [twin_pair_id * 2, twin_pair_id * 2 + 1]
        
        # The 5 bridging pairs are the other 10 rings organized into pairs
        other_rings = [r for r in all_ring_ids if r not in self.axial_rings]
        
        # Pair them up (simplified - actual structure is more complex)
        for i in range(0, len(other_rings), 2):
            if i + 1 < len(other_rings):
                self.bridging_pairs.append((other_rings[i], other_rings[i + 1]))
        
    @property
    def num_bridging_pairs(self) -> int:
        """Number of bridging ring-pairs (should be 5)."""
        return len(self.bridging_pairs)
    
    @property
    def pentagonal_bond(self) -> bool:
        """The pentagonal bond - 5 bridging pairs."""
        return self.num_bridging_pairs == 5
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get Clifford structure statistics.
        
        Returns:
            Dictionary with structural counts
        """
        return {
            "axial_rings": len(self.axial_rings),
            "bridging_ring_pairs": self.num_bridging_pairs,
            "total_bridging_rings": self.num_bridging_pairs * 2,
            "cells_in_bridging_rings": self.num_bridging_pairs * 2 * 10,
        }
