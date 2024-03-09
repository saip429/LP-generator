import csv
import json


def title_from_keyword(keyword, difficulty, keyword_title_file):
    title = ""

    with open(keyword_title_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:

            if row["keyword"] == keyword and row["difficulty"] == difficulty:

                title = row["course_title "]
    return title


with open("docs/dev/path_generator/course_data.json", "r") as file:
    data = json.load(file)


def get_modules(topic):
    for entry in data:
        if entry["title"] == topic:
            return entry["modules"]
    return None


# Define the dataset file path
dataset_file = "docs/dev/path_generator/course_data.json"

# Specify the desired course title
course_title = title_from_keyword(
    "python", "advanced", "docs/dev/path_generator/title.csv"
)
print(course_title)
# Generate the course modules
modules = get_modules(course_title)
if modules:
    print("Modules for Introduction to Python Programming:")
    for module in modules:
        print(module)
else:
    print("Topic not found.")
