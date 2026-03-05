import os
import json

LEMMA_DIR = "lemmas"
INDEX_FILE = "inverted_index.json"

#список терминов (индекс)
inverted_index = {}

for filename in os.listdir(LEMMA_DIR):
    if not filename.endswith(".txt"):
        continue

    doc_id = filename.replace("lemmas_", "").replace(".txt", "")

    with open(os.path.join(LEMMA_DIR, filename), "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            lemma = parts[0]
            inverted_index.setdefault(lemma, set()).add(doc_id)

# преобразуем множества в списки
for lemma in inverted_index:
    inverted_index[lemma] = sorted(list(inverted_index[lemma]))

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    json.dump(inverted_index, f, ensure_ascii=False, indent=2)

print("Индекс создан.")