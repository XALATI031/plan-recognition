import subprocess
import tempfile
import math
import os
import matplotlib.pyplot as plt

FD_PATH = os.path.expanduser(
    "~/downward/fast-downward.py"
)

CANDIDATE_GOALS = [
    "(on A B)",
    "(on B A)",
    "(holding A)"
]

BETA = 1.0

# ---------------------------------------------------
# CREATE FILES
# ---------------------------------------------------

def create_files(goal, obs_level):

    pickup_obs = "(obs-1)" if obs_level >= 1 else ""

    stack_obs = (
        "(when (obs-1) (obs-2))"
        if obs_level == 2
        else ""
    )

    if obs_level == 0:

        final_obs = ""

        compliant_goal = f"(and {goal})"

        non_compliant_goal = (
            "(and "
            + goal +
            " (not (= 1 1)))"
        )

    else:

        final_obs = (
            "(obs-1)"
            if obs_level == 1
            else "(obs-2)"
        )

        compliant_goal = (
            f"(and {goal} {final_obs})"
        )

        non_compliant_goal = (
            f"(and {goal} (not {final_obs}))"
        )

    domain_content = f"""
(define (domain blocksworld)

  (:requirements
    :strips
    :negative-preconditions
    :conditional-effects
  )

  (:predicates
    (on ?x ?y)
    (ontable ?x)
    (clear ?x)
    (holding ?x)
    (handempty)
    (obs-1)
    (obs-2)
  )

  (:action pick-up
    :parameters (?x)
    :precondition
      (and
        (clear ?x)
        (ontable ?x)
        (handempty)
      )
    :effect
      (and
        (holding ?x)
        (not (ontable ?x))
        (not (clear ?x))
        (not (handempty))
        {pickup_obs}
      )
  )

  (:action stack
    :parameters (?x ?y)
    :precondition
      (and
        (holding ?x)
        (clear ?y)
      )
    :effect
      (and
        (on ?x ?y)
        (clear ?x)
        (handempty)
        (not (holding ?x))
        (not (clear ?y))
        {stack_obs}
      )
  )
)
"""

    compliant_problem = f"""
(define (problem bw-1)

  (:domain blocksworld)

  (:objects
    A B
  )

  (:init
    (ontable A)
    (ontable B)
    (clear A)
    (clear B)
    (handempty)
  )

  (:goal {compliant_goal})
)
"""

    non_compliant_problem = f"""
(define (problem bw-1)

  (:domain blocksworld)

  (:objects
    A B
  )

  (:init
    (ontable A)
    (ontable B)
    (clear A)
    (clear B)
    (handempty)
  )

  (:goal {non_compliant_goal})
)
"""

    d_temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pddl",
        mode="w"
    )

    d_temp.write(domain_content)
    d_temp.close()

    p_comp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pddl",
        mode="w"
    )

    p_comp.write(compliant_problem)
    p_comp.close()

    p_non = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pddl",
        mode="w"
    )

    p_non.write(non_compliant_problem)
    p_non.close()

    return (
        d_temp.name,
        p_comp.name,
        p_non.name
    )

# ---------------------------------------------------
# RUN PLANNER
# ---------------------------------------------------

def run_planner(domain_file, problem_file):

    cmd = [
        "python3",
        FD_PATH,
        domain_file,
        problem_file,
        "--search",
        "astar(blind())"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():

        if "Plan cost:" in line:

            return int(
                line.split(":")[-1].strip()
            )

    return float("inf")

# ---------------------------------------------------
# COMPUTE PROBABILITIES
# ---------------------------------------------------

history = {
    goal: []
    for goal in CANDIDATE_GOALS
}

for t in range(3):

    step_results = []

    for goal in CANDIDATE_GOALS:

        d_mod, p_comp, p_non = create_files(
            goal,
            t
        )

        cost_O = run_planner(
            d_mod,
            p_comp
        )

        cost_not_O = (
            float("inf")
            if t == 0
            else run_planner(
                d_mod,
                p_non
            )
        )

        if cost_O == float("inf"):

            likelihood = 0

        elif cost_not_O == float("inf"):

            likelihood = 1

        else:

            numerator = math.exp(
                -BETA * cost_O
            )

            denominator = (
                numerator
                +
                math.exp(
                    -BETA * cost_not_O
                )
            )

            likelihood = (
                numerator / denominator
            )

        prior = (
            math.exp(-BETA * cost_O)
            if cost_O != float("inf")
            else 0
        )

        posterior = likelihood * prior

        step_results.append({
            "goal": goal,
            "posterior": posterior
        })

        os.unlink(d_mod)
        os.unlink(p_comp)
        os.unlink(p_non)

    total = sum(
        r["posterior"]
        for r in step_results
    )

    for r in step_results:

        probability = (
            r["posterior"] / total
            if total > 0
            else 0
        )

        history[r["goal"]].append(
            probability
        )

# ---------------------------------------------------
# CREATE GRAPH
# ---------------------------------------------------

fig, ax = plt.subplots(
    figsize=(8, 5)
)

time_steps = [0, 1, 2]

labels = [
    "t=0",
    "t=1",
    "t=2"
]

for goal in CANDIDATE_GOALS:

    ax.plot(
        time_steps,
        history[goal],
        marker="o",
        linewidth=2,
        label=goal
    )

ax.set_xlabel(
    "Observation Sequence"
)

ax.set_ylabel(
    "Posterior Probability"
)

ax.set_xticks(time_steps)

ax.set_xticklabels(labels)

ax.set_ylim(0, 1)

ax.grid(True)

ax.legend()

plt.title(
    "Posterior Goal Probabilities Over Time"
)

plt.savefig(
    "Figure_2_Probabilities.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()