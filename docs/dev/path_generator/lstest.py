from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import json

# Load the saved model
loaded_model = load_model("docs/dev/path_generator/course_generator.h5")

# Load JSON data
with open("docs/dev/path_generator/course_data.json", "r") as file:
    data = json.load(file)

# Extract titles and modules
titles = [entry["title"] for entry in data]

# Tokenize titles
tokenizer = Tokenizer()
tokenizer.fit_on_texts(titles)

# Example: New course title for prediction
new_title = "Advanced concepts in python"

# Tokenize the new title
new_title_sequence = tokenizer.texts_to_sequences([new_title])

# Pad the sequence
max_sequence_length = 20  # Use the same max_sequence_length as used during training
padded_new_title_sequence = pad_sequences(
    new_title_sequence, maxlen=max_sequence_length
)

# Make predictions using the loaded model
predicted_modules = loaded_model.predict(padded_new_title_sequence)
