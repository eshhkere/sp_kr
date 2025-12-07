import os
import random

DIR = "test_files"


def create_files():
    if not os.path.exists(DIR):
        os.makedirs(DIR)

    # создаем 100 файлов с разным количеством строк
    for i in range(100):
        filename = os.path.join(DIR, f"file_{i}.txt")
        line_count = random.randint(100, 5000)
        with open(filename, "w") as f:
            f.write("\n".join(["data"] * line_count))
    print(f"Создана директория '{DIR}' с тестовыми файлами.")


if __name__ == "__main__":
    create_files()
