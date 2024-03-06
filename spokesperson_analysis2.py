#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import io

def preprocess_data(data):
    # Split the data into rows
    rows = data.split('\n')
    
    # Create a dictionary to store the preprocessed data
    preprocessed_data = {}
    
    # Process each row
    for row in rows:
        # Split the row into spokespeople
        spokespeople = row.split('|')
        
        # Process each spokesperson
        for spokesperson in spokespeople:
            # Split the spokesperson into name and job title
            parts = spokesperson.strip().split(' - ')
            if len(parts) > 1:
                name = parts[0].strip()
                job_title = parts[1].strip()
            else:
                name = parts[0].strip()
                job_title = ''
            
            # Check if the spokesperson already exists in the preprocessed data
            if name in preprocessed_data:
                # If the spokesperson exists and the stored job title is empty, update it with the current job title
                if not preprocessed_data[name]:
                    preprocessed_data[name] = job_title
            else:
                # If the spokesperson doesn't exist, add them to the preprocessed data
                preprocessed_data[name] = job_title
    
    # Create a new data string with the preprocessed data
    preprocessed_data_string = ''
    for name, job_title in preprocessed_data.items():
        preprocessed_data_string += f"{name} - {job_title}\n"
    
    return preprocessed_data_string

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
            parts = spokesperson.strip().split()
            if len(parts) > 1 and parts[-1].isdigit():
                name = ' '.join(parts[:-1])
                frequency = int(parts[-1])
            else:
                name = ' '.join(parts)
                frequency = 1
            
            # Add the spokesperson and frequency to the processed data if the name is not blank
            if name.strip():
                processed_data.append((name, frequency))
    
    # Create a DataFrame from the processed data
    df = pd.DataFrame(processed_data, columns=['Spokesperson', 'Frequency'])
    
    # Group the DataFrame by spokesperson and sum the frequencies
    df = df.groupby('Spokesperson').sum().reset_index()
    
    # Sort the DataFrame by frequency in descending order
    df = df.sort_values('Frequency', ascending=False)
    
    return df

def main():
    st.title('Spokesperson Frequency App')
    
    # Get the input data from the user
    data = st.text_area('Enter the data:', height=200)
    
    if st.button('Process Data'):
        # Preprocess the data
        preprocessed_data = preprocess_data(data)
        
        # Process the preprocessed data
        df = process_data(preprocessed_data)
        
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
