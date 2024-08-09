import streamlit as st
import pandas as pd

# Function to load and process data from the selected Excel file
def load_and_process_data(file):
    # Load the Excel file
    df = pd.read_excel(file, usecols='C:T', skiprows=1)  # Read columns C to T, starting at row 2
    
    # Define the column names
    df.columns = [
        'TYPE', 'Account Group Code', 'Account Group Name', 'Ledger Account Code', 'Ledger Account Name', 
        'SAPGL CODE', 'NAME', 'Gain', 'Loss', 'REMARKS- IAD', 'FVTPL', 'FVOCI', 'HTM', 
        'BUY - FVOCI', 'SELL - FVOCI', 'BUY - FVTPL', 'SELL - FVTPL', 'REMARKS'
    ]
    
    # Drop any rows where all elements are NaN
    df.dropna(how='all', inplace=True)
    
    # Create a new dataset
    new_data = []
    
    for index, row in df.iterrows():
        # Check each specified column and process if not empty
        columns_to_check = ['SAPGL CODE', 'Gain', 'Loss', 'FVTPL', 'FVOCI', 'HTM', 
                            'BUY - FVOCI', 'SELL - FVOCI', 'BUY - FVTPL', 'SELL - FVTPL']
        
        for column in columns_to_check:
            if pd.notna(row[column]):
                entry = {
                    'Type': row['TYPE'],
                    'Account Group Code': row['Account Group Code'],
                    'Ledger Account Code': row['Ledger Account Code'],
                    'Ledger Account Name': row['Ledger Account Name'],
                    'GL Account': str(row[column])  # Convert to string
                }
                new_data.append(entry)
    
    # Convert the new dataset to a DataFrame
    new_df = pd.DataFrame(new_data)
    
    return new_df

# Streamlit app
def main():
    st.title('Excel Data Processor on SAP GL Ledger Accounts')

    # Sidebar for file selection
    st.sidebar.header('File Selection')
    file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")
    
    if file:
        processed_data = load_and_process_data(file)
        st.write("Processed Data:")
        st.dataframe(processed_data)
    else:
        st.write("Please upload an Excel file.")

if __name__ == "__main__":
    main()
