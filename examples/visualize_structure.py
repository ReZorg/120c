#!/usr/bin/env python3
"""
Visual Summary of 120-Cell Hopf Decomposition

Creates a text-based visualization showing the key structural relationships.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import HopfDecomposition, TwinPairLifecycle, PHI


def print_header(text: str, width: int = 80):
    """Print a centered header."""
    print("\n" + "═" * width)
    print(text.center(width))
    print("═" * width + "\n")


def visualize_twin_pair_structure():
    """Visualize the twin pair double helix structure."""
    print_header("TWIN PAIR STRUCTURE: The Double Helix")
    
    print("Ring A (Toroidal) - 10 Cells:")
    print("┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐")
    print("│ Ph 1 │ Ph 2 │ Ph 3 │ Ph 4 │ Ph 5 │ Ph 6 │ Ph 7 │ Ph 8 │ Ph 9 │ Ph10 │")
    print("└──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘")
    print("   │      │      │      │      │      │      │      │      │      │")
    print("  100 inter-ring rungs (pentagonal faces) — the base pairs")
    print("   │      │      │      │      │      │      │      │      │      │")
    print("┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐")
    print("│ Ph 1 │ Ph 2 │ Ph 3 │ Ph 4 │ Ph 5 │ Ph 6 │ Ph 7 │ Ph 8 │ Ph 9 │ Ph10 │")
    print("└──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘")
    print("Ring B (Poloidal) - 10 Cells")
    
    print("\nPhase-locked base pairing:")
    print("  • Phase 1A ↔ Phase 1B: 10 shared faces")
    print("  • Phase 2A ↔ Phase 2B: 10 shared faces")
    print("  • ... (same for all 10 phases)")
    print("  • Phase 10A ↔ Phase 10B: 10 shared faces")
    print("\n  Total: 10 phases × 10 faces = 100 inter-ring rungs")


def visualize_hopf_rings():
    """Visualize the 12 rings organization."""
    print_header("THE 12 HOPF RINGS — Organization into 6 Twin Pairs")
    
    pairs = [
        ("Twin Pair 0", "Ring 0 (A)", "Ring 1 (B)", "→ Face 0 of Cube of Space"),
        ("Twin Pair 1", "Ring 2 (A)", "Ring 3 (B)", "→ Face 1 of Cube of Space"),
        ("Twin Pair 2", "Ring 4 (A)", "Ring 5 (B)", "→ Face 2 of Cube of Space"),
        ("Twin Pair 3", "Ring 6 (A)", "Ring 7 (B)", "→ Face 3 of Cube of Space"),
        ("Twin Pair 4", "Ring 8 (A)", "Ring 9 (B)", "→ Face 4 of Cube of Space"),
        ("Twin Pair 5", "Ring 10 (A)", "Ring 11 (B)", "→ Face 5 of Cube of Space"),
    ]
    
    for pair_name, ring_a, ring_b, note in pairs:
        print(f"{pair_name:14s} = {ring_a:12s} + {ring_b:12s}  {note}")
    
    print("\nEach twin pair contains exactly 1/6 of all elements:")
    print("  • 20 cells (1/6 × 120)")
    print("  • 100 vertices (1/6 × 600)")
    print("  • 200 edges (1/6 × 1200)")
    print("  • 120 faces (1/6 × 720)")


def visualize_phase_cycle():
    """Visualize the 10-phase lifecycle."""
    print_header("THE 10-PHASE LIFECYCLE — Ascending & Descending Arcs")
    
    phases = [
        (1, "INCEPTION", "Seed state", "↑", 0.000),
        (2, "FORMATION", "Initial structure", "↑", 0.342),
        (3, "STRUCTURING", "Pattern emerges", "↑", 0.643),
        (4, "INTEGRATION", "Coherence builds", "↑", 0.866),
        (5, "CULMINATION", "Apex — max curvature", "●", 0.985),
        (6, "DISTRIBUTION", "Energy disperses", "↓", 0.985),
        (7, "REFINEMENT", "Optimization", "↓", 0.866),
        (8, "CONSOLIDATION", "Stabilization", "↓", 0.643),
        (9, "DISSOLUTION", "Release", "↓", 0.342),
        (10, "SEED_REBIRTH", "Feeds Phase 1", "↻", 0.000),
    ]
    
    print("                                    Curvature")
    print("Phase   Name              Description               │  Value")
    print("─" * 75)
    
    for num, name, desc, arrow, curv in phases:
        bar = "█" * int(curv * 40)
        print(f"  {num:2d}   {name:15s}  {desc:20s}  {arrow}  {bar}")
    
    print("\n↑ = Ascending arc (curvature increasing)")
    print("● = Apex (maximum curvature)")
    print("↓ = Descending arc (curvature decreasing)")
    print("↻ = Closed loop (Phase 10 → Phase 1)")


def visualize_combinatorics():
    """Visualize the key combinatorial relationships."""
    print_header("KEY COMBINATORIAL RELATIONSHIPS")
    
    print("Pentagon Structure (5 everywhere):")
    print("  ┌─────────────────────────────────────┐")
    print("  │        5 vertices per face          │")
    print("  │        5 edges per face             │")
    print("  │        5 Platonic solids            │")
    print("  │        5 finals (ך ם ן ף ץ)         │")
    print("  │        5 bridging ring-pairs        │")
    print("  │        10 phases = 2 × 5            │")
    print("  └─────────────────────────────────────┘")
    
    print("\nFactorial Structure:")
    print("  120 = 5! = 5 × 4 × 3 × 2 × 1")
    print("  Every permutation of 5 terminals explored")
    
    print(f"\nGolden Ratio φ:")
    print(f"  φ = {PHI:.6f}")
    print(f"  φ² = {PHI**2:.6f} = φ + 1")
    print(f"  1/φ = {1/PHI:.6f}")
    print("  The eigenvalue of self-similar recursion")
    
    print("\nCoordinate Degrees:")
    print("  100 vortex-states × 3 coordinates = 300")
    print("  (COM, ORG, ENT) per vertex")


def main():
    """Run all visualizations."""
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "120-CELL HOPF DECOMPOSITION — Visual Summary".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    visualize_hopf_rings()
    visualize_twin_pair_structure()
    visualize_phase_cycle()
    visualize_combinatorics()
    
    print("\n" + "─" * 80)
    print("The phoenix exhausts the entire combinatorial space. 🔥")
    print("The local and global are self-similar. 🌀")
    print("─" * 80 + "\n")


if __name__ == "__main__":
    main()
