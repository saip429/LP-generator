"""
TF-IDF VECTORIZER
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

nltk.download("punkt")
from nltk.corpus import stopwords

# Download NLTK stopwords
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Read raw text data from file
file_path = "docs/dev/data/raw_data.txt"
with open(file_path, "r", encoding="utf-8") as file:
    raw_text = file.read()

# Tokenize the raw text into words
words = nltk.word_tokenize(raw_text)

# Remove stop words, punctuation, and special characters
filtered_words = [
    word.lower() for word in words if word.isalnum() and word.lower() not in stop_words
]

# Join filtered words back into text
filtered_text = " ".join(filtered_words)

# TF-IDF vectorization
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform([filtered_text])

# Get feature names (keywords)
keywords = tfidf_vectorizer.get_feature_names_out()

# Save extracted keywords to a file
keywords_file_path = "docs/dev/data/extracted_keywords.txt"
with open(keywords_file_path, "w", encoding="utf-8") as keywords_file:
    keywords_file.write("\n".join(keywords))

print("Keywords have been extracted and saved to:", keywords_file_path)
