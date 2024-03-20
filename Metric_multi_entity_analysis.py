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
        metrics = row.split('|')
        
        # Check if the last part of the row is a frequency
        last_part = metrics[-1].strip().split()
        if len(last_part) > 1 and last_part[-1].isdigit():
            volume = int(last_part[-1])
            metrics[-1] = ' '.join(last_part[:-1])
        else:
            volume = 1
        
        # Process each spokesperson
        for metric in metrics:
            name = metric.strip()  # Convert the name to lowercase
            
            # Add the spokesperson and frequency to the processed data if the name is not blank
            if name:
                processed_data.append((name, volume))
    
    # Create a DataFrame from the processed data
    df = pd.DataFrame(processed_data, columns=['Entity', 'Volume'])
    
    # Group the DataFrame by spokesperson and sum the frequencies
    df = df.groupby('Entity').sum().reset_index()
    
    # Sort the DataFrame by frequency in descending order
    df = df.sort_values('Volume', ascending=False)
    
    return df

def main():
    st.title('Metric Entity Volume Analyser')
    
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
            file_name='metric_entity_volume.csv',
            mime='text/csv'
        )

if __name__ == '__main__':
    main()
# In[ ]:
