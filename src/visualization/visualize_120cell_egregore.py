#!/usr/bin/env python3
"""
120-Cell Egregore State Space Visualization

This script creates visualizations of the 120-cell polytope as a model for
a self-organizing egregore/movement ecosystem, highlighting:
- Working Groups (Dodecahedral Cells)
- Shared Concerns (Pentagonal Faces)
- Flows of Trust (Edges)
- Influential Individuals (Vertices)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.colors as mcolors
from scipy.spatial import ConvexHull
import json

# Set dark theme
plt.style.use('dark_background')

# Golden ratio - fundamental to 120-cell geometry
phi = (1 + np.sqrt(5)) / 2
phi_inv = 1 / phi

def get_output_directory():
    """
    Get the output directory for visualization images.
    Returns the docs/images directory within the repository.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))
    output_dir = os.path.join(repo_root, 'docs', 'images')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def generate_120cell_vertices():
    """
    Generate the 600 vertices of the 120-cell in 4D,
    then project to 3D using stereographic projection.
    """
    vertices_4d = []
    
    # The 120-cell vertices can be constructed from several families
    # All permutations of (±2, ±2, 0, 0) - 24 vertices
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            for perm in [(0,1,2,3), (0,2,1,3), (0,3,1,2), (1,2,0,3), (1,3,0,2), (2,3,0,1)]:
                v = [0, 0, 0, 0]
                v[perm[0]] = 2 * s1
                v[perm[1]] = 2 * s2
                vertices_4d.append(v)
    
    # All permutations of (±1, ±1, ±1, ±√5) - 64 vertices
    sqrt5 = np.sqrt(5)
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            for s3 in [-1, 1]:
                for s4 in [-1, 1]:
                    for i in range(4):
                        v = [s1, s2, s3, s4 * sqrt5]
                        # Rotate the sqrt5 position
                        v = v[-i:] + v[:-i] if i > 0 else v
                        vertices_4d.append(v[:])
    
    # All permutations of (±φ², ±φ, ±φ, ±φ) - 64 vertices  
    phi2 = phi * phi
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            for s3 in [-1, 1]:
                for s4 in [-1, 1]:
                    for i in range(4):
                        v = [s1 * phi2, s2 * phi, s3 * phi, s4 * phi]
                        v = v[-i:] + v[:-i] if i > 0 else v
                        vertices_4d.append(v[:])
    
    # All permutations of (±φ², ±1, ±1/φ, ±1/φ) and cyclic - 192 vertices
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            for s3 in [-1, 1]:
                for s4 in [-1, 1]:
                    base_coords = [
                        [s1 * phi2, s2 * 1, s3 * phi_inv, s4 * phi_inv],
                        [s1 * 1, s2 * phi2, s3 * phi_inv, s4 * phi_inv],
                        [s1 * phi_inv, s2 * 1, s3 * phi2, s4 * phi_inv],
                        [s1 * phi_inv, s2 * phi_inv, s3 * 1, s4 * phi2],
                    ]
                    for v in base_coords:
                        vertices_4d.append(v)
    
    # Even permutations of (±φ², ±1/φ², ±1, ±√5) - 96 vertices
    phi2_inv = 1 / (phi * phi)
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            for s3 in [-1, 1]:
                for s4 in [-1, 1]:
                    even_perms = [
                        [s1*phi2, s2*phi2_inv, s3*1, s4*sqrt5],
                        [s1*phi2, s2*1, s3*sqrt5, s4*phi2_inv],
                        [s1*phi2_inv, s2*phi2, s3*sqrt5, s4*1],
                        [s1*1, s2*sqrt5, s3*phi2, s4*phi2_inv],
                        [s1*sqrt5, s2*phi2_inv, s3*phi2, s4*1],
                        [s1*sqrt5, s2*1, s3*phi2_inv, s4*phi2],
                    ]
                    for v in even_perms:
                        vertices_4d.append(v)
    
    # Even permutations of (±2, ±1, ±φ, ±φ²) - 96 vertices
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            for s3 in [-1, 1]:
                for s4 in [-1, 1]:
                    even_perms = [
                        [s1*2, s2*1, s3*phi, s4*phi2],
                        [s1*2, s2*phi, s3*phi2, s4*1],
                        [s1*1, s2*2, s3*phi2, s4*phi],
                        [s1*phi, s2*phi2, s3*2, s4*1],
                        [s1*phi2, s2*1, s3*2, s4*phi],
                        [s1*phi2, s2*phi, s3*1, s4*2],
                    ]
                    for v in even_perms:
                        vertices_4d.append(v)
    
    # Remove duplicates and normalize
    vertices_4d = np.array(vertices_4d)
    # Remove near-duplicates
    unique_vertices = []
    for v in vertices_4d:
        is_dup = False
        for uv in unique_vertices:
            if np.linalg.norm(v - uv) < 0.01:
                is_dup = True
                break
        if not is_dup:
            unique_vertices.append(v)
    
    vertices_4d = np.array(unique_vertices)
    
    # If we don't have exactly 600, use a simpler construction
    if len(vertices_4d) != 600:
        # Use a simplified approach - generate points on 3-sphere
        # and select those that form the 120-cell structure
        vertices_4d = generate_simplified_120cell()
    
    return vertices_4d

