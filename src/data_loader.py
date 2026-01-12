
import pandas as pd
from pathlib import Path

# MAIN_FILE_PATH = Path.cwd().parent
# DATA_FILE_PATH = MAIN_FILE_PATH / "data"
# DATA_FILE = DATA_FILE_PATH / "Basic_Macro_Indicators_Cleaned.csv"

BASE_DIR = Path(__file__).parent.parent  # go up from src/ to project root
DATA_FILE = BASE_DIR / "data" / "Basic_Macro_Indicators_Cleaned.csv"

def load_data(data_file=DATA_FILE):
    data = pd.read_csv(data_file)
    return data

# ==============================

