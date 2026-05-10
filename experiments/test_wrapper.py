import sys
import os
sys.path.append(os.path.expanduser("~/plan_recognition"))


from planner.runner import run_planner

domain = "/Users/xalatimaluleke/plan_recognition/domains/blocksworld/domain.pddl"
problem = "/Users/xalatimaluleke/plan_recognition/domains/blocksworld/problem.pddl"

output = run_planner(domain, problem)

print(output)