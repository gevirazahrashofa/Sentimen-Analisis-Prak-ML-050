# -*- coding: utf-8 -*-
"""Sentimen Analisis SVM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1taEYaWXCpUwWqkLu-cj3T1G3QBn8Cpml

## **Sentimen Analisis Menggunakan SVM**

Nama : Gevira Zahra Shofa

NIM :  1227050050

Kelas : Prak. Pembelajaran Mesin E

Dataset : https://www.kaggle.com/competitions/si650winter11/data?select=training.txt

Import Library
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import pandas as pd
import numpy as np
from textblob import TextBlob
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import _pickle as cPickle
from scipy.io import loadmat
from sklearn.svm import SVC
import seaborn as sns
sns.set_context('notebook')
sns.set_style('white')

import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer ,TfidfVectorizer,TfidfTransformer
# Import train_test_split, StratifiedKFold, and cross_val_score from sklearn.model_selection
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, f1_score, confusion_matrix, roc_auc_score
from sklearn.pipeline import Pipeline
# Import GridSearchCV from sklearn.model_selection
from sklearn.model_selection import GridSearchCV
# Import learning_curve from sklearn.model_selection (or use learning_curve from sklearn.model_selection)
from sklearn.model_selection import learning_curve
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB

df=pd.read_csv("training.txt",sep="\t", names=['liked','text'],encoding="utf-8");
df.head(3)

"""Kode tersebut memuat data ulasan dari "training.txt" ke dalam pandas DataFrame. Kolom 'liked' menunjukkan sentimen, dan 'text' berisi teks ulasan. df.head(3) menampilkan tiga ulasan pertama sebagai contoh. Ini adalah langkah awal untuk analisis sentimen."""

print(len(df))

df.groupby('liked').describe()

"""Data Preprocessing"""

def tokens(review):
    return TextBlob(review).words

df.head().text.apply(tokens)

TextBlob("ready was not a good movie").tags
#nltk.help.upenn_tagset('JJ')

"""TextBlob untuk melakukan Part-of-Speech (POS) tagging pada teks "ready was not a good movie". Outputnya adalah daftar tuple yang memuat setiap kata dan label POS-nya (contoh: 'ready' sebagai kata benda 'NN', 'good' sebagai kata sifat 'JJ')."""

def to_lemmas(review):
    wordss = TextBlob(review.lower()).words
    # for each word, take its "base form" = lemma
    return [word.lemma for word in wordss]

df.text.head().apply(to_lemmas)

from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
lmtzr.lemmatize('octopi')
#nltk

"""Converting text data into vectors"""

bow_transformer = CountVectorizer(analyzer=to_lemmas).fit(df['text'])
print(len(bow_transformer.vocabulary_))

review1=df['text'][3]
print(review1)
#to check 3rd document/review in collection/database

bow=bow_transformer.transform([review1])
print(bow)
bow.shape

"""Proses transformasi teks review1 menjadi representasi numerik menggunakan bow_transformer.transform(). Hasilnya adalah Compressed Sparse Row (CSR) matrix, yang efisien untuk data teks yang umumnya sparse. Setiap angka dalam output menunjukkan kemunculan kata dalam review1 dan posisinya dalam vocabulary yang dibuat oleh bow_transformer."""

# print(bow_transformer.get_feature_names()[372])
# to check 372nd word in collection

# Use get_feature_names_out() instead of the deprecated get_feature_names()
print(bow_transformer.get_feature_names_out()[372])

review_bow = bow_transformer.transform(df['text'])
print( 'sparse matrix shape:', review_bow.shape)
print('number of non-zeros:', review_bow.nnz) #learn this
print( 'sparsity: %.2f%%' % (100.0 * review_bow.nnz))

"""Tf-idf Vectorizer"""

tfidf_transformer =TfidfTransformer().fit(review_bow)
review_tfidf = tfidf_transformer.transform(review_bow)
review_tfidf.shape

text_train, text_test, liked_train, liked_test = train_test_split(df['text'], df['liked'], test_size=0.2)
print(len(text_train), len(text_test), len(text_train) , len(text_test))

"""Pembagian data menjadi training dan testing set menggunakan train_test_split. Data teks (df['text']) dan label sentimen (df['liked']) dibagi dengan rasio 80:20 (test_size=0.2). Output menunjukkan ukuran training set (5534) dan testing set (1384) untuk teks dan label."""

pipeline_svm = Pipeline([
    ('bow', CountVectorizer(analyzer=to_lemmas)),
    ('tfidf', TfidfTransformer()),
    ('classifier', SVC()),
])

# pipeline parameters to automatically explore and tune
param_svm = [
  {'classifier__C': [1, 10, 100, 1000], 'classifier__kernel': ['linear']},
  {'classifier__C': [1, 10, 100, 1000], 'classifier__gamma': [0.001, 0.0001], 'classifier__kernel': ['rbf']},
]

# pipeline parameters to automatically explore and tune
param_svm = [
  {'classifier__C': [1, 10, 100, 1000], 'classifier__kernel': ['linear']},
  {'classifier__C': [1, 10, 100, 1000], 'classifier__gamma': [0.001, 0.0001], 'classifier__kernel': ['rbf']},
]

grid_svm = GridSearchCV(
    pipeline_svm, #object used to fit the data
    param_grid=param_svm,
    refit=True,  # fit using all data, on the best detected classifier
    n_jobs=-1,  # number of cores to use for parallelization; -1 for "all cores" i.e. to run on all CPUs
    scoring='accuracy',#optimizing parameter
    cv=StratifiedKFold(n_splits=5), # Changed n_folds to n_splits
)

# Commented out IPython magic to ensure Python compatibility.
# %time classifier = grid_svm.fit(text_train, liked_train) # find the best combination from param_svm
# print(classifier.grid_scores_) # Deprecated and removed
print(classifier.cv_results_) # Use cv_results_ instead

print(classification_report(liked_test, classifier.predict(text_test)))

"""Hasil evaluasi model klasifikasi menggunakan classification_report. Model memiliki performa sangat baik dengan precision, recall, dan f1-score sebesar 0.99 untuk kedua kelas (0 dan 1) serta akurasi 0.99. Ini mengindikasikan model mampu memprediksi sentimen dengan sangat akurat pada data testing."""

print(classifier.predict(["the vinci code is awesome"])[0])

print(classifier.predict(["the vinci code is bad"])[0])

def gaussKernel(x1, x2, sigma):
    ss=np.power(sigma,2)
    norm= (x1-x2).T.dot(x1-x2)
    return np.exp(-norm/(2*ss))
x1 = np.array([1, 2, 1])
x2 = np.array([0, 4, -1])
sigma = 2
gaussKernel(x1,x2,sigma)