import streamlit as st
import pandas as pd
import re
import io
import base64

# Configure Streamlit page
st.set_page_config(
    page_title="Company Name Cleaner",
    page_icon="🏢",
    layout="wide"
)

# Apply custom CSS for better visibility
st.markdown("""
    <style>
        .stApp {
            background-color: white;
        }
        .main {
            padding: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

def clean_company_name(name):
    """
    Remove common business suffixes and clean up company names.
    """
    suffixes = [
        r'\bInc\.?$',
        r'\bCo\.?$',
        r'\bCorp\.?$',
        r'\bLLC$',
        r'\bLtd\.?$',
        r'\bLimited$',
        r'\bPLC$',
        r'\bL\.?P\.?$',
        r'\bL\.?L\.?C\.?$',
        r'\bP\.?C\.?$',
        r'\bCompany$',
        r'\bCorporation$',
        r'\bIncorporated$',
    ]
    
    name = str(name).strip()
    
    for suffix in suffixes:
        name = re.sub(suffix, '', name, flags=re.IGNORECASE)
    
    name = re.sub(r'[,\.\s]+$', '', name)
    name = ' '.join(name.split())
    
    return name

def get_download_link(df):
    """
    Generate a download link for the processed dataframe
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'data:file/csv;base64,{b64}'
    return href

# Add a title and description
st.title("✨ Company Name Cleaner")
st.markdown("""
This tool helps you clean company names by removing common suffixes like Inc., Co., Corp., etc.

**How to use:**
1. Upload your CSV file
2. Select the column containing company names
3. Click 'Clean Company Names'
4. Download your cleaned data
""")

# File upload section
st.subheader("📁 Upload Your Data")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Read the CSV
        df = pd.read_csv(uploaded_file)
        
        # Column selection
        st.subheader("🎯 Select Company Name Column")
        company_column = st.selectbox(
            "Which column contains the company names?",
            options=df.columns,
            index=0
        )
        
        # Process button
        if st.button("🧹 Clean Company Names"):
            # Process the data
            with st.spinner("Cleaning company names..."):
                df[f'cleaned_{company_column}'] = df[company_column].apply(clean_company_name)
            
            # Show results
            st.subheader("📊 Results Preview")
            st.dataframe(df[[company_column, f'cleaned_{company_column}']].head())
            
            # Download section
            st.subheader("📥 Download Cleaned Data")
            download_link = get_download_link(df)
            st.markdown(
                f'<a href="{download_link}" download="cleaned_companies.csv" '
                f'class="button">Download Cleaned CSV</a>',
                unsafe_allow_html=True
            )
            
            # Statistics
            st.subheader("📈 Statistics")
            total_changed = (df[company_column] != df[f'cleaned_{company_column}']).sum()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Records Modified", total_changed)
    
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.info("Please make sure your CSV file is properly formatted and try again.")
