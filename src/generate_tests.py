import os
import time
from typing import List, Optional
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from openai import OpenAI

# Resolve data files relative to the repository root (two levels up from this file)
REPO_ROOT = Path(__file__).resolve().parents[1]
COMPLETE_CSV = str(REPO_ROOT / "data" / "complete_functions.csv")
OUTPUT_CSV = str(REPO_ROOT / "data" / "generated_tests.csv")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

client = OpenAI(api_key=OPENAI_API_KEY)


# Prompt to pass to GPT-4 for generating tests
SYS_PROMPT = (
    "You are an expert Python developer who writes concise pytest unit tests. "
    "Given a single Python function implementation, produce a pytest-compatible test file that "
    "contains multiple meaningful tests (normal, edge, and error cases). Do not make any references to functions " \
    "that are not defined in the provided function code or standard libraries. " \
    "Return only valid Python test code with no extra commentary or explanation. Do not under any circumstances " \
    "write any comments or text that is not runnable Python code."
)


def make_user_prompt(function_code: str, index: int) -> str:
    return (
        f"Function #{index}:\n"
        "```python\n"
        f"{function_code}\n"
        "```\n\n"
        "Write pytest tests for the function above. Include any needed imports and fixtures. "
        "Prefer simple, deterministic tests that can run without network or unusual side effects. "
        "If the function requires dependencies, mock them. Return only Python test code. Do not under "
        "any circumstances write any comments or text that is not runnable Python code."
    )

def generate_tests_for_functions(functions: List[str], retry_times: int = 3, delay: float = 1.0) -> List[Optional[str]]:
    results: List[Optional[str]] = []
    for i, func in enumerate(tqdm(functions, desc="Generating tests")):
        if not func or not func.strip():
            results.append(None)
            continue

        prompt = make_user_prompt(func, i + 1)
        attempt = 0

        # Prompt GPT-4 to generate tests
        while attempt < retry_times:
            try:
                resp = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": SYS_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=1200,
                    temperature=0.0,
                )
                
                # Add response to results list
                content = resp.choices[0].message.content
                results.append(content)
                break

            # If there was an error, retry after delay
            except Exception as e:
                attempt += 1
                if attempt >= retry_times:
                    results.append(None)
                time.sleep(delay * attempt)
    return results

def main(limit: Optional[int] = None) -> None:
    df = pd.read_csv(COMPLETE_CSV)
    funcs = df["full_function"].fillna("").astype(str)

    # Apply limit if specified
    if limit is not None:
        funcs = funcs.iloc[:limit]

    # Generate test for each function
    tests = generate_tests_for_functions(list(funcs))

    # Create new dataframe for generated tests and save to CSV
    out_df = pd.DataFrame({"full_function": funcs, "generated_test": tests})
    out_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(out_df)} rows to '{OUTPUT_CSV}'")


if __name__ == "__main__":
    main(5)