from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Read keywords from file
keywords_file = "docs/dev/data/keywords.txt"
with open(keywords_file, "r") as file:
    keywords_to_identify = file.read().splitlines()

# Prompt user to enter a query
user_query = input("Enter your query: ")

# Extract features from user query
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform([user_query])

# List to store keyword-presence pairs
keyword_presence = []

# Loop over each keyword and check its presence in the user query
for keyword in keywords_to_identify:
    if keyword in user_query.lower():
        keyword_presence.append((keyword, "Present"))
    else:
        keyword_presence.append((keyword, "Absent"))

# Print keyword-presence pairs
print("Keyword Presence:")
for keyword, presence in keyword_presence:
    (
        print(f"Keyword: {keyword}, Presence: {presence}")
        if presence == 1
        else print("not present")
    )
