#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import io

def process_data(data):
    # Split the data into rows
    rows = data.split('\n')
    
    # Create a list to store the processed data
    processed_data = []
    
    # Process each row
    for row in rows:
        # Split the row into spokespeople
        spokespeople = row.split('|')
        
        # Process each spokesperson
        for spokesperson in spokespeople:
            # Split the spokesperson into name and frequency
            parts = spokesperson.strip().rsplit(' ', 1)
            name = parts[0].strip()
            frequency = int(parts[1]) if len(parts) > 1 and parts[1].strip().isdigit() else 1
            
            # Add the spokesperson and frequency to the processed data
            processed_data.append((name, frequency))
    
    # Create a DataFrame from the processed data
    df = pd.DataFrame(processed_data, columns=['Spokesperson', 'Frequency'])
    
    # Group the DataFrame by spokesperson and sum the frequencies
    df = df.groupby('Spokesperson').sum().reset_index()
    
    return df

def main():
    st.title('Spokesperson Frequency App')
    
    # Get the input data from the user
    data = st.text_area('Enter the data:', height=200)
    
    if st.button('Process Data'):
        # Process the data
        df = process_data(data)
        
        # Display the preview of the CSV file
        st.subheader('Preview of CSV file:')
        st.write(df)
        
        # Convert the DataFrame to CSV
        csv = df.to_csv(index=False)
        
        # Create a download button for the CSV file
        st.download_button(
            label='Download CSV',
            data=csv,
            file_name='spokesperson_frequency.csv',
            mime='text/csv'
        )

if __name__ == '__main__':
    main()
# In[ ]:
