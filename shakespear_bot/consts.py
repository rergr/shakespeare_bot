from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data_set"
HARRY_POTTER_PATH = DATA_DIR / "harry_potter.txt"
SHAKESPEARE_PATH = DATA_DIR / "shakespeare.txt"

ASSESTS_DIR = BASE_DIR / "assets"

SP_DIR = ASSESTS_DIR / "sp.png"
SP_GIF_DIR =  ASSESTS_DIR / "sp.gif"

MODEL_DIR = BASE_DIR / "models"
ONE_STEP_DIR = MODEL_DIR / "one_step"

LOGS_DIR = BASE_DIR / "logs"
LOG_DIR = LOGS_DIR / "log.txt"
LOGSH_DIR = LOGS_DIR / "logsh.txt"