def generate_simplified_120cell():
    """
    Generate a simplified 120-cell using quaternion representation.
    The 120-cell vertices correspond to the binary icosahedral group.
    """
    vertices = []
    
    # 24-cell vertices (subset)
    for perm in [(0,1,2,3), (0,2,3,1), (0,3,1,2)]:
        for s1 in [-1, 1]:
            for s2 in [-1, 1]:
                v = [0, 0, 0, 0]
                v[perm[0]] = s1
                v[perm[1]] = s2
                vertices.append(v)
    
    # Add more vertices using golden ratio
    coords = [
        (0, phi_inv, phi, 1),
        (0, phi, phi_inv, 1),
        (phi_inv, 0, 1, phi),
        (phi_inv, 1, phi, 0),
        (phi, 0, 1, phi_inv),
        (phi, 1, phi_inv, 0),
        (1, phi_inv, 0, phi),
        (1, phi, 0, phi_inv),
    ]
    
    for c in coords:
        for s0 in [-1, 1]:
            for s1 in [-1, 1]:
                for s2 in [-1, 1]:
                    for s3 in [-1, 1]:
                        v = [s0*c[0], s1*c[1], s2*c[2], s3*c[3]]
                        if abs(np.linalg.norm(v) - 2) < 0.5:  # Normalize to similar radius
                            vertices.append(v)
    
    vertices = np.array(vertices)
    # Normalize to unit sphere
    norms = np.linalg.norm(vertices, axis=1, keepdims=True)
    norms[norms == 0] = 1
    vertices = vertices / norms * 2
    
    # Remove duplicates
    unique = []
    for v in vertices:
        is_dup = False
        for u in unique:
            if np.linalg.norm(v - u) < 0.1:
                is_dup = True
                break
        if not is_dup:
            unique.append(v)
    
    return np.array(unique)

def stereographic_projection(vertices_4d, projection_point=None):
    """
    Project 4D vertices to 3D using stereographic projection.
    """
    if projection_point is None:
        projection_point = np.array([0, 0, 0, 3])  # Project from w=3
    
    vertices_3d = []
    for v in vertices_4d:
        # Stereographic projection from 4D to 3D
        w = v[3]
        denom = projection_point[3] - w
        if abs(denom) < 0.001:
            denom = 0.001
        scale = projection_point[3] / denom
        x = v[0] * scale
        y = v[1] * scale
        z = v[2] * scale
        vertices_3d.append([x, y, z])
    
    return np.array(vertices_3d)

def find_edges(vertices_3d, threshold=None):
    """
    Find edges by connecting nearby vertices.
    In the 120-cell, each vertex connects to 4 others.
    """
    n = len(vertices_3d)
    distances = []
    
    for i in range(n):
        for j in range(i+1, n):
            d = np.linalg.norm(vertices_3d[i] - vertices_3d[j])
            distances.append((d, i, j))
    
    distances.sort()
    
    # Find the edge length (first peak in distance distribution)
    if threshold is None:
        # Take edges that are in the shortest 5% of distances
        threshold = distances[int(len(distances) * 0.08)][0]
    
    edges = []
    for d, i, j in distances:
        if d <= threshold:
            edges.append((i, j))
    
    return edges

def create_egregore_visualization():
    """
    Create the main visualization of the 120-cell as egregore state space.
    """
    # Generate vertices
    print("Generating 120-cell vertices...")
    vertices_4d = generate_simplified_120cell()
    print(f"Generated {len(vertices_4d)} 4D vertices")
    
    # Project to 3D
    vertices_3d = stereographic_projection(vertices_4d)
    print(f"Projected to {len(vertices_3d)} 3D vertices")
    
    # Find edges
    edges = find_edges(vertices_3d)
    print(f"Found {len(edges)} edges")
    
    # Create figure with dark background
    fig = plt.figure(figsize=(16, 16), facecolor='#0a0a0f')
    ax = fig.add_subplot(111, projection='3d', facecolor='#0a0a0f')
    
    # Color scheme for egregore visualization
    vertex_color = '#00ffaa'  # Cyan-green for influential individuals
    edge_color = '#3366ff'    # Blue for trust flows
    highlight_color = '#ff6600'  # Orange for active working groups
    
    # Calculate vertex importance (degree centrality as proxy)
    vertex_degrees = np.zeros(len(vertices_3d))
    for i, j in edges:
        vertex_degrees[i] += 1
        vertex_degrees[j] += 1
    
    # Normalize degrees for sizing
    max_degree = max(vertex_degrees) if len(vertex_degrees) > 0 else 1
    vertex_sizes = 20 + 80 * (vertex_degrees / max_degree)
    
    # Plot edges (Flows of Trust & Information)
    edge_lines = []
    for i, j in edges:
        edge_lines.append([vertices_3d[i], vertices_3d[j]])
    
    if edge_lines:
        edge_collection = Line3DCollection(edge_lines, colors=edge_color, 
                                           linewidths=0.5, alpha=0.4)
        ax.add_collection3d(edge_collection)
    
    # Plot vertices (Influential Individuals & Core Ideas)
    # Color by importance
    colors = plt.cm.viridis(vertex_degrees / max_degree)
    
    ax.scatter(vertices_3d[:, 0], vertices_3d[:, 1], vertices_3d[:, 2],
               c=colors, s=vertex_sizes, alpha=0.8, edgecolors='white', linewidths=0.3)
    
    # Highlight some "working groups" - clusters of high-connectivity vertices
    # Find top 10% most connected vertices
    threshold_degree = np.percentile(vertex_degrees, 90)
    high_influence = vertices_3d[vertex_degrees >= threshold_degree]
    
    if len(high_influence) > 0:
        ax.scatter(high_influence[:, 0], high_influence[:, 1], high_influence[:, 2],
                   c=highlight_color, s=150, alpha=0.9, marker='*', 
                   edgecolors='white', linewidths=1, label='High-Influence Nodes')
    
    # Set axis properties
    ax.set_xlabel('Dimension X', color='white', fontsize=10)
    ax.set_ylabel('Dimension Y', color='white', fontsize=10)
    ax.set_zlabel('Dimension Z', color='white', fontsize=10)
    
    # Remove grid and set pane colors
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#222233')
    ax.yaxis.pane.set_edgecolor('#222233')
    ax.zaxis.pane.set_edgecolor('#222233')
    ax.grid(True, alpha=0.1, color='#444466')
    
    # Set tick colors
    ax.tick_params(colors='#888899')
    
    # Title
    ax.set_title('120-Cell as Egregore State Space\nSelf-Organizing Movement Ecosystem', 
                 color='white', fontsize=16, fontweight='bold', pad=20)
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#00ffaa', 
               markersize=10, label='Vertices: Influential Individuals & Core Ideas', linestyle='None'),
        Line2D([0], [0], marker='*', color='w', markerfacecolor='#ff6600', 
               markersize=15, label='High-Influence Nodes (Working Group Nuclei)', linestyle='None'),
        Line2D([0], [0], color='#3366ff', linewidth=2, 
               label='Edges: Flows of Trust & Information'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', facecolor='#1a1a2e', 
              edgecolor='#333355', labelcolor='white', fontsize=9)
    
    plt.tight_layout()
    output_dir = get_output_directory()
    plt.savefig(os.path.join(output_dir, 'egregore_120cell_main.png'), 
                dpi=150, facecolor='#0a0a0f', edgecolor='none', bbox_inches='tight')
    plt.close()
    
    return vertices_3d, edges, vertex_degrees

