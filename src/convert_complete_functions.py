from pathlib import Path
import ast
import re
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = REPO_ROOT / "data" / "complete_functions.csv"
OUT_PATH = REPO_ROOT / "data" / "complete_functions.py"


def _strip_fenced(code: str) -> str:
    # remove surrounding triple-backtick fences and optional language tag
    code = code.strip()
    if code.startswith("```") and code.endswith("```"):
        # remove first and last fence lines
        code = "\n".join(code.splitlines()[1:-1])
    # also remove leading/trailing single/back quotes left from CSV artifacts
    return code.strip(' \t\n\r"\'`')


def cell_is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except Exception:
        return False


def main() -> None:
    df = pd.read_csv(CSV_PATH)
    funcs = df["full_function"].fillna("").astype(str)

    header = [
        "# Auto-generated module containing functions from data/complete_functions.csv",
        f"# Source: {CSV_PATH}",
        "",
    ]

    out_lines = header[:]

    skipped = 0
    written = 0
    for i, cell in enumerate(funcs, start=1):
        raw = _strip_fenced(cell)
        if not raw:
            continue

        # Ensure there's a separating newline between entries
        out_lines.append(f"# --- entry {i} ---")

        if cell_is_valid_python(raw):
            out_lines.append(raw)
            out_lines.append("")  # blank line
            written += 1
        else:
            # Comment out invalid code instead of emitting it verbatim to avoid SyntaxError
            out_lines.append(f"# SKIPPED ENTRY {i}: invalid Python (commented out below)")
            for ln in raw.splitlines():
                out_lines.append("# " + ln)
            # provide a harmless placeholder so module can be imported
            out_lines.append(f"def _skipped_entry_{i}():")
            out_lines.append("    pass")
            out_lines.append("")
            skipped += 1

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(out_lines), encoding="utf8")

    print(f"Wrote {written} function entries to '{OUT_PATH}' (skipped {skipped} invalid entries)")


if __name__ == "__main__":
    main()