"""
FINAL NLP SCRIPT
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

# Read keywords from file
keywords_file = "docs/dev/data/keywords.txt"
with open(keywords_file, "r") as file:
    keywords_to_identify = file.read().splitlines()

# Prompt user to enter a query


with open("docs/dev/data/valid.txt", "r") as file:
    positive_samples = file.read().splitlines()

# Extract features from user query and positive samples
tfidf_vectorizer = TfidfVectorizer()
X_positive = tfidf_vectorizer.fit_transform(positive_samples)
y_positive = np.ones(len(positive_samples))  # Label 1 for positive samples

# Negative samples (randomly generated)
with open("docs/dev/data/invalid.txt", "r") as file:
    negative_samples = file.read().splitlines()

# Extract features from negative samples
X_negative = tfidf_vectorizer.transform(negative_samples)
y_negative = np.zeros(len(negative_samples))  # Label 0 for negative samples

# Combine positive and negative samples
X_train = np.vstack((X_positive.toarray(), X_negative.toarray()))
y_train = np.concatenate((y_positive, y_negative))

# Train a logistic regression classifier
classifier = LogisticRegression()
classifier.fit(X_train, y_train)

# Test the model on the user query
new_query = input("Enter a query: ")

# Transform new query using the same TF-IDF vectorizer
X_new = tfidf_vectorizer.transform([new_query])

# Predict presence of keywords in new query
prediction = classifier.predict(X_new)

# Print prediction
found: bool = False

for keyword in keywords_to_identify:
    if keyword.lower() in new_query.lower():
        print("fetching relevant results for: ", keyword)
        found = True
        break
if not found:
    print("invalid query")
