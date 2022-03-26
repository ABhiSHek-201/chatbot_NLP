import nltk
nltk.download("punkt")
nltk.download("wordnet")
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random

words = []
classes = []
documents = []
ignore_words = ["?", "!"]
data_file = open("job_intents.json", encoding="utf-8").read()
intents = json.loads(data_file)

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        # tokenize
        wt = nltk.word_tokenize(pattern)
        words.extend(wt)
        
        # add all tokenized words with tags in a tuple
        documents.append((wt, intent["tag"]))

        if intent["tag"] not in classes:
            classes.append(intent["tag"])
        
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

print("documents=>",len(documents))
print("classes=>",len(classes))
print("words=>",len(words))

pickle.dump(classes, open("classes.pkl", "wb"))
pickle.dump(words, open("words.pkl", "wb"))

# Training on data 
training = []
output_empty = [0] * len(classes)
print(documents)
print()
for doc in documents:
    bag = []
    print(doc)
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append((bag, output_row))


# print("traniing",training)
random.shuffle(training)
# print("traniing",training)
training = np.array(training)
# print("traniing",training)

train_x = list(training[:,0])
train_y = list(training[:,1])

print("Trining data Created")

# Creating model - 3 layers. first layer- 128 neurons, 2nd layer - 64 neurons and 3rd ouptut layer = neurons equal to num of intents to predict op
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]), ), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))

sgd = SGD(lr = 0.01, decay=1e-6, momentum = 0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size = 5, verbose = 1)
model.save("chatbot_model.h5", hist)

print("Model Created")
