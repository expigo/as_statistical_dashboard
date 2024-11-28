from pathlib import Path
from typing import Dict

class Settings:
    """Application-wide settings"""

    # proj structure
    ROOT_DIR: Path = Path(__file__).parent.parent.parent.parent
    DATA_DIR: Path = ROOT_DIR / "data"
    
    # Data files
    COMPANIES_FILE: Path = DATA_DIR / "Top_1000_Companies_Dataset.csv"
    SLEEP_FILES: Dict[str, Path] = {
        "bedtime": DATA_DIR / "quality_of_sleep_bedtime.csv",
        "wake_up": DATA_DIR / "quality_of_sleep_wake-up time.csv",
        "sleeping_time": DATA_DIR / "quality_of_sleep_sleepingtime.csv"
    }
    AIRBNB: Path = DATA_DIR / "Airbnb_Open_Data.csv"

settings = Settings()