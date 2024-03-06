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
        
        # Get the reach value from the last spokesperson in the row
        last_spokesperson = spokespeople[-1].strip().split()
        if len(last_spokesperson) > 1 and last_spokesperson[-1].isdigit():
            reach = int(last_spokesperson[-1])
        else:
            reach = 0
        
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
            
            # Add the spokesperson, frequency, and reach to the processed data
            processed_data.append((name, frequency, reach))
    
    # Create a DataFrame from the processed data
    df = pd.DataFrame(processed_data, columns=['Spokesperson', 'Frequency', 'Reach'])
    
    # Group the DataFrame by spokesperson and sum the frequencies and reaches
    df = df.groupby('Spokesperson').agg({'Frequency': 'sum', 'Reach': 'sum'}).reset_index()
    
    # Sort the DataFrame by frequency in descending order and then by reach in descending order
    df = df.sort_values(['Frequency', 'Reach'], ascending=[False, False])
    
    return df

def main():
    st.title('Spokesperson Frequency and Reach App')
    
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
            file_name='spokesperson_frequency_reach.csv',
            mime='text/csv'
        )

if __name__ == '__main__':
    main()
# In[ ]:
