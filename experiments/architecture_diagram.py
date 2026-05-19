import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(11, 4.5))
ax.axis('tight')
ax.axis('off')

fig.patch.set_facecolor('white')

blocks = [
    (1.5, 3.2, "Candidate Goals\n(Hypotheses G)"),
    (4.5, 3.2, "Observation Tracker\n(Prefix Sequence O)"),
    (7.5, 3.2, "PDDL Compiler\n(Fluent Injection)"),
    (7.5, 1.2, "Classical Planner\n(Fast Downward)"),
    (4.5, 1.2, "Bayesian Scorer\n(Boltzmann Distribution)"),
    (1.5, 1.2, "Probabilistic Report\nPosterior P(G|O)")
]

box_width = 2.4
box_height = 0.8

for x_c, y_c, text in blocks:
    x_bl = x_c - (box_width / 2)
    y_bl = y_c - (box_height / 2)

    rect = patches.Rectangle(
        (x_bl, y_bl),
        box_width,
        box_height,
        linewidth=1.5,
        edgecolor='blue',
        facecolor='#F0F4F8'
    )

    ax.add_patch(rect)

    ax.text(
        x_c,
        y_c,
        text,
        ha='center',
        va='center',
        fontsize=10,
        fontweight='bold'
    )

def arrow(x1, y1, x2, y2):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="->",
            lw=2
        )
    )

arrow(2.7, 3.2, 3.3, 3.2)
arrow(5.7, 3.2, 6.3, 3.2)
arrow(7.5, 2.8, 7.5, 1.6)
arrow(6.3, 1.2, 5.7, 1.2)
arrow(3.3, 1.2, 2.7, 1.2)

fig.text(
    0.5,
    0.03,
    "Figure 1: Plan Recognition Pipeline Architecture",
    ha='center',
    fontsize=12,
    fontweight='bold'
)

plt.savefig(
    "Figure_1_Pipeline_Clean.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()