from typing import Optional, Dict, List
import pandas as pd
import numpy as np
from scipy import stats

class CompaniesDataProcessor:
    """A class to handle and analysis of the Top 1000 Companies Dataset"""

    def __init__(self, df: Optional[pd.DataFrame] = None):
        """
        Initialize the processor with optional dataframe.
        
        Args:
            df: Optional pandas DataFrame containing companies data
        """
        self.raw_data = df
        self.processed_data = None
        self.numerical_columns: List[str] = []
        self.categorical_columns: List[str] = []
        self.datetime_columns: List[str] = []
        
    def load_data(self, filepath: str) -> None:
        """
        Load data from CSV file.
        
        Args:
            filepath: Path to the CSV file
        """
        self.raw_data = pd.read_csv(filepath)
        
    def identify_column_types(self) -> Dict[str, List[str]]:
        """
        Identify and categorize columns by their data types.
        
        Returns:
            Dictionary containing lists of column names by type
        """
        if self.raw_data is None:
            raise ValueError("No data loaded. Please load data first.")
            
        # Identify numerical columns (excluding year-like numbers)
        self.numerical_columns = self.raw_data.select_dtypes(
            include=['int64', 'float64']
        ).columns.tolist()
        
        # Identify categorical columns
        self.categorical_columns = self.raw_data.select_dtypes(
            include=['object', 'category']
        ).columns.tolist()
        
        # Look for potential datetime columns
        self.datetime_columns = [
            col for col in self.categorical_columns 
            if 'date' in col.lower() or 'founded' in col.lower()
        ]
        
        return {
            'numerical': self.numerical_columns,
            'categorical': self.categorical_columns,
            'datetime': self.datetime_columns
        }

    def clean_numerical_columns(self) -> None:
        """
        Clean numerical columns by handling missing values and outliers.
        """
        if self.raw_data is None:
            raise ValueError("No data loaded. Please load data first.")
            
        self.processed_data = self.raw_data.copy()
        
        for col in self.numerical_columns:
            # Convert string representations of numbers (e.g., "1.2B", "$500M")
            if self.processed_data[col].dtype == 'object':
                self.processed_data[col] = self._convert_financial_string(
                    self.processed_data[col]
                )
            
            # Handle missing values
            median_value = self.processed_data[col].median()
            self.processed_data[col] = self.processed_data[col].fillna(median_value)
            
    @staticmethod
    def _convert_financial_string(series: pd.Series) -> pd.Series:
        """
        Convert string representations of financial numbers to float values.
        
        Args:
            series: Pandas series containing financial strings
            
        Returns:
            Converted series with float values
        """
        def convert_value(val):
            if pd.isna(val):
                return np.nan
            if isinstance(val, (int, float)):
                return val
                
            val = str(val).upper()
            val = val.replace('$', '').replace(',', '')
            
            multipliers = {'K': 1e3, 'M': 1e6, 'B': 1e9}
            for suffix, multiplier in multipliers.items():
                if val.endswith(suffix):
                    try:
                        return float(val[:-1]) * multiplier
                    except ValueError:
                        return np.nan
            try:
                return float(val)
            except ValueError:
                return np.nan
                
        return series.apply(convert_value)
        
    def get_summary_statistics(self) -> Dict[str, pd.DataFrame]:
        """
        Calculate summary statistics for numerical and categorical columns.
        
        Returns:
            Dictionary containing summary statistics for different column types
        """
        if self.processed_data is None:
            raise ValueError("Data not processed. Please process data first.")
            
        numerical_stats = self.processed_data[self.numerical_columns].describe()
        
        categorical_stats = pd.DataFrame({
            col: self.processed_data[col].value_counts().head()
            for col in self.categorical_columns
        })
        
        return {
            'numerical_statistics': numerical_stats,
            'categorical_statistics': categorical_stats
        }
        
    def detect_outliers(
        self, 
        columns: Optional[List[str]] = None, 
        method: str = 'iqr'
    ) -> Dict[str, pd.Series]:
        """
        Detect outliers in specified numerical columns.
        
        Args:
            columns: List of columns to check for outliers
            method: Method to use for outlier detection ('iqr' or 'zscore')
            
        Returns:
            Dictionary containing boolean masks for outliers in each column
        """
        if columns is None:
            columns = self.numerical_columns
            
        outliers = {}
        for col in columns:
            if method == 'iqr':
                Q1 = self.processed_data[col].quantile(0.25)
                Q3 = self.processed_data[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers[col] = (
                    (self.processed_data[col] < (Q1 - 1.5 * IQR)) | 
                    (self.processed_data[col] > (Q3 + 1.5 * IQR))
                )
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(self.processed_data[col]))
                outliers[col] = z_scores > 3
            else:
                # TODO: add more outlier detection methods
                raise ValueError("method not implmented yet!")
                
        return outliers
