from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample course data
course_data = [
    {
        "title": "Introduction to Python Programming",
        "description": "Learn the basics of Python programming language.",
    },
    {
        "title": "Machine Learning Fundamentals",
        "description": "An introduction to machine learning algorithms and techniques.",
    },
    {
        "title": "Computer Vision with OpenCV",
        "description": "Explore computer vision concepts using OpenCV library.",
    },
    {
        "title": "Natural Language Processing Basics",
        "description": "An overview of natural language processing techniques.",
    },
    {
        "title": "Data Science for Beginners",
        "description": "Introduction to data science concepts and tools.",
    },
    {
        "title": "Artificial Intelligence Essentials",
        "description": "Learn the fundamentals of artificial intelligence.",
    },
]

# Extract course titles and descriptions
course_titles = [course["title"] for course in course_data]
course_descriptions = [course["description"] for course in course_data]

# Combine course titles and descriptions for TF-IDF vectorization
combined_texts = [
    title + " " + description
    for title, description in zip(course_titles, course_descriptions)
]

# User query
user_query = "I want to learn about machine learning"

# TF-IDF vectorization
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(combined_texts)

# Labels (course titles)
y = course_titles

# Train a logistic regression classifier
classifier = LogisticRegression()
classifier.fit(X, y)

# Transform user query using the same TF-IDF vectorizer
user_query_vectorized = tfidf_vectorizer.transform([user_query])

# Predict course path based on user query
predicted_course = classifier.predict(user_query_vectorized)[0]
print("Recommended Course:", predicted_course)
