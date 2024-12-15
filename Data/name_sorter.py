


def remove_duplicates_preserve_order(lines):
    """
    Remove duplicates from the list while preserving the original order.
    """
    seen = set()
    return [line for line in lines if not (line in seen or seen.add(line))]


def categorize_name(name):
    """
    Categorize a name based on suffix patterns.
    """
    female_suffixes = {"a","ess", "anne", "elle", "wyn", "eth", "in", "wen", "ynn", "enne", "ix", "ynne", "ryn"}
    male_suffixes = {"o", "an","or", "on", "el", "onis", "us", "ic", "os", "or", "ar", "anth", "orn"}
    gender_neutral_suffixes = {"um","en", "ann","eth", "ir", "ann", "drin", "ath", "rin", "il", "ith", "is", "ell", "lyn", "al", "as"}

    if any(name.endswith(suffix) for suffix in female_suffixes):
        return "Female"
    elif any(name.endswith(suffix) for suffix in male_suffixes):
        return "Male"
    elif any(name.endswith(suffix) for suffix in gender_neutral_suffixes):
        return "Gender-Neutral"
    else:
        return "Uncategorized"


def process_names(input_file):
    """
    Process names from input file, categorize, sort, and write to respective files.
    """
    # File paths for output
    file_paths = {
        "Male": "./Data/sorted_m_names.txt",
        "Female": "./Data/sorted_f_names.txt",
        "Gender-Neutral": "./Data/sorted_n_names.txt",
        "Uncategorized": "./Data/uncategorized.txt"
    }

    # Initialize categories
    categories = {key: [] for key in file_paths.keys()}

    # Read names, remove duplicates, and strip whitespace
    with open(input_file, 'r') as file:
        names = remove_duplicates_preserve_order([line.strip() for line in file])

    # Categorize names
    for name in names:
        category = categorize_name(name)
        categories[category].append(name)

    # Write sorted and categorized names to respective files
    for category, file_path in file_paths.items():
        with open(file_path, 'w') as file:
            file.write("\n".join(sorted(categories[category])))

    print("Names have been categorized, sorted, and written to respective files.")


if __name__ == "__main__":
    input_file_path = "./Data/input.txt"
    process_names(input_file_path)
