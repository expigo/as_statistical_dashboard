from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from scipy import stats
from statdash.config.settings import settings

class SleepDataProcessor:
    """A class to handle and analysis of the Quality of Sleep Dataset"""

    def __init__(self) -> None:
        """Initialize the sleep data processor."""
        self.raw_data: Dict[str, Optional[pd.DataFrame]] = {
            'bedtime': None,
            'wake_up': None,
            'sleeping_time': None
        }
        
        self.processed_data: Optional[pd.DataFrame] = None
        
        # Store unique categories
        self.time_periods: List[str] = []
        self.terms: List[str] = []
        self.habits: List[str] = []
        
    def load_data(self) -> None:
        """
        Load data from all three sleep-related CSV files.
        """
        try:
            for key, file_path in settings.SLEEP_FILES.items():
                try:
                    self.raw_data[key] = pd.read_csv(file_path)
                except Exception as e:
                    raise ValueError(f"Error reading {key} file: {str(e)}")
            
            # extract unique categories
            self._extract_categories()
            
        except Exception as e:
            raise ValueError(f"Error in data loading process: {str(e)}")
    
    def _extract_categories(self) -> None:
        """
        Extract unique categories from the loaded data.
        """
        if any(df is None for df in self.raw_data.values()):
            raise ValueError("Not all data files have been loaded")
            
        # bedtime time as reference column
        df = self.raw_data['bedtime']
        if df is None:  
            raise ValueError("Bedtime data is missing")
            
        # extract unique values
        self.time_periods = df['time'].unique().tolist()
        self.terms = df['terms'].unique().tolist()
        # Get habit columns by excluding known non-habit columns
        self.habits = [col for col in df.columns 
                      if col not in ['sex', 'time', 'terms']]
    
    def integrate_datasets(self) -> None:
        """
        Integrate the three datasets into a unified structure.
        
        This method combines data from different time-related files while
        preserving the relationships between behaviors and adding source
        tracking for each record.
        """
        # check if any of our DataFrames are None
        if any(df is None for df in self.raw_data.values()):
            raise ValueError("Not all data files have been loaded")
            
        # create identifier columns to track data source
        dfs = []
        for source, df in self.raw_data.items():
            if df is not None:  # Extra safety check
                df_copy = df.copy()
                df_copy['source'] = source
                dfs.append(df_copy)
        
        if not dfs:  
            raise ValueError("No valid datasets to combine")
            
        self.processed_data = pd.concat(dfs, axis=0, ignore_index=True)
        
        # convert frequency columns to numeric, handling any non-numeric values
        habit_columns = [col for col in self.processed_data.columns 
                        if col not in ['sex', 'time', 'terms', 'source']]
        
        for col in habit_columns:
            self.processed_data[col] = pd.to_numeric(
                self.processed_data[col], 
                errors='coerce' # set invalid to NaN
            )
    
    def get_summary_statistics(self) -> Dict[str, pd.DataFrame]:
        """
        Calculate summary statistics for the integrated dataset.
        
        Returns:
            Dictionary containing various statistical summaries:
            - Frequency distributions by gender
            - Time period distributions
            - Habit patterns
        """
        if self.processed_data is None:
            raise ValueError("Data has not been processed yet")
            
        stats = {}
        
        # gender distribution across different times
        stats['gender_time'] = pd.crosstab(
            self.processed_data['sex'],
            self.processed_data['time']
        )
        
        # overall frequency of different habits
        habit_columns = [col for col in self.processed_data.columns 
                        if col not in ['sex', 'time', 'terms', 'source']]
        
        stats['habit_summary'] = self.processed_data[habit_columns].describe()
        
        return stats
