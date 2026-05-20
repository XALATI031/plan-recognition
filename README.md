# Probabilistic Plan Recognition using PDDL and Fast Downward

## Project Overview

This project implements a probabilistic plan recognition system using classical Artificial Intelligence planning techniques. The system predicts an agent’s hidden goal from partial observations by combining:

- PDDL planning
- Classical search
- Bayesian probability scoring
- Cost-based goal inference

The implementation uses the Fast Downward planner together with Python automation scripts to evaluate candidate goals, calculate posterior probabilities, and visualize probability evolution over time.

---

# Objectives

The objectives of this project are:

- Model planning environments using PDDL
- Generate valid plans using Fast Downward
- Infer hidden goals from observations
- Compute posterior probabilities using Bayesian inference
- Evaluate recognition quality using benchmark metrics
- Visualize probability evolution graphically

---

# Technologies Used

The following technologies and tools were used:

- Python 3
- PDDL (Planning Domain Definition Language)
- Fast Downward Planner
- Matplotlib
- Bayesian Inference
- Classical AI Planning

---

# Project Structure

```bash
plan_recognition/
│
├── domains/
│   └── blocksworld/
│       ├── domain.pddl
│       └── problem.pddl
│
├── planner/
│   ├── recognizer.py
│   └── planner_interface.py
│
├── experiments/
│   ├── basic_test.py
│   ├── benchmark.py
│   ├── variance_analysis.py
│   ├── probability_visualization.py
│   └── architecture_diagram.py
│
├── figures/
│   ├── Figure_1_Pipeline_Clean.png
│   └── Figure_2_Probabilities.png
│
├── requirements.txt
└── README.md
```

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/XALATI031/plan-recognition.git
cd plan-recognition
```

---

# Install Dependencies

Install matplotlib:

```bash
pip3 install matplotlib
```

---

# Fast Downward Setup

Clone the Fast Downward planner:

```bash
git clone https://github.com/aibasel/downward.git
```

Update the planner path inside the Python scripts:

```python
FD_PATH = "/path/to/downward/fast-downward.py"
```

Example:

```python
FD_PATH = "/Users/username/downward/fast-downward.py"
```

---

# Running the System

## 1. Run Basic Planning Test

```bash
PYTHONPATH=. python3 experiments/basic_test.py
```

This validates:
- planner integration
- plan generation
- domain execution

---

## 2. Run Goal Recognition

```bash
PYTHONPATH=. python3 -m planner.recognizer
```

This:
- evaluates candidate goals
- computes probabilities
- predicts the most likely goal

---

## 3. Run Benchmark Evaluation

```bash
PYTHONPATH=. python3 experiments/benchmark.py
```

This evaluates:
- execution time
- recognition quality
- spread metric

---

## 4. Run Variance Analysis

```bash
PYTHONPATH=. python3 experiments/variance_analysis.py
```

This measures:
- statistical stability
- reproducibility
- variance across multiple runs

---

## 5. Generate Probability Visualization

```bash
PYTHONPATH=. python3 experiments/probability_visualization.py
```

This generates:
- posterior probability graphs
- probability evolution figures

---

## 6. Generate Architecture Diagram

```bash
PYTHONPATH=. python3 experiments/architecture_diagram.py
```

This generates:
- the probabilistic recognition pipeline architecture

---

# Methodology

The system follows the following pipeline:

1. Define candidate goals
2. Observe partial action sequences
3. Modify planning problems using observation fluents
4. Generate plans using Fast Downward
5. Extract plan costs
6. Apply Bayesian scoring
7. Normalize posterior probabilities
8. Predict the most probable goal

---

# Bayesian Scoring Formula

The posterior probability is calculated using Bayesian inference:

\[
P(G|O) \propto P(O|G) \times P(G)
\]

Where:

- \(P(G|O)\) = posterior probability
- \(P(O|G)\) = observation likelihood
- \(P(G)\) = prior probability

The likelihood is computed using Boltzmann cost weighting:

\[
P(O|G) =
\frac{e^{-\beta c(G+O)}}
{e^{-\beta c(G+O)} + e^{-\beta c(G+\neg O)}}
\]

---

# Benchmark Results

| Observation Level | Time (s) | Q | S |
|------------------|----------|---|---|
| 50%              | 0.74     | 0 | 1 |
| 100%             | 0.71     | 1 | 2 |

---

# Interpretation of Metrics

## Q Metric (Quality)

Measures whether the correct hidden goal was successfully identified.

- Q = 1 → correct recognition
- Q = 0 → incorrect recognition

---

## S Metric (Spread)

Measures ambiguity in prediction.

- Lower S = better confidence
- Higher S = more uncertainty

---

# Example Output

```text
=== FINAL PREDICTION ===