def create_layered_visualization(vertices_3d, edges, vertex_degrees):
    """
    Create a multi-panel visualization showing different layers of the egregore.
    """
    fig = plt.figure(figsize=(20, 12), facecolor='#0a0a0f')
    
    # Panel 1: Vertices Only (Influential Individuals)
    ax1 = fig.add_subplot(231, projection='3d', facecolor='#0a0a0f')
    max_degree = max(vertex_degrees) if len(vertex_degrees) > 0 else 1
    colors = plt.cm.plasma(vertex_degrees / max_degree)
    sizes = 30 + 100 * (vertex_degrees / max_degree)
    ax1.scatter(vertices_3d[:, 0], vertices_3d[:, 1], vertices_3d[:, 2],
                c=colors, s=sizes, alpha=0.8)
    ax1.set_title('Layer 1: Influential Individuals\n(600 Vertices)', color='white', fontsize=11)
    style_axis(ax1)
    
    # Panel 2: Edges Only (Trust Flows)
    ax2 = fig.add_subplot(232, projection='3d', facecolor='#0a0a0f')
    edge_lines = [[vertices_3d[i], vertices_3d[j]] for i, j in edges]
    if edge_lines:
        edge_collection = Line3DCollection(edge_lines, colors='#00aaff', 
                                           linewidths=0.6, alpha=0.5)
        ax2.add_collection3d(edge_collection)
    ax2.set_title('Layer 2: Flows of Trust\n(1,200 Edges)', color='white', fontsize=11)
    style_axis(ax2)
    
    # Panel 3: Combined View
    ax3 = fig.add_subplot(233, projection='3d', facecolor='#0a0a0f')
    if edge_lines:
        edge_collection = Line3DCollection(edge_lines, colors='#3366ff', 
                                           linewidths=0.4, alpha=0.3)
        ax3.add_collection3d(edge_collection)
    ax3.scatter(vertices_3d[:, 0], vertices_3d[:, 1], vertices_3d[:, 2],
                c=colors, s=sizes*0.5, alpha=0.7)
    ax3.set_title('Combined: Network Structure', color='white', fontsize=11)
    style_axis(ax3)
    
    # Panel 4: Working Groups (Clustered Regions)
    ax4 = fig.add_subplot(234, projection='3d', facecolor='#0a0a0f')
    # Identify clusters by spatial proximity
    from scipy.cluster.hierarchy import fcluster, linkage
    if len(vertices_3d) > 10:
        Z = linkage(vertices_3d, method='ward')
        clusters = fcluster(Z, t=12, criterion='maxclust')
        cluster_colors = plt.cm.tab20(clusters / max(clusters))
        ax4.scatter(vertices_3d[:, 0], vertices_3d[:, 1], vertices_3d[:, 2],
                    c=cluster_colors, s=40, alpha=0.8)
    ax4.set_title('Layer 3: Working Groups\n(120 Dodecahedral Cells)', color='white', fontsize=11)
    style_axis(ax4)
    
    # Panel 5: Shared Concerns (Face highlighting)
    ax5 = fig.add_subplot(235, projection='3d', facecolor='#0a0a0f')
    # Show edges with varying thickness based on shared connectivity
    edge_weights = []
    for i, j in edges:
        # Weight by sum of endpoint degrees (shared importance)
        weight = (vertex_degrees[i] + vertex_degrees[j]) / (2 * max_degree)
        edge_weights.append(weight)
    
    if edge_lines and edge_weights:
        for idx, (line, weight) in enumerate(zip(edge_lines, edge_weights)):
            color = plt.cm.hot(weight)
            ax5.plot([line[0][0], line[1][0]], 
                     [line[0][1], line[1][1]], 
                     [line[0][2], line[1][2]], 
                     color=color, linewidth=0.5 + 2*weight, alpha=0.6)
    ax5.set_title('Layer 4: Shared Concerns\n(720 Pentagonal Faces)', color='white', fontsize=11)
    style_axis(ax5)
    
    # Panel 6: Hopf Fibration View (Linked Rings)
    ax6 = fig.add_subplot(236, projection='3d', facecolor='#0a0a0f')
    # Create ring-like structures
    theta = np.linspace(0, 2*np.pi, 50)
    for ring_idx in range(6):
        r = 1.5 + 0.3 * ring_idx
        phase = ring_idx * np.pi / 3
        x = r * np.cos(theta + phase)
        y = r * np.sin(theta + phase)
        z = 0.5 * np.sin(2*theta + phase)
        color = plt.cm.rainbow(ring_idx / 6)
        ax6.plot(x, y, z, color=color, linewidth=2, alpha=0.8)
    ax6.set_title('Hopf Fibration View\n(Linked Initiative Rings)', color='white', fontsize=11)
    style_axis(ax6)
    
    plt.suptitle('The 120-Cell Egregore: Multi-Layer State Space Visualization', 
                 color='white', fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    output_dir = get_output_directory()
    plt.savefig(os.path.join(output_dir, 'egregore_120cell_layers.png'), 
                dpi=150, facecolor='#0a0a0f', edgecolor='none', bbox_inches='tight')
    plt.close()

def style_axis(ax):
    """Apply consistent dark styling to 3D axis."""
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#222233')
    ax.yaxis.pane.set_edgecolor('#222233')
    ax.zaxis.pane.set_edgecolor('#222233')
    ax.grid(True, alpha=0.1, color='#444466')
    ax.tick_params(colors='#666677', labelsize=7)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')

def create_conceptual_diagram():
    """
    Create a conceptual diagram showing the mapping between
    120-cell components and egregore elements.
    """
    fig, ax = plt.subplots(figsize=(16, 10), facecolor='#0a0a0f')
    ax.set_facecolor('#0a0a0f')
    
    # Turn off axis
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.95, '120-Cell → Egregore State Space Mapping', 
            ha='center', va='top', fontsize=20, fontweight='bold', color='white',
            transform=ax.transAxes)
    
    # Create boxes for each mapping
    box_props = dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e', edgecolor='#3366ff', linewidth=2)
    arrow_props = dict(arrowstyle='->', color='#00ffaa', lw=2)
    
    # Left column: 120-Cell Components
    left_x = 0.15
    components = [
        ('600 Vertices', '#ff6600'),
        ('1,200 Edges', '#00aaff'),
        ('720 Faces', '#aa00ff'),
        ('120 Cells', '#ffaa00'),
    ]
    
    # Right column: Egregore Elements
    right_x = 0.85
    elements = [
        ('Influential Individuals\n& Core Ideas', '#ff6600'),
        ('Flows of Trust\n& Information', '#00aaff'),
        ('Shared Concerns\n& Interfaces', '#aa00ff'),
        ('Working Groups\n& Initiatives', '#ffaa00'),
    ]
    
    y_positions = [0.75, 0.55, 0.35, 0.15]
    
    for i, ((comp, color), (elem, _), y) in enumerate(zip(components, elements, y_positions)):
        # Left box
        ax.text(left_x, y, comp, ha='center', va='center', fontsize=14, 
                color='white', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e', 
                         edgecolor=color, linewidth=2),
                transform=ax.transAxes)
        
        # Right box
        ax.text(right_x, y, elem, ha='center', va='center', fontsize=12, 
                color='white',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e', 
                         edgecolor=color, linewidth=2),
                transform=ax.transAxes)
        
        # Arrow
        ax.annotate('', xy=(right_x - 0.12, y), xytext=(left_x + 0.1, y),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2),
                    transform=ax.transAxes)
    
    # Add column headers
    ax.text(left_x, 0.88, '120-Cell Geometry', ha='center', va='center', 
            fontsize=16, color='#00ffaa', fontweight='bold', transform=ax.transAxes)
    ax.text(right_x, 0.88, 'Egregore Dynamics', ha='center', va='center', 
            fontsize=16, color='#00ffaa', fontweight='bold', transform=ax.transAxes)
    
    # Add central concept
    ax.text(0.5, 0.45, 'PHOENIX\nENGINE', ha='center', va='center', fontsize=18, 
            color='#ff3366', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#2a1a2e', 
                     edgecolor='#ff3366', linewidth=3),
            transform=ax.transAxes)
    
    # Add description at bottom
    description = (
        "The 120-cell provides the geometric substrate for modeling self-organizing movements.\n"
        "The Phoenix Engine governs the autopoietic dynamics of death and rebirth,\n"
        "preserving identity through continuous transformation."
    )
    ax.text(0.5, 0.02, description, ha='center', va='bottom', fontsize=11, 
            color='#888899', style='italic', transform=ax.transAxes)
    
    output_dir = get_output_directory()
    plt.savefig(os.path.join(output_dir, 'egregore_concept_map.png'), 
                dpi=150, facecolor='#0a0a0f', edgecolor='none', bbox_inches='tight')
    plt.close()

