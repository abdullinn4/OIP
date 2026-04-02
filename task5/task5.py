import os
import math
import pymorphy2
from collections import defaultdict, Counter
from nltk.corpus import stopwords

TFIDF_LEMMAS_DIR = "tfidf_lemmas"

TOP_N = 10
stop_words = set(stopwords.words("russian"))
morph = pymorphy2.MorphAnalyzer()

# Загрузка TF-IDF документов
documents_vectors = {}
all_lemmas = set()
idf_values = {}

for filename in os.listdir(TFIDF_LEMMAS_DIR):
    if not filename.endswith(".txt"):
        continue
    doc_id = filename.replace("tfidf_", "").replace(".txt", "")
    vector = {}
    with open(os.path.join(TFIDF_LEMMAS_DIR, filename), encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                lemma, idf, tfidf = parts[0], float(parts[1]), float(parts[2])
                vector[lemma] = tfidf
                all_lemmas.add(lemma)
                idf_values[lemma] = idf
    documents_vectors[doc_id] = vector

# Косинусное сходство
def cosine_similarity(vec1, vec2):
    dot = sum(vec1.get(k, 0.0) * vec2.get(k, 0.0) for k in all_lemmas)
    norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


# Преобразование запроса в TF-IDF вектор
def query_to_vector(query):
    words = [w.lower() for w in query.split()]
    tokens = [
        w for w in words
        if w.isalpha() and w not in stop_words and len(w) > 2
    ]
    lemmas = [morph.parse(w)[0].normal_form for w in tokens]
    
    counts = Counter(lemmas)
    total = len(lemmas)
    vec = {}
    for lemma, count in counts.items():
        if lemma in all_lemmas:
            tf = count / total
            idf = idf_values[lemma]
            vec[lemma] = tf * idf
    return vec

# Поиск документов
def search(query, top_n=TOP_N):
    q_vec = query_to_vector(query)
    scores = []
    for doc_id, doc_vec in documents_vectors.items():
        score = cosine_similarity(q_vec, doc_vec)
        if score > 0:
            scores.append((doc_id, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]


while True:
    query = input("Введите запрос (или 'exit' для выхода): ")
    if query.lower() == "exit":
        break
    results = search(query)
    if not results:
        print("Документы не найдены")
    else:
        print("Топ документов:")
        for doc_id, score in results:
            print(f"{doc_id} (сходство: {score:.4f})")