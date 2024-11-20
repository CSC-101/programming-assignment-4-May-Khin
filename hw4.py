import sys
import build_data
from data import CountyDemographics

# Load the full dataset
full_data = build_data.get_data()

# Define operations as functions

#Prints the total 2014 population of all counties
def population_total(counties: list[CountyDemographics]) -> None:
    total_population = sum(county.population['2014 Population'] for county in counties)
    print(f"2014 Population: {total_population}")

#Prints the total population for a specific field
def population_by_field(counties: list[CountyDemographics], field: str) -> None:
    value = sum(county.population['2014 Population'] * (county.get(field, 0) / 100) for county in counties)
    print(f"2014 {field} population: {value}")

#Prints the percentage of the total population
def percent_by_field(counties: list[CountyDemographics], field: str) -> None:
    total_population = sum(county.population['2014 Population'] for county in counties)
    field_population = sum(county.population['2014 Population'] * (county.get(field, 0) / 100) for county in counties)
    percent = (field_population / total_population) * 100 if total_population > 0 else 0
    print(f"2014 {field} percentage: {percent}%")

#Filters counties by state abbreviation
def filter_by_state(counties: list[CountyDemographics], state: str) -> list[CountyDemographics]:
    return [county for county in counties if county.state == state]

#Filters counties where the specified field value is greater than the given threshold
def filter_gt(counties: list[CountyDemographics], field: str, value: float) -> list[CountyDemographics]:
    return [county for county in counties if county.get(field, 0) > value]

#Filters counties where the specified field value is less than the given threshold
def filter_lt(counties: list[CountyDemographics], field: str, value: float) -> list[CountyDemographics]:
    return [county for county in counties if county.get(field, 0) < value]

#Prints detailed information for each county
def display(counties: list[CountyDemographics]) -> None:
    for county in counties:
        print(f"[{county.county}]")
        print(f"\tPOPULATION: {county.population['2014 Population']}")
        print("\tAGE")
        for age in county.age:
            print(f"\t\t{age}: {county.age[age]}%")
        print("\tEDUCATION")
        for edu in county.education:
            print(f"\t\t{edu}: {county.education[edu]}%")
        print("\tETHNICITIES")
        for eth in county.ethnicities:
            print(f"\t\t{eth}: {county.ethnicities[eth]}%")
        print("\tINCOME")
        for income in county.income:
            print(f"\t\t{income}: {county.income[income]}%")

# Operations map that associates each operation with a corresponding function
operations_map = {
    "population-total": population_total,
    "population:": population_by_field,
    "percent:": percent_by_field,
    "display": display,
    "filter-state": filter_by_state,
    "filter-gt": filter_gt,
    "filter-lt": filter_lt,
}


def run_operations(stats: list[CountyDemographics], line: str) -> None:
    operation = line.strip()
    if ":" in operation:
        op_type, field = operation.split(":")
        field = field.strip()
    else:
        op_type = operation
        field = ""

    if op_type in operations_map:
        if field:
            operations_map[op_type](stats, field)
        else:
            operations_map[op_type](stats)
    else:
        print(f"Error: Invalid operation '{op_type}'")

def filter_data(stats: list[CountyDemographics], line: str) -> list[CountyDemographics]:
    parts = line.strip().split(":")
    filter_type = parts[0]
    if filter_type == "filter-state":
        state = parts[1].strip()
        return filter_by_state(stats, state)
    elif filter_type == "filter-gt" or filter_type == "filter-lt":
        field = parts[1].strip()
        threshold = float(parts[2].strip())
        if filter_type == "filter-gt":
            return filter_gt(stats, field, threshold)
        elif filter_type == "filter-lt":
            return filter_lt(stats, field, threshold)
    else:
        raise ValueError("Invalid filter type.")

def main() -> None:
    try:
        # Read the input file
        file = "inputs/" + sys.argv[1]
        with open(file, 'r') as infile:
            print(f"{len(full_data)} records loaded.")
            stats = full_data  # Initialize stats with the full dataset

            # Process each line in the input file
            for count, line in enumerate(infile, 1):
                line = line.strip()
                try:
                    # If the line is a filter instruction
                    if "filter" in line:
                        stats = filter_data(stats, line)
                    else:
                        # Else, perform the operation
                        run_operations(stats, line)
                except Exception as e:
                    print(f"An error occurred at line {count}: {line}. Error: {e}")
    except FileNotFoundError:
        print("ERROR: File not found.")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    main()
