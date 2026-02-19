import requests
import time
import os

os.makedirs("pages", exist_ok=True)

headers = {
    "User-Agent": "Educational crawler for university project"
}

urls = [f"https://ilibrary.ru/text/5152/p.{i}/index.html" for i in range(1, 120)]
index_lines = []

for i, url in enumerate(urls, start=1):
    try:
        resp = requests.get(url, headers=headers, timeout=10)

        if resp.status_code == 200:
            # Сохраняем байты напрямую
            with open(f"pages/{i}.html", "wb") as f:
                f.write(resp.content)

            index_lines.append(f"{i} {url}")
            print(f"[OK] {i}")

        else:
            print(f"[SKIP] {i} (status={resp.status_code})")

        time.sleep(0.5)

    except Exception as e:
        print(f"[ERROR] {i}: {e}")

with open("index.txt", "w", encoding="utf-8") as f_index:
    f_index.write("\n".join(index_lines))
