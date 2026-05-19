import sys
import os
import tempfile
import re

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from planner.runner import run_planner

BASE = os.path.dirname(os.path.abspath(__file__))

DOMAIN = os.path.abspath(
    os.path.join(
        BASE,
        "..",
        "domains",
        "blocksworld",
        "domain.pddl"
    )
)

BASE_PROBLEM = os.path.abspath(
    os.path.join(
        BASE,
        "..",
        "domains",
        "blocksworld",
        "problem.pddl"
    )
)

candidate_goals = [
    "(on A B)",
    "(on B A)",
    "(holding A)"
]


def make_problem(goal):

    new_problem = f"""
(define (problem bw-test)
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

    (:goal
        (and
            {goal}
        )
    )
)
"""

    tmp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pddl",
        mode="w"
    )

    tmp.write(new_problem)
    tmp.close()

    return tmp.name

print("DOMAIN:", DOMAIN)
print("BASE PROBLEM:", BASE_PROBLEM)

for goal in candidate_goals:

    print("\n====================")
    print("Testing goal:", goal)

    temp_problem = make_problem(goal)

    plan, cost = run_planner(
        DOMAIN,
        temp_problem
    )

    print("Cost:", cost)

    print("Plan:")
    for step in plan:
        print(" ", step)