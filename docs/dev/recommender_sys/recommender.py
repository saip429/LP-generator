import pandas as pd
import numpy as np
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
import constants as c

model_save_path = f"{c.MODEL_SAVE_PATH}recommender_model.h5"
# Load the data from the CSV file
data = pd.read_csv("docs/dev/recommender_sys/info.csv")

# Preprocess the data
X = data[["views", "likes"]].values
y = data["topic"].values

# One-hot encode the target variable
topics = np.unique(y)
num_topics = len(topics)
topic_to_index = {topic: i for i, topic in enumerate(topics)}
y_encoded = np.array([topic_to_index[topic] for topic in y])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Neural network model
model = Sequential(
    [
        Dense(64, activation="relu", input_shape=(X_train_scaled.shape[1],)),
        Dropout(0.5),
        Dense(32, activation="relu"),
        Dropout(0.5),
        Dense(
            num_topics, activation="softmax"
        ),  # Use softmax activation for multi-class classification
    ]
)

# Compile the model
model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

# Train the model
model.fit(
    X_train_scaled,
    y_train,
    epochs=10,
    batch_size=32,
    validation_data=(X_test_scaled, y_test),
)
model.save(model_save_path)


# Function to recommend a video based on the desired topic, views, and likes
def recommend_video(topic, min_views, min_likes):
    # Predict the probabilities for each topic
    topic_probabilities = model.predict(np.array([[min_views, min_likes]]))

    # Get the index of the predicted topic
    predicted_topic_index = np.argmax(topic_probabilities)

    # Map the index back to the original topic
    predicted_topic = topics[predicted_topic_index]

    # Filter videos based on the predicted topic, views, and likes
    filtered_videos = data[
        (data["topic"] == predicted_topic)
        & (data["views"] >= min_views)
        & (data["likes"] >= min_likes)
    ]

    # Select a random video from the filtered list (if any)
    if not filtered_videos.empty:
        recommended_video = filtered_videos.sample()["url"].values[0]
        print("Recommended video:")
        print(recommended_video)
        print(type(recommended_video))
    else:
        print("No videos found matching the criteria.")


# Example usage
desired_topic = "Operators in C"
desired_views = 1000000
desired_likes = 50000

recommend_video(desired_topic, desired_views, desired_likes)
