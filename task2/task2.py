import os
import re
from bs4 import BeautifulSoup
import pymorphy2
from nltk.corpus import stopwords

morph = pymorphy2.MorphAnalyzer()
stop_words = set(stopwords.words("russian"))

os.makedirs("tokens", exist_ok=True)
os.makedirs("lemmas", exist_ok=True)

PAGES_DIR = "pages"

def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")
    text = text.lower()
    return text

def tokenize(text):
    words = re.findall(r"[а-яё]+", text)
    tokens = [
        w for w in words
        if w not in stop_words and len(w) > 2
    ]
    return sorted(set(tokens))

def lemmatize(tokens):
    lemma_dict = {}

    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        lemma_dict.setdefault(lemma, []).append(token)

    return lemma_dict

for filename in sorted(os.listdir(PAGES_DIR)):
    if not filename.endswith(".html"):
        continue

    page_num = filename.replace(".html", "")
    print(f"[PROCESS] page {page_num}")

    with open(os.path.join(PAGES_DIR, filename), "rb") as f:
        html = f.read()

    text = clean_text(html)
    tokens = tokenize(text)
    lemmas = lemmatize(tokens)

    with open(f"tokens/tokens_{page_num}.txt", "w", encoding="utf-8") as f:
        for token in tokens:
            f.write(token + "\n")

    with open(f"lemmas/lemmas_{page_num}.txt", "w", encoding="utf-8") as f:
        for lemma, forms in lemmas.items():
            f.write(lemma + " " + " ".join(forms) + "\n")