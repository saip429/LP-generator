import json
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import save_model, load_model

# Load JSON data
with open("docs/dev/path_generator/course_data.json", "r") as file:
    data = json.load(file)

# Extract titles and modules
titles = [entry["title"] for entry in data]
modules = [entry["modules"] for entry in data]

# Tokenize titles
tokenizer = Tokenizer()
tokenizer.fit_on_texts(titles)
sequences = tokenizer.texts_to_sequences(titles)

# Pad sequences
max_sequence_length = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)

# Convert modules to one-hot encoding
num_classes = len(set(module for sublist in modules for module in sublist))
module_indices = {
    module: i
    for i, module in enumerate(
        sorted(set(module for sublist in modules for module in sublist))
    )
}
one_hot_modules = np.zeros((len(modules), num_classes), dtype=np.float32)
for i, module_list in enumerate(modules):
    for module in module_list:
        one_hot_modules[i, module_indices[module]] = 1

# Define and compile the model

# Define and compile the model
model = Sequential(
    [
        Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64),
        LSTM(64),
        Dense(num_classes, activation="sigmoid"),
    ]
)

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the model
model.fit(
    padded_sequences, one_hot_modules, epochs=10, batch_size=16, validation_split=0.2
)

save_model(model, "docs/dev/path_generator/course_generator.h5")

# Load the saved model
loaded_model = load_model("docs/dev/path_generator/course_generator.h5")

new_title = "Introduction to Python programming"
new_title_sequence = tokenizer.texts_to_sequences([new_title])
padded_new_title_sequence = pad_sequences(
    new_title_sequence, maxlen=max_sequence_length
)
predicted_modules = loaded_model.predict(padded_new_title_sequence)
predicted_modules = [
    module
    for module, prob in zip(module_indices.keys(), predicted_modules[0])
    if prob > 0.5
]

print("Predicted Modules:", predicted_modules)
