import streamlit as st
import pandas as pd
from typing import Optional, List, Dict
from statdash.processing.companies_processing import CompaniesDataProcessor
from statdash.config.settings import settings

class CompaniesPage:
    """Handler for the companies analysis page."""
    
    def __init__(self) -> None:
        self.processor: Optional[CompaniesDataProcessor] = None
        self.data: Optional[pd.DataFrame] = None
        
    def load_data(self) -> None:
        """Load and process the companies data."""
        try:
            self.processor = CompaniesDataProcessor()
            self.processor.load_data(settings.COMPANIES_FILE)
            self.processor.identify_column_types()
            self.processor.clean_numerical_columns()
            self.data = self.processor.processed_data
            if self.data is None or self.data.empty:
                st.error("No data was loaded")
                return False
                
            if not self.processor.numerical_columns:
                st.warning("No numerical columns found in the data")
                return False
            
            return True
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            
    def show_data_overview(self) -> None:
        """Display the data overview section."""
        st.header("Companies Data Overview")
        
        if self.data is not None:
            tab1, tab2 = st.tabs(["📊 Data Preview", "📈 Summary Statistics"])
            
            with tab1:
                st.dataframe(self.data.head(n=10))
                
            with tab2:
                if self.processor:
                    stats = self.processor.get_summary_statistics()
                    st.write("Numerical Statistics")
                    st.dataframe(stats['numerical_statistics'])
                    
    def show_interactive_analysis(self) -> None:
        """Display interactive analysis options."""
        st.header("Interactive Analysis")
        
        analysis_type = st.selectbox(
            "Choose Analysis Type",
            ["Distribution Analysis", "Correlation Analysis", "Outlier Detection"]
        )
        
        # TODO: implement this and more
        if analysis_type == "Distribution Analysis":
            st.info("Distribution analysis will be implemented here anywhere soon hopefully")
            
    def run(self) -> None:
        """Main method to run the companies analysis page."""
        st.title("Companies Data Analysis")
        
        with st.spinner("Loading data..."):
            if self.load_data():
                self.show_data_overview()
                self.show_interactive_analysis()
            else:
                st.error("Could not proceed with analysis due to data loading issues")

if __name__ == "__main__":
    analysis_page = CompaniesPage()
    analysis_page.run()