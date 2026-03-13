import csv

def visualize_csv_table(file_path):
    # Read CSV file
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Find the maximum width of each column
    col_widths = []
    num_cols = len(data[0])

    for col in range(num_cols):
        max_width = max(len(row[col]) for row in data)
        col_widths.append(max_width)

    # Function to print horizontal border
    def print_border():
        print("+", end="")
        for width in col_widths:
            print("-" * (width + 2) + "+", end="")
        print()

    # Print table
    print_border()
    for i, row in enumerate(data):
        print("|", end="")
        for j, cell in enumerate(row):
            print(" " + cell.ljust(col_widths[j]) + " |", end="")
        print()
        print_border()


# Example usage
visualize_csv_table("data.csv")