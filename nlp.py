# coding: utf-8
#import copy
import random
import logging
import nltk
import nltk.classify
from nltk.corpus import stopwords
from itertools import chain
from optparse import OptionParser
from scrape import configure_logging

'''
Test program that trains and classifies product descriptions.

First, Preinstall the requied python modules from the requirements.txt file.
Then, run the Macy's product scaper program (scrape.py).
Run nlp.py --help for help on options.

Training on a data set of approximately 10,000 data points requires about
3.5 GB of RAM.
'''

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

info = logger.info
warn = logger.warn
error = logger.error
debug = logger.debug


def top_words(data, limit=None):
    """
    documents: A list of word tokens for each document.
    """
    #fd = nltk.FreqDist((w.lower() for w in \
            #chain(*(d[3].split() for d in data))))
    fd = nltk.FreqDist(chain(*(d[4] for d in data)))
    if limit is not None:
        return fd.keys()[:limit]
    return fd.keys()


def document_features(tokens, word_features):
    words = set(tokens)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in words)
    return features


def tokenize(s, stemmer, mystopwords):
    return [stemmer.stem(t)
                for t in map(unicode.lower, nltk.wordpunct_tokenize(s))
                if t not in mystopwords]


porter = nltk.PorterStemmer()
eng_stop_words = set(stopwords.words("english"))
stop_punct = set([c for c in "(){}[]\|;:'\"<>,./?-_=+!@#$%^&*~`"])

'''
data is a list of lists of:
[
 [<category list>, <product id>, <product title>, <product description>]
 ...
]
'''


def tokenize_data(data):
    stop_set = eng_stop_words | stop_punct
    for entry in data:
        entry.append(tokenize(entry[2] + " " + entry[3], porter, stop_set))


def features(data, catn=1):
    """
    Return a list of pairs of (feature_dict, class label) 2-tuples.
    catn: Max category depth to use as the class label.
    """
    word_features = top_words(data, limit=2000)
    classified_features = [(document_features(d[4], word_features),
                            d[0][min(len(d[0])-1, catn)])
                            for d in data]
    return classified_features


def train_classifier(classified_features):
    classifier = nltk.NaiveBayesClassifier.train(classified_features)
    return classifier


def test_classification(data, catn=1):
    """
    Before calling this function, data should be randomized.
    IE:
        data = copy.copy(data)
        random.shuffle(data)  # in place random shuffle
    """
    tokenize_data(data)
    samples = len(data)
    print ("{0} Data Samples.".format(samples))
    train_samples = int(samples * 0.9)
    print ("Generating features...")
    classified_features = features(data, catn)
    train_set = classified_features[:train_samples]
    test_set = classified_features[train_samples:]
    print ("Training Classifier...")
    classifier = train_classifier(train_set)
    print ("Testing Accuracy...")
    accuracy = nltk.classify.accuracy(classifier, test_set)
    classifier.show_most_informative_features(25)
    print ("Accuracy: {0}".format(accuracy))
    print ("A few examples: ")
    for i in range(20):
        doc = random.choice(classified_features)
        prediction = classifier.classify(doc[0])
        actual = doc[1]
        print ("Actual: {0} | Prediction: {1}".format(actual, prediction))

    return classifier, classified_features


def nlpchain(data):
    tokenize_data(data)
    classified_features = features(data)
    return train_classifier(classified_features)


import codecs
from os.path import walk, join as pathjoin
from scrape import fix_chars


def load_data(basepath):
    data = []
    def load_file(fname):
        #debug("Loading data from: {0}".format(fname))
        with codecs.open(fname, encoding='utf-8') as fp:
            lines = fix_chars(fp.read()).splitlines()
            #lines = fp.read().splitlines()

        if len(lines) > 3:
            cats = [c.strip() for c in lines[0].split(",")]
            pid = int(lines[1].strip())
            title = lines[2]
            desc = lines[3]
            data.append([cats, pid, title, desc])
        else:
            warn("Invalid input file: {0}. Lines: {1}. Skipping."
                    .format(fname, len(lines)))

    def cb(arg, dirname, fnames):
        #print("Walking: {0}".format(dirname))
        for fname in fnames:
            if fname.endswith(".txt"):
                load_file(pathjoin(dirname, fname))

    walk(basepath, cb, None)
    return data


def main():
    configure_logging()

    parser = OptionParser(description="NLTK Classifier Test.")

    parser.add_option("-c", "--category", dest="category",
                      type="int",
                      default=1,
                      help=("Category Index. Integer in range [1, 3]. "
                            "Specifies the category depth in the product "
                            "category hierarchy to attempt to classify."),
                      metavar="CATEGORY")

    parser.add_option("-p", "--data-path", dest="datapath",
                      default="./data",
                      help=("Path to scraped data files. Defaults to './data'"),
                      metavar="DATAPATH")

    (option, args) = parser.parse_args()

    if option.category not in range(1,4):
        parser.error("Invalid category depth.")

    print ("Loading data from directory: {0}".format(option.datapath))
    data = load_data(option.datapath)
    random.shuffle(data)  # in place random shuffle
    print (("Classifying product descriptions up to a product category "
            "hierarchy depth of {0}.").format(option.category))
    test_classification(data, option.category-1)


if __name__ == "__main__":
    main()
