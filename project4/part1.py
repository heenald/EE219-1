from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
import nltk
from nltk.stem.snowball import SnowballStemmer
import string
import re

# Uncomment if the machine is missing punkt, wordnet or stopwords modules.
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# RegExpTokenizer reduces term count from 29k to 25k

def fetch_all_categories():
    return [
       "comp.graphics",
       "comp.os.ms-windows.misc",
       "comp.sys.ibm.pc.hardware",
       "comp.sys.mac.hardware"
    ] + [
       "rec.autos",
       "rec.motorcycles",
       "rec.sport.baseball",
       "rec.sport.hockey"
    ]

def fetch_train(categories):
    return fetch_20newsgroups(
        subset = 'train',
        categories = categories,
        shuffle=True,
        random_state = 42
    )

def fetch_test(categories):
    return fetch_20newsgroups(
        subset = 'test',
        categories = categories,
        shuffle=True,
        random_state = 42
    )

class StemTokenizer(object):
    def __init__(self):
        self.snowball_stemmer = SnowballStemmer("english")

    def __call__(self, doc):
        doc = re.sub('[,.-:/()?{}*$#&]', ' ', doc)
        doc = ''.join(ch for ch in doc if ch not in string.punctuation)
        doc = ''.join(ch for ch in doc if ord(ch) < 128)
        doc = doc.lower()
        words = doc.split()
        words = [word for word in words if word not in text.ENGLISH_STOP_WORDS]

        return [
            self.snowball_stemmer.stem(word) for word in words
        ]

def get_vectorizer():
    return CountVectorizer(
        tokenizer=StemTokenizer(),
        lowercase=True,
        min_df = 2,
        max_df = 0.99
    )

def get_tfid_transformer():
    return TfidfTransformer(
        norm='l2',
        sublinear_tf=True
    )

def get_train_idf():
    
    categories= fetch_all_categories()
    
    pipeline = Pipeline(
        [
            ('vectorize', get_vectorizer()),
            ('tf-idf', get_tfid_transformer())
        ]
    )
    
    train = fetch_train(categories)
    
    print("%d documents" % len(train.filenames))
    print("%d categories" % len(train.target_names))
    
    train_idf = pipeline.fit_transform(train.data)
    print "Number of terms in TF-IDF representation:",train_idf.shape[1]

    return train_idf

if __name__ == "__main__":
    get_train_idf()