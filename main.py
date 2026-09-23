import json
import math
import sys


# ============================================================
# TASK 1: LOAD JSON DATA
# ============================================================

def load_data(file_path):
    """
    Read and parse the JSON input file.

    The official assignment format contains:
        - warehouses: dictionary of warehouse IDs and locations
        - agents: dictionary of agent IDs and locations
        - packages: list of package dictionaries

    Args:
        file_path (str): Path to the JSON input file.

    Returns:
        dict: Parsed JSON data.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


# ============================================================
# TASK 2: DISTANCE CALCULATION
# ============================================================

def calculate_distance(point1, point2):
    """
    Calculate Euclidean distance between two points.

    Formula:
        distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)

    Args:
        point1 (list): [x, y]
        point2 (list): [x, y]

    Returns:
        float: Euclidean distance.
    """

    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


# ============================================================
# TASK 2: FIND NEAREST AGENT
# ============================================================

def find_nearest_agent(agents, warehouse_location):
    """
    Find the agent closest to a warehouse.

    The assignment specifically says that packages must be
    assigned using the Euclidean distance from the agent's
    location to the package's warehouse.

    Args:
        agents (dict):
            {
                "A1": [x, y],
                "A2": [x, y]
            }

        warehouse_location (list):
            [x, y]

    Returns:
        tuple:
            (nearest_agent_id, shortest_distance)
    """

    shortest_distance = float("inf")
    nearest_agent_id = None

    # Check every agent.
    for agent_id, agent_location in agents.items():

        distance = calculate_distance(
            agent_location,
            warehouse_location
        )

        # Update the nearest agent if this distance
        # is smaller than the previous shortest distance.
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_agent_id = agent_id

    return nearest_agent_id, shortest_distance


# ============================================================
# TASK 2: ASSIGN PACKAGES TO AGENTS
# ============================================================

def assign_packages_to_agents(packages, warehouses, agents):
    """
    Assign every package to the nearest delivery agent.

    Important assumption:
    The assignment is calculated using the agents'
    initial locations, exactly as specified in Task 2.

    Agent locations are updated only during the simulation.

    Args:
        packages (list): List of package dictionaries.
        warehouses (dict): Warehouse ID -> [x, y].
        agents (dict): Agent ID -> [x, y].

    Returns:
        dict:
            {
                "A1": ["P1", "P4"],
                "A2": ["P2"],
                ...
            }
    """

    # Create an empty package list for every agent.
    assignments = {
        agent_id: []
        for agent_id in agents
    }

    # Process every package.
    for package in packages:

        package_id = package["id"]
        warehouse_id = package["warehouse"]

        # Check whether the referenced warehouse exists.
        if warehouse_id not in warehouses:
            raise ValueError(
                f"Warehouse '{warehouse_id}' "
                f"not found for package '{package_id}'."
            )

        warehouse_location = warehouses[warehouse_id]

        # Find the nearest agent using the agent's
        # initial location.
        nearest_agent, distance = find_nearest_agent(
            agents,
            warehouse_location
        )

        # Assign the package.
        assignments[nearest_agent].append(package_id)

        print(
            f"Package {package_id} -> "
            f"Warehouse {warehouse_id} -> "
            f"Agent {nearest_agent} "
            f"(distance: {distance:.2f})"
        )

    return assignments


# ============================================================
# TASK 3: SIMULATE DELIVERIES FOR ONE AGENT
# ============================================================

def simulate_agent_deliveries(
    agent_id,
    assigned_packages,
    package_lookup,
    warehouses,
    agents
):
    """
    Simulate deliveries for one agent.

    For every package, the agent travels:

        Current Agent Location
                |
                v
            Warehouse
                |
                v
           Destination

    After a package is delivered, the agent's current
    location becomes that package's destination.

    This means the next package starts from the previous
    delivery destination.

    Args:
        agent_id (str): Delivery agent ID.
        assigned_packages (list): Package IDs assigned to agent.
        package_lookup (dict): Package ID -> package data.
        warehouses (dict): Warehouse ID -> [x, y].
        agents (dict): Agent ID -> [x, y].

    Returns:
        dict: Delivery statistics.
    """

    # Agent starts at their original location.
    current_location = agents[agent_id]

    total_distance = 0.0
    packages_delivered = 0

    # Process packages in their assignment order.
    for package_id in assigned_packages:

        package = package_lookup[package_id]

        warehouse_id = package["warehouse"]
        destination = package["destination"]

        warehouse_location = warehouses[warehouse_id]

        # ----------------------------------------------------
        # Distance 1:
        # Current agent location -> warehouse
        # ----------------------------------------------------

        distance_to_warehouse = calculate_distance(
            current_location,
            warehouse_location
        )

        # ----------------------------------------------------
        # Distance 2:
        # Warehouse -> customer destination
        # ----------------------------------------------------

        distance_to_destination = calculate_distance(
            warehouse_location,
            destination
        )

        # Total distance for this package.
        package_distance = (
            distance_to_warehouse +
            distance_to_destination
        )

        total_distance += package_distance
        packages_delivered += 1

        # After delivery, the agent is located at
        # the customer's destination.
        current_location = destination

        print(
            f"Agent {agent_id} delivered {package_id}: "
            f"{package_distance:.2f} distance units"
        )

    return {
        "packages_delivered": packages_delivered,
        "total_distance": total_distance,
        "final_location": current_location
    }


# ============================================================
# TASK 3: SIMULATE ALL AGENTS
# ============================================================

def simulate_deliveries(
    assignments,
    packages,
    warehouses,
    agents
):
    """
    Simulate deliveries for all agents.

    Args:
        assignments (dict): Agent ID -> package IDs.
        packages (list): All package data.
        warehouses (dict): Warehouse data.
        agents (dict): Agent data.

    Returns:
        dict: Delivery results for every agent.
    """

    # Create a fast lookup dictionary:
    #
    # {
    #     "P1": {...},
    #     "P2": {...}
    # }
    package_lookup = {
        package["id"]: package
        for package in packages
    }

    delivery_results = {}

    # Simulate each agent independently.
    for agent_id in agents:

        assigned_packages = assignments[agent_id]

        result = simulate_agent_deliveries(
            agent_id,
            assigned_packages,
            package_lookup,
            warehouses,
            agents
        )

        delivery_results[agent_id] = result

    return delivery_results


# ============================================================
# TASK 4: GENERATE REPORT
# ============================================================

def generate_report(delivery_results):
    """
    Generate the final FastBox report.

    Efficiency is defined as:

        total_distance / packages_delivered

    Therefore, a lower distance per package means
    greater delivery efficiency.

    Args:
        delivery_results (dict):
            Results for every agent.

    Returns:
        dict: Final report.
    """

    report = {}

    best_agent_id = None
    best_efficiency = float("inf")

    for agent_id, result in delivery_results.items():

        packages_delivered = result["packages_delivered"]
        total_distance = result["total_distance"]

        # Prevent division by zero for agents who
        # did not deliver any packages.
        if packages_delivered > 0:

            efficiency = (
                total_distance /
                packages_delivered
            )

            # Lower distance per package is better.
            if efficiency < best_efficiency:
                best_efficiency = efficiency
                best_agent_id = agent_id

        else:
            efficiency = None

        report[agent_id] = {
            "packages_delivered": packages_delivered,
            "total_distance": round(total_distance, 2),
            "efficiency": (
                round(efficiency, 2)
                if efficiency is not None
                else None
            )
        }

    # Add the most efficient agent.
    report["best_agent"] = best_agent_id

    return report


# ============================================================
# TASK 5: SAVE REPORT
# ============================================================

def save_report(report, output_file):
    """
    Save the final report to a JSON file.

    Args:
        report (dict): Final report.
        output_file (str): Output JSON file path.
    """

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump(
            report,
            file,
            indent=4
        )

    print()
    print(f"Report saved successfully to: {output_file}")


# ============================================================
# VALIDATE INPUT DATA
# ============================================================

def validate_data(data):
    """
    Validate the basic structure of the input JSON.

    This helps catch incorrect or incomplete input files
    before the simulation starts.
    """

    required_keys = [
        "warehouses",
        "agents",
        "packages"
    ]

    for key in required_keys:

        if key not in data:
            raise ValueError(
                f"Input JSON is missing required field: '{key}'"
            )

    if not isinstance(data["warehouses"], dict):
        raise ValueError(
            "'warehouses' must be a dictionary."
        )

    if not isinstance(data["agents"], dict):
        raise ValueError(
            "'agents' must be a dictionary."
        )

    if not isinstance(data["packages"], list):
        raise ValueError(
            "'packages' must be a list."
        )

    # Validate package references.
    for package in data["packages"]:

        if "id" not in package:
            raise ValueError(
                "Every package must contain an 'id'."
            )

        if "warehouse" not in package:
            raise ValueError(
                f"Package '{package['id']}' "
                f"is missing the 'warehouse' field."
            )

        if "destination" not in package:
            raise ValueError(
                f"Package '{package['id']}' "
                f"is missing the 'destination' field."
            )

        warehouse_id = package["warehouse"]

        if warehouse_id not in data["warehouses"]:
            raise ValueError(
                f"Package '{package['id']}' references "
                f"unknown warehouse '{warehouse_id}'."
            )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """
    Main function for the FastBox delivery simulator.

    Usage:

        python main.py

    or:

        python main.py path/to/test_case.json

    If no input path is provided, the program uses:

        data/data.json
    """

    # --------------------------------------------------------
    # Determine input file.
    # --------------------------------------------------------

    if len(sys.argv) > 1:

        input_file = sys.argv[1]

    else:

        input_file = "data/data.json"

    # Output report file.
    output_file = "report.json"

    print("=" * 60)
    print("FASTBOX DELIVERY SIMULATOR")
    print("=" * 60)

    print()
    print(f"Input file: {input_file}")

    # --------------------------------------------------------
    # TASK 1: Load JSON
    # --------------------------------------------------------

    data = load_data(input_file)

    # Validate input.
    validate_data(data)

    print("Input data loaded successfully.")

    # --------------------------------------------------------
    # Display input summary.
    # --------------------------------------------------------

    print()
    print("Input Summary")
    print("-" * 60)

    print(
        "Warehouses:",
        len(data["warehouses"])
    )

    print(
        "Agents:",
        len(data["agents"])
    )

    print(
        "Packages:",
        len(data["packages"])
    )

    # --------------------------------------------------------
    # TASK 2: Assign packages.
    # --------------------------------------------------------

    print()
    print("PACKAGE ASSIGNMENTS")
    print("-" * 60)

    assignments = assign_packages_to_agents(
        data["packages"],
        data["warehouses"],
        data["agents"]
    )

    print()
    print("Final Assignments")
    print("-" * 60)

    for agent_id, package_ids in assignments.items():

        print(
            f"{agent_id}: {package_ids}"
        )

    # --------------------------------------------------------
    # TASK 3: Simulate deliveries.
    # --------------------------------------------------------

    print()
    print("DELIVERY SIMULATION")
    print("-" * 60)

    delivery_results = simulate_deliveries(
        assignments,
        data["packages"],
        data["warehouses"],
        data["agents"]
    )

    # --------------------------------------------------------
    # Check that every package was delivered.
    # --------------------------------------------------------

    total_delivered = sum(
        result["packages_delivered"]
        for result in delivery_results.values()
    )

    total_packages = len(data["packages"])

    print()
    print("Delivery Validation")
    print("-" * 60)

    print(
        f"Total packages: {total_packages}"
    )

    print(
        f"Packages delivered: {total_delivered}"
    )

    if total_delivered != total_packages:
        raise RuntimeError(
            "Not all packages were delivered."
        )

    print("All packages were delivered successfully.")

    # --------------------------------------------------------
    # TASK 4: Generate report.
    # --------------------------------------------------------

    report = generate_report(
        delivery_results
    )

    print()
    print("FINAL REPORT")
    print("-" * 60)

    for agent_id, result in report.items():

        # best_agent is a single string,
        # so don't treat it like an agent result.
        if agent_id == "best_agent":
            continue

        print(
            f"{agent_id}: "
            f"packages_delivered="
            f"{result['packages_delivered']}, "
            f"total_distance="
            f"{result['total_distance']}, "
            f"efficiency="
            f"{result['efficiency']}"
        )

    print()
    print(
        f"Most efficient agent: "
        f"{report['best_agent']}"
    )

    # --------------------------------------------------------
    # TASK 5: Save report.
    # --------------------------------------------------------

    save_report(
        report,
        output_file
    )

    print()
    print("=" * 60)
    print("SIMULATION COMPLETED SUCCESSFULLY")
    print("=" * 60)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()