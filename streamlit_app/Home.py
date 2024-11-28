import streamlit as st

class DashboardConfig:
    """Configuration for the dashboard."""
    TITLE: str = "Applied Statistics"
    SUBTITLE: str = "EDA and Data Cleaning On Real-Rorld Data"

class HomePage:
    """Main page handler for the dashboard."""
    
    def __init__(self) -> None:
        self.config = DashboardConfig()
        
    def set_page_config(self) -> None:
        st.set_page_config(
            page_title=self.config.TITLE,
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
    def show_welcome(self) -> None:
        st.title(self.config.TITLE)
        st.markdown("""
        Welcome to the Applied Statistics Dashboard!
        """)
        
    def show_dataset_preview(self) -> None:
        st.header("Available Datasets")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Companies Dataset")
            
        with col2:
            st.subheader("Sleep Quality Dataset")
            
    def run(self) -> None:
        self.set_page_config()
        self.show_welcome()
        self.show_dataset_preview()

if __name__ == "__main__":
    home_page = HomePage()
    home_page.run()