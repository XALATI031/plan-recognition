import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create the canvas (width, height)
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.axis('tight')
ax.axis('off')

# Set figure background to white
fig.patch.set_facecolor('white')

# Define block coordinates and labels
# Format: (x_center, y_center, text_label)
blocks = [
    (1.5, 3.2, "Candidate Goals\n(Hypotheses $G$)"),
    (4.5, 3.2, "Observation Tracker\n(Prefix Sequence $O$)"),
    (7.5, 3.2, "PDDL Compiler\n(Fluent-Injection Modifications)"),
    (7.5, 1.2, "Classical Planner\n(Fast Downward Engine)"),
    (4.5, 1.2, "Bayesian Scorer\n(Boltzmann Distribution)"),
    (1.5, 1.2, "Probabilistic Report\n(Posterior $P(G|O)$ Matrix)")
]

# Set box styling dimensions
box_width = 2.4
box_height = 0.8

# Draw blocks dynamically
for x_c, y_c, text in blocks:
    x_bl = x_c - (box_width / 2)
    y_bl = y_c - (box_height / 2)

    rect = patches.Rectangle(
        (x_bl, y_bl), box_width, box_height,
        linewidth=1.5, edgecolor='#4C72B0', facecolor='#F0F4F8', zorder=2
    )
    ax.add_patch(rect)

    ax.text(
        x_c, y_c, text, ha='center', va='center',
        fontsize=10, color='#1A1A1A', fontweight='bold', zorder=3
    )

# Helper function to draw crisp directional arrows with safely padded text
def draw_arrow(x1, y1, x2, y2):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color='#4C72B0', lw=2),
        zorder=1
    )

# --- CONNECTING THE ARCHITECTURE ARROWS ---
# Box 1 to Box 2
draw_arrow(1.5 + (box_width/2), 3.2, 4.5 - (box_width/2), 3.2)
ax.text(3.0, 3.35, "1", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#4A4A4A')

# Box 2 to Box 3
draw_arrow(4.5 + (box_width/2), 3.2, 7.5 - (box_width/2), 3.2)
ax.text(6.0, 3.35, "2", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#4A4A4A')

# Box 3 down to Box 4
draw_arrow(7.5, 3.2 - (box_height/2), 7.5, 1.2 + (box_height/2))
ax.text(7.65, 2.2, "Creates $G+O$ & $G+\\overline{O}$ PDDL", ha='left', va='center', fontsize=9.5, color='#333333')

# Box 4 to Box 5
draw_arrow(7.5 - (box_width/2), 1.2, 4.5 + (box_width/2), 1.2)
ax.text(6.0, 1.35, "Extracts Plan Costs $c(G+O)$ & $c(G+\\overline{O})$", ha='center', va='bottom', fontsize=9.5, color='#333333')

# Box 5 to Box 6
draw_arrow(4.5 - (box_width/2), 1.2, 1.5 + (box_width/2), 1.2)
ax.text(3.0, 1.35, "5", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#4A4A4A')


# Configure plot canvas layout bounds
ax.set_xlim(0, 10.5)
ax.set_ylim(0.0, 4.2)

# FIXED: Title placed underneath the entire architecture layout
fig.text(0.5, 0.05, "Figure 1: Generative Plan Recognition System Pipeline Architecture",
         fontsize=12, fontweight='bold', ha='center', color='#1A1A1A')

# Save the tidy figure as a high-resolution PNG file
plt.savefig("Figure_1_Pipeline_Clean.png", dpi=300, bbox_inches='tight')
plt.show()
