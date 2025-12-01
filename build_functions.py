import pandas as pd
from typing import List, Optional
from strip_prompts import strip_code

# Global constants. These can be changed to modify the data returned as needed
PARQUET_PATH = 'hf://datasets/openai/openai_humaneval/openai_humaneval/test-00000-of-00001.parquet'
STRIPPED_CSV = 'stripped_prompts.csv'
ORIGINAL_CSV = 'original_prompts.csv'
LIMIT: Optional[int] = None
PROMPT_COL = 'prompt'
SOLUTION_COL = 'canonical_solution'

# Process a dataframe, stripping prompts and returning a new dataframe
def process_dataframe(df: pd.DataFrame, limit: Optional[int] = None) -> pd.DataFrame:
    # Get prompts and solutions from dataframe
    prompts = df[PROMPT_COL]
    solutions = df[SOLUTION_COL]
    
    # Limit number of prompts if specified
    if limit is not None:
        prompts = prompts.iloc[:limit]

    # Iterate through prompts and strip each one, adding to new stripped_list
    stripped_list: List[Optional[str]] = []
    for raw, sol in zip(prompts, solutions):
        try:
            stripped_list.append(strip_code(raw, sol))
        except Exception:
            stripped_list.append(None)

    # Create new dataframe with original prompts and stripped prompts
    out_df = pd.DataFrame({
        PROMPT_COL: prompts.values,
        'stripped_prompt': stripped_list,
    })
    return out_df


def main() -> None:
    print(f"Loading dataframe from '{PARQUET_PATH}'...")

    # Init dataframe from parquet file
    df = pd.read_parquet(PARQUET_PATH)

    # Save original prompts to CSV
    df[PROMPT_COL].to_csv(ORIGINAL_CSV, index=False)
    print(f"Saved {len(df)} original prompts to '{ORIGINAL_CSV}'")

    # Create new dataframe with stripped prompts
    out_df = process_dataframe(df, limit=LIMIT)

    # Convert new dataframe to CSV
    out_df.to_csv(STRIPPED_CSV, index=False)
    print(f"Saved {len(out_df)} stripped prompts to '{STRIPPED_CSV}'")


if __name__ == '__main__':
    main()
