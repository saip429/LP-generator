# List of keywords
with open("docs/dev/data/keywords.txt", "r") as f:
    keywords = f.readlines()


# User input
user_input = input(
    "Enter a sentence: "
).lower()  # Convert input to lowercase for case-insensitive matching

# Extract keywords from user input
extracted_keywords = [keyword for keyword in keywords if keyword in user_input]

# Print extracted keywords
if extracted_keywords:
    print("Keywords found:", extracted_keywords)
else:
    print("No keywords found in the input.")