Predicted Goal: (holding A)
Confidence: 0.5761
```

---

# Generated Figures

## Figure 1 — Pipeline Architecture

This figure illustrates the complete probabilistic plan recognition architecture, including:

- candidate goals
- observation tracking
- PDDL compilation
- planning
- Bayesian scoring
- posterior prediction

---

## Figure 2 — Probability Evolution

This figure shows how posterior goal probabilities evolve as more observations become available.

---

# Academic Concepts Demonstrated

This project demonstrates:

- Automated Planning
- Goal Recognition
- Plan Recognition
- Bayesian Inference
- Heuristic Search
- Probabilistic Reasoning
- PDDL Modelling
- Classical AI Planning

---

# Experimental Domain

## Blocksworld Domain

The Blocksworld domain models block stacking actions such as:

- pick-up
- stack
- put-down

This domain is widely used in AI planning research.

---

# Key Features

- PDDL-based planning
- Fast Downward integration
- Bayesian probability scoring
- Observation tracking
- Benchmark evaluation
- Statistical variance analysis
- Graph generation
- Architecture visualization

---

# Repository

GitHub Repository:

https://github.com/XALATI031/plan-recognition

---

# Authors

- Xalati Maluleke
- Group Members

---

# Conclusion

This project successfully demonstrates a probabilistic plan recognition framework capable of inferring hidden goals from partial observations using classical planning and Bayesian reasoning.

The implementation combines planning efficiency with probabilistic inference to create an interpretable and extensible goal recognition system suitable for academic AI research and experimentation.


# Reference

[1] Baker, C.L., Saxe, R. and Tenenbaum, J.B., 2009. Action understanding as inverse planning. Cognition, 113(3), pp.329-349.
[2] Geib, C.W. and Goldman, R.P., 2009. A probabilistic plan recognition algorithm based on plan tree grammars. Artificial Intelligence, 173(11), pp.1101-1132.
[3] Gundersen, O.E. and Kjensmo, S., 2018, April. State of the art: Reproducibility in artificial intelligence. In Proceedings of the AAAI conference on artificial intelligence (Vol. 32, No. 1).
[4] Helmert, M., 2006. The fast downward planning system. Journal of Artificial Intelligence Research, 26, pp.191-246.
[5] Helmert, M. and Domshlak, C., 2009, October. Landmarks, critical paths and abstractions: what’s the difference anyway?. In Proceedings of the international conference on automated planning and scheduling (Vol. 19, pp. 162-169).
[6] Mirsky, R., Galun, R., Gal, K. and Kaminka, G., 2022. Comparing Plan Recognition Algorithms Through Standard Plan Libraries. Frontiers in Artificial Intelligence, 4, p.732177.
[7] Ramırez, M. and Geffner, H., 2009, July. Plan recognition as planning. In Proceedings of the 21st international joint conference on Artifical intelligence. Morgan Kaufmann Publishers Inc (pp. 1778-1783).
[8] Ram´ırez, M. and Geffner, H., 2010, July. Probabilistic plan recognition using off-the-shelf classical planners. In Proceedings of the AAAI conference on artificial intelligence (Vol. 24, No. 1, pp. 1121-1126).
[9] Sohrabi, S., Riabov, A.V. and Udrea, O., 2016, July. Plan Recognition as Planning Revisited. In IJCAI (pp. 3258-3264).
[10] Sukthankar, G., Geib, C., Bui, H.H., Pynadath, D. and Goldman, R.P. eds., 2014. Plan, activity, and intent recognition: Theory and practice. Newnes.