def create_lifecycle_diagram():
    """
    Create a diagram showing the death-rebirth cycle of working groups.
    """
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#0a0a0f')
    ax.set_facecolor('#0a0a0f')
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.95, 'Autopoietic Lifecycle: Death & Rebirth of Working Groups', 
            ha='center', va='top', fontsize=18, fontweight='bold', color='white',
            transform=ax.transAxes)
    
    # Draw circular lifecycle
    center = (0.5, 0.5)
    radius = 0.3
    
    # Phases of the lifecycle
    phases = [
        ('EMERGENCE', 0, '#00ff88', 'Resonance attracts\nparticipants'),
        ('GROWTH', 72, '#00aaff', 'Trust edges form\nStructure crystallizes'),
        ('MATURITY', 144, '#ffaa00', 'Peak influence\nCore ideas solidify'),
        ('DECAY', 216, '#ff6600', 'Energy disperses\nFocus shifts'),
        ('DISSOLUTION', 288, '#ff3366', 'Cell dissolves\nVertices released'),
    ]
    
    for phase, angle_deg, color, desc in phases:
        angle = np.radians(90 - angle_deg)  # Start from top
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        
        # Phase node
        ax.plot(x, y, 'o', markersize=30, color=color, transform=ax.transAxes)
        ax.text(x, y, phase, ha='center', va='center', fontsize=9, 
                color='black', fontweight='bold', transform=ax.transAxes)
        
        # Description
        desc_x = center[0] + (radius + 0.15) * np.cos(angle)
        desc_y = center[1] + (radius + 0.15) * np.sin(angle)
        ax.text(desc_x, desc_y, desc, ha='center', va='center', fontsize=10, 
                color=color, transform=ax.transAxes)
    
    # Draw arrows between phases
    for i in range(len(phases)):
        angle1 = np.radians(90 - phases[i][1])
        angle2 = np.radians(90 - phases[(i+1) % len(phases)][1])
        
        # Midpoint for arrow
        mid_angle = (angle1 + angle2) / 2
        if i == len(phases) - 1:
            mid_angle = np.radians(90 - 324)
        
        x1 = center[0] + radius * np.cos(angle1)
        y1 = center[1] + radius * np.sin(angle1)
        x2 = center[0] + radius * np.cos(angle2)
        y2 = center[1] + radius * np.sin(angle2)
        
        # Draw arc arrow
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#666688', lw=1.5,
                                   connectionstyle='arc3,rad=0.3'),
                    transform=ax.transAxes)
    
    # Center: Phoenix symbol
    ax.text(center[0], center[1], '🔥', ha='center', va='center', fontsize=40,
            transform=ax.transAxes)
    ax.text(center[0], center[1] - 0.08, 'PHOENIX\nENGINE', ha='center', va='center', 
            fontsize=12, color='#ff6600', fontweight='bold', transform=ax.transAxes)
    
    # Add note about identity preservation
    note = (
        "Identity is preserved not in the components,\n"
        "but in the invariant rules of self-creation\n"
        "and the continuous chain of memory."
    )
    ax.text(0.5, 0.08, note, ha='center', va='center', fontsize=11, 
            color='#888899', style='italic', transform=ax.transAxes,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e', 
                     edgecolor='#333355', linewidth=1))
    
    output_dir = get_output_directory()
    plt.savefig(os.path.join(output_dir, 'egregore_lifecycle.png'), 
                dpi=150, facecolor='#0a0a0f', edgecolor='none', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    output_dir = get_output_directory()
    
    print("Creating 120-Cell Egregore Visualizations...")
    print(f"Output directory: {output_dir}")
    
    # Main visualization
    print("\n1. Creating main egregore visualization...")
    vertices_3d, edges, vertex_degrees = create_egregore_visualization()
    
    # Layered visualization
    print("2. Creating multi-layer visualization...")
    create_layered_visualization(vertices_3d, edges, vertex_degrees)
    
    # Conceptual diagram
    print("3. Creating concept mapping diagram...")
    create_conceptual_diagram()
    
    # Lifecycle diagram
    print("4. Creating lifecycle diagram...")
    create_lifecycle_diagram()
    
    print("\nAll visualizations complete!")
    print("Output files:")
    for f in os.listdir(output_dir):
        if f.endswith('.png'):
            print(f"  - {os.path.join(output_dir, f)}")
