import os
import re
import math
from collections import Counter
from bs4 import BeautifulSoup
import pymorphy2
from nltk.corpus import stopwords

PAGES_DIR = "pages"

OUT_TERMS = "tfidf_terms"
OUT_LEMMAS = "tfidf_lemmas"

os.makedirs(OUT_TERMS, exist_ok=True)
os.makedirs(OUT_LEMMAS, exist_ok=True)

morph = pymorphy2.MorphAnalyzer()
stop_words = set(stopwords.words("russian"))

token_pattern = re.compile(r"[а-яё]+")

documents_terms = {}
documents_lemmas = {}

# Читаем html документы

for filename in os.listdir(PAGES_DIR):

    if not filename.endswith(".html"):
        continue

    doc_id = filename.replace(".html", "")

    with open(os.path.join(PAGES_DIR, filename), "rb") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text().lower()

    words = token_pattern.findall(text)

    tokens = [
        w for w in words
        if w not in stop_words and len(w) > 2
    ]

    lemmas = [
        morph.parse(w)[0].normal_form
        for w in tokens
    ]

    documents_terms[doc_id] = tokens
    documents_lemmas[doc_id] = lemmas


# IDF терминов

N = len(documents_terms)

df_terms = Counter()

for terms in documents_terms.values():
    for term in set(terms):
        df_terms[term] += 1

idf_terms = {
    term: math.log(N / df)
    for term, df in df_terms.items()
}


# IDF лемм

df_lemmas = Counter()

for lemmas in documents_lemmas.values():
    for lemma in set(lemmas):
        df_lemmas[lemma] += 1

idf_lemmas = {
    lemma: math.log(N / df)
    for lemma, df in df_lemmas.items()
}


# TF-IDF терминов

for doc_id, terms in documents_terms.items():

    counts = Counter(terms)
    total = len(terms)

    with open(f"{OUT_TERMS}/tfidf_{doc_id}.txt", "w", encoding="utf-8") as f:

        for term, count in counts.items():

            tf = count / total
            idf = idf_terms[term]

            tfidf = tf * idf

            f.write(f"{term} {idf:.6f} {tfidf:.6f}\n")


# TF-IDF лемм

for doc_id, lemmas in documents_lemmas.items():

    counts = Counter(lemmas)
    total = len(lemmas)

    with open(f"{OUT_LEMMAS}/tfidf_{doc_id}.txt", "w", encoding="utf-8") as f:

        for lemma, count in counts.items():

            tf = count / total
            idf = idf_lemmas[lemma]

            tfidf = tf * idf

            f.write(f"{lemma} {idf:.6f} {tfidf:.6f}\n")


print("TF-IDF рассчитан")