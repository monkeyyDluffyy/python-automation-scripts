# Instance size hierarchy
sizes = ["nano","micro","small","medium","large","xlarge","2xlarge",
         "4xlarge","8xlarge","16xlarge","32xlarge"]

def print_table(data):
    # Find column widths
    col_widths = []
    cols = len(data[0])

    for i in range(cols):
        width = max(len(row[i]) for row in data)
        col_widths.append(width)

    # Print border
    def border():
        print("+", end="")
        for w in col_widths:
            print("-"*(w+2) + "+", end="")
        print()

    border()
    for row in data:
        print("|", end="")
        for i, cell in enumerate(row):
            print(" " + cell.ljust(col_widths[i]) + " |", end="")
        print()
        border()


# --- INPUT ---
current_instance = input("Current EC2 instance (example t2.large): ")
cpu = int(input("CPU Utilization (%): "))

# Split instance type and size
instance_type, size = current_instance.split(".")

index = sizes.index(size)

# --- LOGIC ---
if cpu < 20:
    status = "Underutilized"
    if index > 0:
        new_size = sizes[index-1]
    else:
        new_size = size
    recommendation = instance_type + "." + new_size

elif cpu > 80:
    status = "Overutilized"
    if index < len(sizes)-1:
        new_size = sizes[index+1]
    else:
        new_size = size
    recommendation = instance_type + "." + new_size

else:
    status = "Optimized"
    recommendation = "Latest generation equivalent (e.g., t3." + size + ")"

# --- TABLE DATA ---
table = [
    ["Current Instance", current_instance],
    ["CPU Utilization", str(cpu) + "%"],
    ["Status", status],
    ["Recommended Instance", recommendation]
]

# Print result table
print_table(table)