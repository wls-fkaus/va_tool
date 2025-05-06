# Ash Cowne and Aiden Canady
# 4/24/2025
# Creating the second part of the code to put the new datalist into groups and sorting them.

# Its program name is the keys while the student IDs are the values.

import pandas as pd
import csv
# Convers the csv into a python script/dict
from collections import defaultdict, Counter


rows = []
#df = pd.read_csv("student_programs.csv")
with open('clean_data.csv', newline='') as f:

#print(df)
    reader = csv.DictReader(f)

    for r in reader:
        rows.append((int(r['ID']), r['PROGRAMS']))
    #print(rows)

dict_stu_pro = defaultdict(set)
for student, prog in rows:
    dict_stu_pro[student].add(prog)

combinations = defaultdict(list)
for student, prog_set in dict_stu_pro.items():
    key = tuple(sorted(prog_set))
    combinations[key].append(student)

for combo, students in combinations.items():
    print(f"{combo!r} {students}")

# Sorted the students into dictonarys.
# Now need to sort by A, D, C and give the numbe of the most common combination.

#def sort(Student_ID,Program_ID):
    #print(d)


    4/29/2025


# Helper to classify combinations by program type (A, C, D)
def classify_combo(combo):
    has_A = any(p.startswith('A') for p in combo)
    has_C = any(p.startswith('C') for p in combo)
    has_D = any(p.startswith('D') for p in combo)
    return has_A, has_C, has_D

# Counters for each of A, C, and D
a_combos = []
c_combos = []
d_combos = []

# Classify combinations into A, C, or D groups
for combo, students in combinations.items():
    has_A, has_C, has_D = classify_combo(combo)
    n_students = len(students)

    if has_A:
        a_combos.append((combo, n_students))
    if has_C:
        c_combos.append((combo, n_students))
    if has_D:
        d_combos.append((combo, n_students))

# Find most common combinations for each group
def get_most_common(combos):
    combo_counter = Counter(dict(combos))
    return combo_counter.most_common(1)

# Output
def print_group_summary(group_name, combos):
    total_students = sum(n for combo, n in combos)
    most_common_combo, count = get_most_common(combos)[0]
    print(f"\nDataSet {group_name}:")
    print(f"Total number of students: {total_students}")
    print(f"Most common combination: {most_common_combo} with {count} students")

# Print results for each group
print_group_summary("A", a_combos)
print_group_summary("C", c_combos)
print_group_summary("D", d_combos)