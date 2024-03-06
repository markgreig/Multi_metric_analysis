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
            # Split the spokesperson into name and values
            parts = spokesperson.strip().rsplit(None, 2)
            if len(parts) == 3 and parts[-1].isdigit() and parts[-2].isdigit():
                name = parts[0]
                frequency = int(parts[-2])
                reach = int(parts[-1])
            elif len(parts) == 2 and parts[-1].isdigit():
                name = parts[0]
                frequency = 1
                reach = int(parts[-1])
            else:
                name = spokesperson.strip()
                frequency = 1
                reach = 0
            
            # Add the spokesperson, frequency, and reach to the processed data
            processed_data.append((name, frequency, reach))
    
    # Create a DataFrame from the processed data
    df = pd.DataFrame(processed_data, columns=['Spokesperson', 'Frequency', 'Reach'])
    
    # Group the DataFrame by spokesperson and sum the frequencies and reaches
    df = df.groupby('Spokesperson').agg({'Frequency': 'sum', 'Reach': 'sum'}).reset_index()
    
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
