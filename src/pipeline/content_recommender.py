"""
Module content recommender system 
arguments: module name
output: url dict upon invoking get_url
"""

from tensorflow.keras.models import load_model
import constants as C
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import random

model_path = f"{C.MODEL_SAVE_PATH}recommender_model.h5"
model = load_model(model_path)


class ContentRecommender:
    def __init__(self, module):
        self.module = module
        self.url_dict = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"An exception of type {exc_type} occurred")

    def forward(self) -> str:
        df = pd.read_csv(f"{C.DATA_DIR}/recommender/info.csv")
        label_encoder = LabelEncoder()
        label_encoder.fit(df["topic"])
        encoded_topic = label_encoder.transform([self.module])[0]
        input_features = pd.DataFrame(
            {
                "views": [0],
                "likes": [0],
            }
        )
        scaler = StandardScaler()
        input_features_scaled = scaler.fit_transform(input_features)
        recommended_videos = model.predict(input_features_scaled)
        filtered_df = df[df["topic"] == self.module]
        pos = random.randint(0, 1)
        recommended_videos = filtered_df.iloc[pos]

        self.url_dict[self.module] = recommended_videos["url"]

    def get_urls(self) -> dict:
        return self.url_dict


# Example test
if __name__ == "__main__":
    video = ContentRecommender("what is python")
    video.forward()
    video_url = video.get_urls()
    print(video_url)
