import subprocess
import tempfile
import math
import time
import os

FD_PATH = os.path.expanduser(
    "~/downward/fast-downward.py"
)

CANDIDATE_GOALS = [
    "(on A B)",
    "(on B A)",
    "(holding A)"
]

HIDDEN_GOAL = "(on A B)"

BETA = 1.0


def create_files(goal, obs_level):

    pickup_obs = "(obs-1)" if obs_level >= 1 else ""

    stack_obs = (
        "(when (obs-1) (obs-2))"
        if obs_level == 2
        else ""
    )

    final_obs = (
        "(obs-1)"
        if obs_level == 1
        else "(obs-2)"
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

  (:action put-down
    :parameters (?x)

    :precondition
      (holding ?x)

    :effect
      (and
        (ontable ?x)
        (clear ?x)
        (handempty)
        (not (holding ?x))
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

  (:objects A B)

  (:init
    (ontable A)
    (ontable B)
    (clear A)
    (clear B)
    (handempty)
  )

  (:goal
    (and
      {goal}
      {final_obs}
    )
  )
)
"""

    noncompliant_problem = f"""
(define (problem bw-1)

  (:domain blocksworld)

  (:objects A B)

  (:init
    (ontable A)
    (ontable B)
    (clear A)
    (clear B)
    (handempty)
  )

  (:goal
    (and
      {goal}
      (not {final_obs})
    )
  )
)
"""

    d = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pddl",
        mode="w"
    )

    d.write(domain_content)
    d.close()

    c = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pddl",
        mode="w"
    )

    c.write(compliant_problem)
    c.close()

    n = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pddl",
        mode="w"
    )

    n.write(noncompliant_problem)
    n.close()

    return d.name, c.name, n.name


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


print("\n=== BENCHMARK RESULTS ===\n")

print(
    f"| {'Obs':<6} | {'Time':<8} | {'Q':<3} | {'S':<3} |"
)

print("-" * 40)

for pct, obs_level in [
    ("50%", 1),
    ("100%", 2)
]:

    start = time.time()

    results = []

    for goal in CANDIDATE_GOALS:

        d, c, n = create_files(
            goal,
            obs_level
        )

        cost_o = run_planner(d, c)

        cost_not_o = run_planner(d, n)

        if cost_o == float("inf"):
            probability = 0

        elif cost_not_o == float("inf"):
            probability = 1

        else:

            probability = (
                math.exp(-BETA * cost_o)
                /
                (
                    math.exp(-BETA * cost_o)
                    +
                    math.exp(-BETA * cost_not_o)
                )
            )

        prior = math.exp(
            -BETA * cost_o
        )

        posterior = probability * prior

        results.append({
            "goal": goal,
            "posterior": posterior
        })

        os.unlink(d)
        os.unlink(c)
        os.unlink(n)

    end = time.time()

    runtime = round(end - start, 2)

    max_prob = max(
        r["posterior"]
        for r in results
    )

    best_goals = [
        r["goal"]
        for r in results
        if r["posterior"] == max_prob
    ]

    Q = (
        1
        if HIDDEN_GOAL in best_goals
        else 0
    )

    S = len(best_goals)

    print(
        f"| {pct:<6} | "
        f"{runtime:<8} | "
        f"{Q:<3} | "
        f"{S:<3} |"
    )