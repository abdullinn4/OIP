import json
import re
import pymorphy2

INDEX_FILE = "inverted_index.json"

morph = pymorphy2.MorphAnalyzer()

# загружаем индекс
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    index = json.load(f)

for key in index:
    index[key] = set(index[key])

# множество всех документов
all_docs = set()
for docs in index.values():
    all_docs |= docs


# лемматизация
def lemmatize_word(word):
    return morph.parse(word)[0].normal_form


# поиск
def evaluate_query(query):
    query = query.lower()

    # Разбиваем на токены: слова, операторы, скобки
    tokens = re.findall(r"[а-яё]+|and|or|not|\(|\)", query)

    processed_tokens = []

    for token in tokens:
        if token in {"and", "or", "not"}:
            processed_tokens.append(token.upper())
        elif token in {"(", ")"}:
            processed_tokens.append(token)
        else:
            lemma = lemmatize_word(token)
            processed_tokens.append(f"index.get('{lemma}', set())")

    # Собираем строку обратно
    expression = " ".join(processed_tokens)

    # Заменяем операторы на python-операторы
    expression = expression.replace("AND", "&")
    expression = expression.replace("OR", "|")
    expression = expression.replace("NOT", "all_docs -")

    # Выполняем
    result = eval(expression)

    return result



# для ввода запроса

while True:
    user_query = input("Введите запрос: ")

    if user_query.lower() == "exit":
        break

    try:
        result = evaluate_query(user_query)
        print("Документы:", sorted(result))
    except Exception as e:
        print("Ошибка в запросе:", e)