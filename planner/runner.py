import subprocess
import os

FD = os.path.expanduser("~/downward/fast-downward.py")

def run_planner(domain_path, problem_path):
    cmd = [
        "python3", FD,
        domain_path,
        problem_path,
        "--search", "astar(lmcut())"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr

    plan = []
    cost = None

    for line in output.splitlines():
        if "Plan cost:" in line:
            cost = int(line.split(":")[-1].strip())
        if line.startswith("[") is False and "(" in line and ")" in line:
            if "pick" in line or "stack" in line or "unstack" in line:
                plan.append(line.strip())

    return plan, cost