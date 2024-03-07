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
    
    # Create a dictionary to store the spokesperson names and their corresponding job titles
    metric_dict = {}
    
    # Process each row
    for row in rows:
        # Split the row into spokespeople
        metrics = row.split('|')
        
        # Process each spokesperson
        for metric in metrics:
            # Split the spokesperson into name and frequency
            parts = metric.strip().split()
            if len(parts) > 1 and parts[-1].isdigit():
                name = ' '.join(parts[:-1])
                volume = int(parts[-1])
            else:
                name = ' '.join(parts)
                volume = 1
            
            # Add the spokesperson and frequency to the processed data if the name is not blank
            if name.strip():
                processed_data.append((name, volume))
                
                # Check if the spokesperson name already exists in the dictionary
                first_two_words = ' '.join(name.split()[:2])
                if first_two_words in metric_dict:
                    # Check if the job title matches the existing job title
                    existing_job_title = metric_dict[first_two_words]
                    current_job_title = ' '.join(name.split()[2:])
                    if current_job_title != existing_job_title:
                        processed_data.append((f"Warning: Potential duplicate for '{first_two_words}'", 0))
                else:
                    # Add the spokesperson name and job title to the dictionary
                    metric_dict[first_two_words] = ' '.join(name.split()[2:])
    
    # Create a DataFrame from the processed data
    df = pd.DataFrame(processed_data, columns=['Metric', 'Volume'])
    
    # Group the DataFrame by spokesperson and sum the frequencies
    df = df.groupby('Metric').sum().reset_index()
    
    # Sort the DataFrame by frequency in descending order
    df = df.sort_values('Volume', ascending=False)
    
    return df

def main():
    st.title('Metric Volume Discovery Tool')
    
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
            file_name='metric_volume.csv',
            mime='text/csv'
        )

if __name__ == '__main__':
    main()
# In[ ]: