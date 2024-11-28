import streamlit as st
from typing import Optional
import pandas as pd
from statdash.processing.sleep_processing import SleepDataProcessor

class SleepAnalysisPage:
    """Handler for the sleep analysis page."""
    
    def __init__(self) -> None:
        self.processor: Optional[SleepDataProcessor] = None
        
    def load_data(self) -> bool:
        """
        Load and process the sleep data.
        
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        try:
            self.processor = SleepDataProcessor()
            self.processor.load_data()
            self.processor.integrate_datasets()
            return True
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return False
    
    def show_data_overview(self) -> None:
        """Display the data overview section."""
        st.header("Sleep Patterns Overview")
        
        if self.processor and self.processor.processed_data is not None:
            tabs = st.tabs([
                "📊 Data Preview", 
                "👥 Gender Patterns", 
                "⏰ Time Analysis"
            ])
            
            with tabs[0]:
                st.dataframe(self.processor.processed_data.head(n=10))
                
            with tabs[1]:
                stats = self.processor.get_summary_statistics()
                st.write("Gender Distribution Across Time Periods")
                st.dataframe(stats['gender_time'])
                
            with tabs[2]:
                st.write("Time Period Analysis")
                st.info("Detailed time analysis will go here")
    
    def show_interactive_analysis(self) -> None:
        """Display interactive analysis options."""
        if not self.processor:
            return
            
        st.header("Interactive Analysis")
        
        analysis_type = st.selectbox(
            "Choose Analysis Type",
            [
                "Sleep Duration Patterns",
                "Eating Habits Impact",
                "Gender Comparisons"
            ]
        )
        
        # Placeholder for future implementations
        st.info(f"Analysis for {analysis_type} will be implemented here")
    
    def run(self) -> None:
        """Main method to run the sleep analysis page."""
        st.title("Sleep Quality Analysis")
        
        with st.spinner("Loading sleep data..."):
            if self.load_data():
                self.show_data_overview()
                self.show_interactive_analysis()
            else:
                st.error("Could not proceed with analysis due to data loading issues")

if __name__ == "__main__":
    analysis_page = SleepAnalysisPage()
    analysis_page.run()