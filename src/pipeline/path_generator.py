"""
Learning path generator pipeline 
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import constants as C
import csv
import json


class LearningPathGenerator:
    def __init__(self, keyword, difficulty="beginner"):
        self.keyword = keyword
        self.difficulty = difficulty
        self.nlp_data_path = f"{C.DATA_DIR}/nlp_module"
        self.gen_data_path = f"{C.DATA_DIR}/path_generator"
        self.course_title = ""
        self.extract_keyword()
        self.modules = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"An exception of type {exc_type} occurred")

    # NLP module

    def extract_keyword(self):
        """
        takes query from self.keyword and checks if it is valid. sets self.keyword to the keyword. exits if invalid raising ValueError
        """
        # Read keywords from file
        keywords_file = f"{self.nlp_data_path}/keywords.txt"
        with open(keywords_file, "r") as file:
            keywords_to_identify = file.read().splitlines()
        with open(f"{self.nlp_data_path}/valid.txt", "r") as file:
            positive_samples = file.read().splitlines()
        tfidf_vectorizer = TfidfVectorizer()
        # Extract features from positive samples
        X_positive = tfidf_vectorizer.fit_transform(positive_samples)
        y_positive = np.ones(len(positive_samples))

        with open(f"{self.nlp_data_path}/invalid.txt", "r") as file:
            negative_samples = file.read().splitlines()

        # Extract features from negative samples
        X_negative = tfidf_vectorizer.transform(negative_samples)
        y_negative = np.zeros(len(negative_samples))
        # Combine positive and negative samples
        X_train = np.vstack((X_positive.toarray(), X_negative.toarray()))
        y_train = np.concatenate((y_positive, y_negative))

        classifier = LogisticRegression()
        classifier.fit(X_train, y_train)

        X_new = tfidf_vectorizer.transform([self.keyword])
        prediction = classifier.predict(X_new)
        found: bool = False

        for keyword in keywords_to_identify:
            if keyword.lower() in self.keyword.lower():
                self.keyword = keyword.lower()
                found = True
                break
        if not found:
            self.keyword = "invalid query"
            raise ValueError(self.keyword)

        return self.keyword

    def generate_path(self):
        """
        generates learning path for the keyword and difficulty level
        """
        self.course_title = self.title_from_keyword(
            self.keyword, f"{self.gen_data_path}/title.csv"
        )
        with open(f"{self.gen_data_path}/course_data.json", "r") as file:
            data = json.load(file)

        self.modules = self.get_modules(data)
        if self.modules is None:
            raise ValueError("course not available")

    # Helper function
    def title_from_keyword(self, keyword, keyword_title_file):
        title = ""

        with open(keyword_title_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:

                if row["keyword"] == keyword and row["difficulty"] == self.difficulty:

                    title = row["course_title "]
        return title

    # Helper function
    def get_modules(self, data):
        for entry in data:
            if entry["title"] == self.course_title:
                return entry["modules"]
        return None


# Test
if __name__ == "__main__":
    myg = LearningPathGenerator("I want to learn javascript")
    print(myg.extract_keyword())
    myg.generate_path()
    print(myg.course_title)
    print(myg.modules)
    print(type(myg.modules))
