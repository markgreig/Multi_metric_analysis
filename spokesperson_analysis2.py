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
            # Split the spokesperson into name, job title, and frequency
            parts = spokesperson.strip().split(' - ')
            if len(parts) > 1:
                name_and_frequency = parts[0].strip().split()
                if len(name_and_frequency) > 1 and name_and_frequency[-1].isdigit():
                    name = ' '.join(name_and_frequency[:-1])
                    frequency = int(name_and_frequency[-1])
                else:
                    name = ' '.join(name_and_frequency)
                    frequency = 1
                job_title = parts[1].strip()
            else:
                name_and_frequency = parts[0].strip().split()
                if len(name_and_frequency) > 1 and name_and_frequency[-1].isdigit():
                    name = ' '.join(name_and_frequency[:-1])
                    frequency = int(name_and_frequency[-1])
                else:
                    name = ' '.join(name_and_frequency)
                    frequency = 1
                job_title = ''
            
            # Check if the spokesperson already exists in the preprocessed data
            if name in preprocessed_data:
                # If the spokesperson exists, update the frequency and job title (if empty)
                preprocessed_data[name]['frequency'] += frequency
                if not preprocessed_data[name]['job_title']:
                    preprocessed_data[name]['job_title'] = job_title
            else:
                # If the spokesperson doesn't exist, add them to the preprocessed data
                preprocessed_data[name] = {'frequency': frequency, 'job_title': job_title}
    
    # Create a new data string with the preprocessed data
    preprocessed_data_string = ''
    for name, data in preprocessed_data.items():
        preprocessed_data_string += f"{name} {data['frequency']} - {data['job_title']}\n"
    
    return preprocessed_data_string

def process_data(data):
    # Split the data into rows
    rows = data.split('\n')
    
    # Create a list to store the processed data
    processed_data = []
    
    # Process each row
    for row in rows:
        # Split the row into spokesperson, frequency, and job title
        parts = row.strip().split(' - ')
        if len(parts) > 1:
            name_and_frequency = parts[0].strip().split()
            if len(name_and_frequency) > 1 and name_and_frequency[-1].isdigit():
                name = ' '.join(name_and_frequency[:-1])
                frequency = int(name_and_frequency[-1])
            else:
                name = ' '.join(name_and_frequency)
                frequency = 1
            job_title = parts[1].strip()
        else:
            name_and_frequency = parts[0].strip().split()
            if len(name_and_frequency) > 1 and name_and_frequency[-1].isdigit():
                name = ' '.join(name_and_frequency[:-1])
                frequency = int(name_and_frequency[-1])
            else:
                name = ' '.join(name_and_frequency)
                frequency = 1
            job_title = ''
        
        # Add the spokesperson, frequency, and job title to the processed data if the name is not blank
        if name.strip():
            processed_data.append((name, frequency, job_title))
            
   # Create a DataFrame from the processed data
    df = pd.DataFrame(processed_data, columns=['Spokesperson', 'Frequency', 'Job Title'])
    
    # Group the DataFrame by spokesperson and sum the frequencies
    df = df.groupby(['Spokesperson', 'Job Title']).sum().reset_index()
    
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
