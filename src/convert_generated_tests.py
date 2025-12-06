import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEST_CSV = os.path.join(BASE_DIR, "..", "data", "generated_tests.csv")
OUT_DIR = os.path.join(BASE_DIR, "..", "generated_tests")

os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(TEST_CSV)

for i, row in df.iterrows():
    code = row["generated_test"]
    func_name = f"test_generated_{i+1:03d}.py"
    path = os.path.join(OUT_DIR, func_name)

    if isinstance(code, str) and code.strip():
        # Strip surrounding triple-backtick fenced code blocks if present.
        def _strip_fenced(code_text: str) -> str:
            txt = code_text.strip()
            # Try to capture a fenced block like ```python\n...\n``` anywhere in the text
            m = re.search(r"```(?:\w+)?\n(.*?)```", txt, re.DOTALL)
            if m:
                return m.group(1).strip()
            # If no fenced block, just remove stray backticks and return
            if '```' in txt:
                return txt.replace('```', '').strip()
            return txt

        cleaned = _strip_fenced(code)
        with open(path, "w", encoding="utf8") as f:
            f.write(cleaned)
