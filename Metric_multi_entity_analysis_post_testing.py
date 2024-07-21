#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import io

def process_data(data):
    # Split the data into rows
    rows = data.split('\n')
    
    # Create an OrderedDict to store the processed data
    processed_data = OrderedDict()
    
    # Process each row
    for row in rows:
        # Split the row into metrics
        metrics = row.split('|')
        
        # Process each metric
        for metric in metrics:
            parts = metric.strip().split()
            if parts:
                if len(parts) > 1 and parts[-1].isdigit():
                    name = ' '.join(parts[:-1])
                    volume = int(parts[-1])
                else:
                    name = ' '.join(parts)
                    volume = 1
                
                # Add or update the metric and volume in the processed data
                if name in processed_data:
                    processed_data[name] += volume
                else:
                    processed_data[name] = volume
    
    # Create a DataFrame from the processed data
    df = pd.DataFrame(list(processed_data.items()), columns=['Entity', 'Volume'])
    
    # Sort the DataFrame by volume in descending order, then by entity alphabetically
    df = df.sort_values(['Volume', 'Entity'], ascending=[False, True]).reset_index(drop=True)
    
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
