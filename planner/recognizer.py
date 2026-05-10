from planner.runner import run_planner
import tempfile
import re
import math

DOMAIN = "domains/blocksworld/domain.pddl"
PROBLEM = "domains/blocksworld/problem.pddl"

CANDIDATE_GOALS = [
    "(on A B)",
    "(on B A)",
    "(holding A)"
]

BETA = 1.0


def make_problem_with_goal(goal):

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


def evaluate_goal(goal):

    temp_problem = make_problem_with_goal(goal)

    plan, cost = run_planner(
        DOMAIN,
        temp_problem
    )

    if cost is None:
        cost = float("inf")

    return plan, cost


def compute_probability(cost):

    if cost == float("inf"):
        return 0

    return math.exp(-BETA * cost)


def main():

    results = {}

    total_probability = 0

    print("\n=== PLAN RECOGNITION RESULT ===\n")

    for goal in CANDIDATE_GOALS:

        plan, cost = evaluate_goal(goal)

        probability = compute_probability(cost)

        results[goal] = {
            "plan": plan,
            "cost": cost,
            "probability": probability
        }

        total_probability += probability

    best_goal = None
    best_prob = -1

    for goal, data in results.items():

        normalized = (
            data["probability"] / total_probability
        )

        print(f"Goal: {goal}")
        print(f"Cost: {data['cost']}")
        print(f"Probability: {normalized:.4f}")

        print("Plan:")
        for step in data["plan"]:
            print(" ", step)

        print()

        if normalized > best_prob:
            best_prob = normalized
            best_goal = goal

    print("=== FINAL PREDICTION ===")
    print(f"Predicted Goal: {best_goal}")
    print(f"Confidence: {best_prob:.4f}")


if __name__ == "__main__":
    main()