# Fair Water Allocation Using Cooperative Game Theory

A resource allocation model based on **cooperative game theory** for distributing limited water resources among agricultural users, comparing multiple allocation mechanisms and evaluating their environmental impact.

## Overview

Given a group of farmers with different water demands and sustainability indices, the program computes and compares how available water should be distributed under three distinct allocation criteria.

The objective is to identify allocations that are both efficient and environmentally responsible while balancing equity among participants.

---

## Implemented Allocation Methods

| Method                             | Description                                                                                               |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Priority-Based Allocation**      | Iteratively distributes water using weighted priorities based on inverse demand and sustainability scores |
| **Proportional Allocation**        | Allocates water proportionally to each farmer's demand                                                    |
| **Constrained Equal Awards (CEA)** | Minimizes individual allocation disparities through an equal-awards rule                                  |

---

## Features

* Interactive command-line interface with input validation
* Interactive **Plotly** visualizations:

  * Allocation comparison by farmer
  * Allocation comparison across methods
* Environmental impact assessment for each allocation strategy
* CSV export of all results

---

## Environmental Impact Analysis

In addition to computing water allocations, the system evaluates the environmental implications of each strategy using sustainability indicators associated with each participant.

This allows users to compare not only fairness and efficiency but also the ecological consequences of alternative allocation mechanisms.

---

## Technologies

* Python 3
* `numpy`
* `pandas`
* `plotly` — interactive visualizations

---

## Running the Project

```bash id="h9gt0o"
pip install numpy pandas plotly
python ProyectoMaganaLuisa.py
```

The program will request:

1. Number of farmers
2. Water demand (liters) and sustainability index for each farmer
3. Total available water supply

---

## Outputs

After execution, the program generates:

* Interactive browser-based visualizations
* A CSV file named:

```text id="9iw89u"
comparacion_asignaciones.csv
```

containing all allocation results and environmental metrics.

---

## Example Output

```text id="e1s7wa"
Environmental Impact:

Priority-Based Allocation Impact:     142.3
Proportional Allocation Impact:       198.7
Constrained Equal Awards Impact:      175.4
```

---

## Educational and Research Context

This project explores the application of cooperative game theory principles to environmental resource management problems. It provides a practical framework for analyzing trade-offs between fairness, efficiency, and sustainability in water allocation scenarios, making it suitable for educational purposes and introductory research in resource optimization and decision-making.
