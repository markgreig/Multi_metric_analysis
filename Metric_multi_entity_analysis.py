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
    warnings = []
    
    # Process each row
    for i, row in enumerate(rows):
        if not row.strip():
            continue

        metrics = row.split('|')
        
        # Check if the last part of the row is a frequency
        last_metric = metrics[-1].strip()
        parts = last_metric.split()
        volume = 1

        if len(parts) > 1:
            last_word = parts[-1]
            try:
                volume = int(last_word)
                metrics[-1] = ' '.join(parts[:-1])
            except ValueError:
                # It's not a valid integer, so treat it as part of the name.
                # Reset volume to 1.
                volume = 1
                # Only issue a warning if it looks like a malformed number.
                if any(char.isdigit() for char in last_word):
                    warnings.append(f"Row {i+1}: Could not parse volume from '{last_word}'. Treating as part of the entity name and volume as 1.")
        
        # Process each spokesperson
        for metric in metrics:
            name = metric.strip().lower()  # Convert the name to lowercase
            
            # Add the spokesperson and frequency to the processed data if the name is not blank
            if name:
                processed_data.append((name, volume))
    
    if not processed_data:
        return pd.DataFrame(columns=['Entity', 'Volume']), warnings

    # Create a DataFrame from the processed data
    df = pd.DataFrame(processed_data, columns=['Entity', 'Volume'])
    
    # Group the DataFrame by spokesperson and sum the frequencies
    df = df.groupby('Entity').sum().reset_index()
    
    # Sort the DataFrame by frequency in descending order
    df = df.sort_values('Volume', ascending=False)
    
    return df, warnings

def main():
    st.title('Metric Entity Volume Analyser')
    
    st.info("""
    **Instructions:**
    - Enter your data in the text area below.
    - Each line represents a record.
    - Use a `|` to separate multiple entities on the same line (e.g., `Entity A | Entity B`).
    - To specify a volume for all entities on a line, add a number at the end of the line (e.g., `Entity A | Entity B 5`).
    - If an entity name ends with a number (e.g., `Team 1`), ensure it is not the last entity on the line to avoid it being mistaken for a volume count. For example, write `Team 1 | Other Entity` instead of `Other Entity | Team 1`.
    """)

    # Get the input data from the user
    data = st.text_area('Enter the data:', height=200)
    
    if st.button('Process Data'):
        # Process the data
        df, warnings = process_data(data)

        # Display any warnings
        for warning in warnings:
            st.warning(warning)
        
        # Display the preview of the CSV file
        st.subheader('Preview of CSV file:')
        st.write(df)
        
        if not df.empty:
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
