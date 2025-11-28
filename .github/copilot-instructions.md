## Purpose
Help an AI coding assistant be productive in the DSCBI_Project repository. Focus on the project's structure, where data comes from, how devs run things locally, and code patterns the agent should follow.

## Quick context (big picture)
- This repo is a small macroeconomic dashboard project (MINECOFIN). Primary artifacts:
  - `notebooks/` — data cleaning and exploratory notebooks (e.g., `Data_cleaning_and_database_connection.ipynb`).
  - `data/data.csv` — canonical raw dataset used by notebooks and the dashboard.
  - `data/project_collected_data/` — intended location for cleaned/derived CSV outputs.
  - `src/` — contains a script `Macro-economic-Dashboard-src-code.py` (dashboard entrypoint / experiment code).
  - `proenv/` — a committed Python virtual environment; use this to reproduce installs/versions.
  - `pyproject.toml` — declares build-system (hatchling) and core dependencies (pandas>=2, bokeh, requests, pycountry).

## Primary workflows and commands (repo-specific)
- Activate the included virtualenv on Windows PowerShell:
  - `& .\proenv\Scripts\Activate.ps1` — once active, `python`, `jupyter` and `streamlit` will use the env in `proenv`.
- Running notebooks: open `notebooks/` with Jupyter / Jupyter Lab after activating `proenv`.
- Running the dashboard/script: inspect `src/Macro-economic-Dashboard-src-code.py` for the entrypoint. Common patterns here include either running `python src/Macro-economic-Dashboard-src-code.py` or `streamlit run src/Macro-economic-Dashboard-src-code.py` depending on which framework (Dash vs Streamlit) the script uses — check for `app.run_server` or `st.*` usage.
- Packaging / metadata: `pyproject.toml` is the source of truth for runtime requirements and uses Hatchling as build backend.

## Project-specific conventions and patterns
- Data canonical location: always read from `data/data.csv` and write cleaned outputs to `data/project_collected_data/` when adding derived CSVs. Notebooks follow a melt pattern: see `notebooks/Data_cleaning_and_database_connection.ipynb` where `df.melt(id_vars=["Sector","Indicator","Description"], var_name="Year", value_name="Value")` is used — preserve those id_vars when transforming.
- Notebook-first data work: most ETL and cleaning is performed in notebooks. When converting notebook logic into scripts, preserve the cell-level ordering and add explicit env activation and file-path guards.
- Virtualenv in-repo: `proenv/` is checked in. Prefer using it for reproducibility rather than creating a new `.venv`.

## Where to look for examples and common fixes
- Use `notebooks/Data_cleaning_and_database_connection.ipynb` to see how data is loaded (`pd.read_csv(".../data/data.csv")`) and transformed (`melt`).
- The top-level `README.md` contains a short project summary and authors—use it as citation text when creating new docs.

## Integration points & external dependencies
- External runtime dependencies are declared in `pyproject.toml`. Notable libs: `pandas`, `bokeh`, `requests`, `pycountry`, `streamlit`/`dash` (used in notebooks).
- No CI/test runner is present in the repo; changes that add tests should include a simple command (pytest) and update `pyproject.toml` if necessary.

## Best practices for AI edits (what the agent should do)
- Preserve the notebook's data-shape assumptions: columns `Sector`, `Indicator`, `Description`, `Year`, `Value` appear in analyses. Don't rename or remove them silently.
- When adding scripts, include a small header showing how to run with the committed env. Example header:
  ```py
  # Activate proenv then: python src/your_script.py
  if __name__ == '__main__':
      main()
  ```
- If modifying `proenv/`, do not re-create the entire venv; instead, document package changes in `pyproject.toml` and provide installation notes.
- Keep notebook edits minimal and runnable: add a final cell that prints `df.head()` and shapes after transformations for quick validation.

## Concrete examples to reference in code reviews
- Data melt: `notebooks/Data_cleaning_and_database_connection.ipynb` cell that calls `df.melt(...)` — use this as canonical transform.
- Data read: `pd.read_csv("C:\\Users\\andrew.mushokambere\\Documents\\DSCBI\\DSCBI_Project\\data\\data.csv")` (absolute path in notebooks). Prefer changing to relative paths using `Path(__file__).parents[...]` in scripts.

## When unsure
- Search for `Sector`, `Indicator`, and `Description` to find code relying on the data schema.
- Prefer non-destructive changes: add new scripts/files and keep original notebooks intact unless you're explicitly refactoring for reproducibility.

## Ask for feedback
After applying changes, ask the repo owner which runtime they use to launch the dashboard (Dash vs Streamlit) so the agent can add precise run commands. If you want, I can open `src/Macro-economic-Dashboard-src-code.py` and annotate the entrypoint next.
