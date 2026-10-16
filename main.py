import os
import zipfile

import compress_pickle

SHEETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheets")
CACHE_ENTRY = "xl/calcChain.bin"


def load_compiled(xlsx_path):
    with zipfile.ZipFile(xlsx_path, "r") as zf:
        if CACHE_ENTRY not in zf.namelist():
            return None
        data = zf.read(CACHE_ENTRY)
    return compress_pickle.loads(data, compression="lz4")


def evaluate_all():
    results = {}
    for name in sorted(os.listdir(SHEETS_DIR)):
        if not name.endswith(".xlsx"):
            continue
        path = os.path.join(SHEETS_DIR, name)
        try:
            compiler = load_compiled(path)
            if compiler:
                results[name] = compiler
        except Exception:
            pass
    return results


def main():
    results = evaluate_all()


if __name__ == "__main__":
    main()
