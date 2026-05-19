# Probabilistic Plan Recognition Using Classical Planning

This project implements probabilistic plan recognition using the approach proposed by Ramírez and Geffner (2010).

The system uses the Fast Downward classical planner to infer the most likely goal of an observed agent in the Blocksworld domain.

# Features

- Classical planning with Fast Downward
- Goal recognition
- Probability estimation
- PDDL domain and problem files
- Blocksworld environment
- Bayesian-style probability scoring

---

# Technologies Used

- Python 3
- Fast Downward Planner
- PDDL
- Blocksworld Domain

# Project Structure

```text
planner/
experiments/
domains/
```

# Running the System

## Run experiments

```bash
PYTHONPATH=. python3 experiments/test_run.py
```

## Run recognizer

```bash
PYTHONPATH=. python3 -m planner.recognizer
```

# Example Output

```text
Goal: (holding A)
Probability: 0.5761
```


# Reference

Ramírez, M., & Geffner, H. (2010).
Probabilistic Plan Recognition Using Off-the-Shelf Classical Planners.
Proceedings of AAAI 2010.