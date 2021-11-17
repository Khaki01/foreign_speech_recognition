from flair.models import TextClassifier
from flair.data import Sentence


with open('audio/testaudio.txt') as f:
    lines = f.readlines()
print(lines)
classifier = TextClassifier.load('en-sentiment')

def flair_prediction(x):
    sentence = Sentence(x)
    classifier.predict(sentence)
    score = sentence.labels[0]
    if "POSITIVE" in str(score):
        return "pos {}".format(sentence.labels[0])
    elif "NEGATIVE" in str(score):
        return "neg {}".format(sentence.labels[0])
    else:
        return "neu {}".format(sentence.labels[0])

results = map(flair_prediction, lines)
# print sentence with predicted labels
print(results)
