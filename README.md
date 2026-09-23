# FastBox Delivery Simulator

A Python-based logistics simulator for the FastBox fictional delivery system.

The program reads warehouse, delivery agent, and package information from a JSON file, assigns each package to the nearest delivery agent, simulates the delivery journey, calculates delivery efficiency, and generates a final JSON report.

## Features

* JSON input parsing
* Euclidean distance calculation
* Nearest-agent package assignment
* Delivery route simulation
* Per-agent distance calculation
* Package delivery count
* Delivery efficiency calculation
* Most efficient agent identification
* JSON report generation
* Input validation
* Support for multiple test cases

## Project Structure

```text
fastbox_delivery/
│
├── main.py
├── README.md
├── report.json
│
├── test_cases/
│   ├── test_case_1.json
│   ├── test_case_2.json
│   ├── test_case_3.json
│   ├── test_case_4.json
│   ├── test_case_5.json
│   ├── test_case_6.json
│   ├── test_case_7.json
│   ├── test_case_8.json
│   ├── test_case_9.json
│   └── test_case_10.json
│
└── reports/
    ├── report_test_case_1.json
    ├── report_test_case_2.json
    ├── report_test_case_3.json
    ├── report_test_case_4.json
    ├── report_test_case_5.json
    ├── report_test_case_6.json
    ├── report_test_case_7.json
    ├── report_test_case_8.json
    ├── report_test_case_9.json
    └── report_test_case_10.json
```

## Requirements

* Python 3.x
* No external Python libraries are required.

The implementation uses Python standard-library modules only:

* `json`
* `math`
* `sys`

## Input Format

The program accepts JSON containing:

```json
{
    "warehouses": {
        "W1": [0, 0],
        "W2": [50, 75]
    },
    "agents": {
        "A1": [5, 5],
        "A2": [60, 60]
    },
    "packages": [
        {
            "id": "P1",
            "warehouse": "W1",
            "destination": [30, 40]
        }
    ]
}
```

## How the Program Works

### 1. Load Input

The JSON input file is loaded and converted into Python dictionaries and lists.

### 2. Assign Packages

For every package, the distance between every delivery agent and the package's warehouse is calculated using Euclidean distance.

The package is assigned to the nearest agent.

The Euclidean distance formula is:

```text
distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)
```

### 3. Simulate Deliveries

For every assigned package, the agent travels:

```text
Current Agent Location
        ↓
Package Warehouse
        ↓
Customer Destination
```

The total distance for the package is:

```text
distance(current location, warehouse)
+
distance(warehouse, destination)
```

After completing a delivery, the agent's current location becomes that package's destination.

### 4. Calculate Efficiency

Agent efficiency is calculated as:

```text
efficiency =
total distance travelled / packages delivered
```

A lower distance per delivered package represents greater efficiency.

Agents who do not deliver any packages have an efficiency value of `null`.

### 5. Generate Report

The report contains:

* Number of packages delivered by each agent
* Total distance travelled by each agent
* Efficiency of each agent
* Most efficient agent

Example:

```json
{
    "A1": {
        "packages_delivered": 3,
        "total_distance": 245.67,
        "efficiency": 81.89
    },
    "A2": {
        "packages_delivered": 2,
        "total_distance": 190.25,
        "efficiency": 95.13
    },
    "best_agent": "A1"
}
```

## Running the Program

From the project root:

```bash
python main.py test_cases/test_case_1.json
```

The generated report is saved as:

```text
report.json
```

The same program can be used with every supplied test case:

```bash
python main.py test_cases/test_case_1.json
python main.py test_cases/test_case_2.json
python main.py test_cases/test_case_3.json
python main.py test_cases/test_case_4.json
python main.py test_cases/test_case_5.json
python main.py test_cases/test_case_6.json
python main.py test_cases/test_case_7.json
python main.py test_cases/test_case_8.json
python main.py test_cases/test_case_9.json
python main.py test_cases/test_case_10.json
```

The `reports/` directory contains the saved results for all ten test cases for convenient review.

## Assumptions

The following assumptions were made for scenarios that are not explicitly defined:

1. Package assignment is based on the agent's initial location and the package warehouse location.
2. Once packages are assigned, they remain assigned to that agent during the simulation.
3. Packages assigned to an agent are processed in their input/assignment order.
4. After delivering a package, the agent's current location becomes the package destination.
5. Every valid package has an existing warehouse.
6. Every package is expected to be delivered exactly once.
7. If multiple agents have exactly the same distance to a warehouse, the first agent encountered in the input order is selected.
8. Efficiency is measured as total distance travelled divided by the number of packages delivered.
9. Agents with zero deliveries have no meaningful efficiency and therefore receive `null`.
10. Distances are straight-line Euclidean distances between coordinates.

## Validation

The program validates:

* Required top-level JSON fields
* Warehouse structure
* Agent structure
* Package structure
* Warehouse references used by packages
* Total number of delivered packages

The program raises an error if the number of delivered packages does not match the number of input packages.

## Test Cases

The solution was tested against all 10 supplied test-case JSON files.

The corresponding generated reports are included in the `reports/` directory for easy review.

## Bonus Features

The project also includes two optional bonus features:

### 1. ASCII Route Visualization

The program displays a simple ASCII representation of each agent's delivery route, showing the agent's starting location, warehouses visited, and package destinations.

Example:

```text
Agent A1:
START [89, 16] -> W:W5 [34, 29] -> P:P1 DEST [12, 7]
```

This visualization is for readability only and does not modify the delivery simulation or distance calculations.

### 2. Top Performer CSV Export

The most efficient delivery agent is automatically exported to:

```text
top_performer.csv
```

The CSV contains:

* Agent ID
* Packages delivered
* Total distance
* Efficiency

This provides a convenient way to review the top-performing agent separately from the JSON report.


## Output

The main output file is:

```text
report.json
```

Each agent's result contains:

```text
packages_delivered
total_distance
efficiency
```

The report also contains:

```text
best_agent
```

## Author

M. Srinivas
