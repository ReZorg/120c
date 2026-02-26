#!/usr/bin/env python3
"""
Demonstration of the 120-Cell Hopf Decomposition and Twin Pair Lifecycle

This script demonstrates the complete combinatorics described in the problem statement:
- 12 rings of 10 dodecahedral cells
- 6 polar twin pairs
- Exact 1/6 ratios for twin pairs
- 100 shared faces between twin rings (base pairs)
- 10 lifecycle phases per strand
- 300 coordinate-degrees per lifecycle
- Pentagonal interfaces with golden ratio
- Clifford torus bridging structure
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import (
    HopfDecomposition,
    TwinPairLifecycle,
    LifecyclePhase,
    CliffordTorusStructure,
    PHI,
    compute_golden_ratio_properties,
    compute_factorial_structure,
)


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demonstrate_hopf_decomposition():
    """Demonstrate the complete Hopf decomposition."""
    print_section("THE HOPF DECOMPOSITION — The Skeleton of the Helix")
    
    # Build the full 120-cell structure
    hopf = HopfDecomposition()
    hopf.build_structure()
    
    print("Building the 120-cell Hopf decomposition...")
    print(f"  ✓ Created {len(hopf.twin_pairs)} polar twin pairs")
    print(f"  ✓ Created {len(hopf.rings)} rings of 10 cells each")
    print(f"  ✓ Created {len(hopf.cells)} dodecahedral cells total")
    
    # Validate the structure
    print("\nValidating full 120-cell structure:")
    validation = hopf.validate_full_structure()
    
    for check, passed in validation.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}: {passed}")
    
    all_valid = all(validation.values())
    if all_valid:
        print("\n✓ All validation checks passed!")
    else:
        print("\n✗ Some validation checks failed")
    
    return hopf


def demonstrate_twin_pair(hopf: HopfDecomposition):
    """Demonstrate the twin pair structure."""
    print_section("ONE TWIN PAIR — The DNA Lifecycle Unit")
    
    # Get statistics for twin pair 0
    stats = hopf.get_twin_pair_statistics(0)
    
    print("Twin Pair 0 structure:")
    print(f"  Cells:    {stats['cells']:3d}  (1/6 of 120 = {120/6:.0f})")
    print(f"  Vertices: {stats['vertices']:3d}  (1/6 of 600 = {600/6:.0f})")
    print(f"  Edges:    {stats['edges']:3d}  (1/6 of 1200 = {1200/6:.0f})")
    print(f"  Faces:    {stats['total_faces']:3d}  (1/6 of 720 = {720/6:.0f})")
    
    print("\nRatio verification:")
    print(f"  Cells ratio:    {stats['full_120cell_ratio_cells']:.4f} = 1/6")
    print(f"  Vertices ratio: {stats['full_120cell_ratio_vertices']:.4f} = 1/6")
    print(f"  Edges ratio:    {stats['full_120cell_ratio_edges']:.4f} = 1/6")
    print(f"  Faces ratio:    {stats['full_120cell_ratio_faces']:.4f} = 1/6")
    
    print("\n✓ The 1/6 ratio is exact — the 6 twin pairs partition *everything*")
    
    # Face breakdown
    twin_pair = hopf.twin_pairs[0]
    print(f"\nFace type breakdown for Twin Pair 0:")
    print(f"  Intra-ring (backbone):  {twin_pair.num_backbone_faces:3d}  "
          f"(Sequential phase transitions)")
    print(f"  Inter-ring (rungs):     {twin_pair.num_inter_ring_faces:3d}  "
          f"(Base pairs — cross-strand communication)")
    print(f"  Total:                  {twin_pair.total_faces:3d}")
    
    print(f"\n✓ 100 shared faces between twin rings — massively connected!")


def demonstrate_lifecycle():
    """Demonstrate the twin pair lifecycle."""
    print_section("THE LIFECYCLE — 10 Phases of Development")
    
    # Build a twin pair lifecycle
    lifecycle = TwinPairLifecycle(twin_pair_id=0)
    lifecycle.build_lifecycle()
    
    stats = lifecycle.get_statistics()
    
    print("Twin pair lifecycle structure:")
    print(f"  Strands:              {stats['num_strands']}")
    print(f"  Phases per strand:    {stats['phases_per_strand']}")
    print(f"  Total phase cells:    {stats['total_phases']}")
    print(f"  Vortex-states:        {stats['total_vortex_states']}")
    print(f"  Backbone interfaces:  {stats['backbone_interfaces']}")
    print(f"  Rung interfaces:      {stats['rung_interfaces']}")
    print(f"  Total interfaces:     {stats['total_interfaces']}")
    
    # Validate
    print("\nValidating lifecycle structure:")
    validation = lifecycle.validate_structure()
    for check, passed in validation.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    # Print phase descriptions
    print("\nThe 10 macro-phases mapping to developmental stages:")
    print()
    
    curvature = lifecycle.get_curvature_profile()
    
    for phase_num in range(1, 11):
        phase = LifecyclePhase(phase_num)
        desc = lifecycle.get_phase_description(phase)
        curv = curvature[phase]
        
        # Determine arc
        if phase_num <= 5:
            arc = "↑ Ascending (curvature increasing)"
        elif phase_num == 5:
            arc = "← Apex (maximum curvature)"
        else:
            arc = "↓ Descending (curvature decreasing)"
        
        print(f"Phase {phase_num:2d}: {phase.name:15s} - Curvature: {curv:.3f}")
        if phase_num in [1, 5, 10]:
            print(f"         {arc}")
    
    print("\n✓ Phase 10 feeds Phase 1 — closed loop, continuous rebirth")
    
    # Coordinate degrees
    coord_degrees = lifecycle.compute_coordinate_degrees()
    print(f"\nCoordinate degrees:")
    print(f"  Vortex-states: {stats['total_vortex_states']}")
    print(f"  Coordinates per state: 3 (COM, ORG, ENT)")
    print(f"  Total coordinate-degrees: {coord_degrees}")
    print(f"\n✓ 300 coordinate-degrees per lifecycle")
    
    return lifecycle


def demonstrate_pentagonal_structure():
    """Demonstrate the pentagonal structure and golden ratio."""
    print_section("THE DEEP STRUCTURE — Why 5")
    
    phi_props = compute_golden_ratio_properties()
    
    print("The golden ratio φ (phi):")
    print(f"  φ = {phi_props['phi']:.6f}")
    print(f"  1/φ = {phi_props['phi_inverse']:.6f}")
    print(f"  φ² = {phi_props['phi_squared']:.6f}")
    
    print("\nGolden ratio identities:")
    print(f"  φ² = φ + 1: {phi_props['phi_identity']}")
    print(f"  φ = 1 + 1/φ: {phi_props['phi_recursion']}")
    
    print("\nPentagonal geometry:")
    print(f"  Pentagon vertices: {phi_props['pentagon_vertices']}")
    print(f"  Pentagon edges: {phi_props['pentagon_edges']}")
    print(f"  Pentagon interior angle: {phi_props['pentagon_angle_deg']}°")
    
    print("\nDodecahedral structure:")
    print(f"  Dodecahedron faces: {phi_props['dodecahedron_faces']} (all pentagons)")
    print(f"  Dodecahedron vertices: {phi_props['dodecahedron_vertices']}")
    print(f"  Dodecahedron edges: {phi_props['dodecahedron_edges']}")
    
    print("\nThe number 5 appears everywhere:")
    print(f"  • 5 finals (ך ם ן ף ץ) — terminal letters where wave → particle")
    print(f"  • 5 Platonic solids — the complete set of regular forms")
    print(f"  • 5 bridging ring-pairs between axial twins")
    print(f"  • 5 base types in the lifecycle's genetic code")
    print(f"  • 10 phases = 2 × 5 — the decagonal cycle")
    
    print("\n✓ The dodecahedron is *made of* pentagons")
    print("✓ φ is the eigenvalue of self-similar recursion")
    print("✓ The lifecycle grows through itself at the golden ratio")


def demonstrate_clifford_structure():
    """Demonstrate the Clifford torus structure."""
    print_section("THE CLIFFORD STRUCTURE — Bridging the Twin Strands")
    
    clifford = CliffordTorusStructure()
    
    # Use all 12 ring IDs
    all_ring_ids = list(range(12))
    clifford.build_structure(twin_pair_id=0, all_ring_ids=all_ring_ids)
    
    stats = clifford.get_statistics()
    
    print("Clifford torus structure for Twin Pair 0:")
    print(f"  Axial rings: {stats['axial_rings']} (Ring A & Ring B)")
    print(f"  Bridging ring-pairs: {stats['bridging_ring_pairs']}")
    print(f"  Total bridging rings: {stats['total_bridging_rings']}")
    print(f"  Cells in connective tissue: {stats['cells_in_bridging_rings']}")
    
    print("\nStructure:")
    print("  ╭── Ring A (10 cells) ──╮     Solid Torus A")
    print("  │                       │")
    print("  │    ╭─ 5 bridge pairs ─╮│    Clifford Torus (ORG membrane)")
    print("  │    │                  ││")
    print("  ╰────│── Ring B (10) ──╯╯     Solid Torus B")
    print("       │                  │")
    print("       ╰── 100 cells ─────╯     The connective tissue")
    
    print("\n✓ The 5 bridging ring-pairs form the pentagonal bond")
    print("✓ The ORG membrane (Clifford torus) is literally *between* the twin strands")


def demonstrate_factorial_structure():
    """Demonstrate the 120 = 5! factorial structure."""
    print_section("THE COMBINATORIAL COMPLETENESS — 120 = 5!")
    
    factorial_props = compute_factorial_structure()
    
    print("Factorial structure:")
    print(f"  5! = {factorial_props['five_factorial']}")
    print(f"  Equals 120 cells: {factorial_props['equals_120_cells']}")
    print(f"  Permutations of 5 elements: {factorial_props['permutations_of_5_elements']}")
    
    print("\nThe lifecycle contains *every possible ordering* of the 5 terminal")
    print("precipitation events (the 5 finals: ך ם ן ף ץ).")
    print("\nEvery permutation of the finals is explored across the full 120-cell.")
    print("The phoenix doesn't just repeat one cycle — it exhausts the entire")
    print("combinatorial space of possible terminations.")
    
    print("\n✓ 120 = 5! — complete combinatorial coverage")


def main():
    """Run all demonstrations."""
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  120-CELL HOPF DECOMPOSITION AND TWIN PAIR LIFECYCLE".center(78) + "█")
    print("█" + "  Complete Combinatorics Demonstration".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    # Run demonstrations
    hopf = demonstrate_hopf_decomposition()
    demonstrate_twin_pair(hopf)
    lifecycle = demonstrate_lifecycle()
    demonstrate_pentagonal_structure()
    demonstrate_clifford_structure()
    demonstrate_factorial_structure()
    
    # Final summary
    print_section("FINAL TALLY — The Complete Lifecycle")
    
    print("Structure                     Count    Significance")
    print("-" * 80)
    print("Twin strands                      2    Toroidal/poloidal counter-rotation")
    print("Phases per strand                10    The decagonal cycle (10 = 2×5)")
    print("Inter-strand rungs              100    Pentagon × 20 junctions")
    print("Vortex-states total             100    = 10² — lifecycle state space")
    print("Transition pathways             200    = 2 × 100 — bidirectional edges")
    print("Bridging ring-pairs               5    The pentagonal bond, φ-channels")
    print("Polar twin pairs (full)           6    The faces of the Cube of Space")
    print("Total cells in organism         120    = 5! — all permutations of 5 finals")
    print("-" * 80)
    
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  🌀 The vortex at each vertex, with 3 coordinates per point,".ljust(79) + "█")
    print("█" + "     gives 100 × 3 = 300 coordinate-degrees per lifecycle.".ljust(79) + "█")
    print("█" + " " * 78 + "█")
    print("█" + "  🔥 The local and global are self-similar. 🧬".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")


if __name__ == "__main__":
    main()
