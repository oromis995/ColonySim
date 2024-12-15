import json

# Load the root and suffix files
with open('Data/roots.json', 'r') as roots_file:
    roots_data = json.load(roots_file)

with open('Data/suffixes.json', 'r') as suffixes_file:
    suffixes_data = json.load(suffixes_file)

# Extract roots and suffixes
roots = []
for category in roots_data.values():
    for root_entry in category:
        root = root_entry['Root'].rstrip('-')  # Remove trailing dashes from roots
        roots.append(root)

suffixes = suffixes_data['suffixes']

# Function to handle consonant clashes and remove suffix dashes
def clean_suffix(root, suffix):
    suffix = suffix.lstrip('-')  # Remove leading dashes from suffix
    if root[-1] == suffix[0] and root[-1].isalpha() and root[-1].lower() not in 'aeiou':
        root = root[:-1] + "'"  # Remove the last consonant from the root
    return root + suffix

# Generate names
masculine_names = []
feminine_names = []
gender_neutral_names = []

for root in roots:
    for suffix_entry in suffixes:
        for gender, suffix in suffix_entry.items():
            name = clean_suffix(root, suffix)
            if gender == "Masculine":
                masculine_names.append(name)
            elif gender == "Feminine":
                feminine_names.append(name)
            elif gender == "GenderNeutral":
                gender_neutral_names.append(name)

# Save the results to files
with open('Data/assembled_m_names.txt', 'w') as masc_file:
    masc_file.write('\n'.join(masculine_names))

with open('Data/assembled_f_names.txt', 'w') as fem_file:
    fem_file.write('\n'.join(feminine_names))

with open('Data/assembled_n_names.txt', 'w') as neutral_file:
    neutral_file.write('\n'.join(gender_neutral_names))

print("Name generation completed. Output saved to files.")
