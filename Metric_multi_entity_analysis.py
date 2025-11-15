#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import io

def process_data(data):
    """
    Process pipe-delimited entity data with optional volume counts.

    Parses input text to extract entity names and their volumes, aggregates
    duplicate entities, and returns a sorted DataFrame.

    Args:
        data (str): Input text with entities separated by pipes (|) or newlines.
                   Optional volume can be specified as the last number on a line.
                   Format: "Entity A|Entity B|Entity C 5" where 5 is the volume
                   for all entities on that line.

    Returns:
        pd.DataFrame: DataFrame with columns ['Entity', 'Volume'], sorted by
                     volume in descending order. Duplicate entities are aggregated
                     with their volumes summed.

    Examples:
        >>> process_data("Entity A|Entity B 5")
        # Returns DataFrame with Entity A and Entity B, both with volume 5

        >>> process_data("Entity A\\nEntity A 3")
        # Returns DataFrame with Entity A having volume 4 (1 + 3)
    """
    # Split the data into rows
    rows = data.split('\n')

    # Create a list to store the processed data
    processed_data = []

    # Process each row
    for row in rows:
        # Skip empty rows
        if not row.strip():
            continue

        # Split the row into entities
        metrics = row.split('|')

        # Check if the last part of the row contains a volume number
        # Input validation to prevent crashes on malformed data
        try:
            last_part = metrics[-1].strip().split()
            if len(last_part) > 1 and last_part[-1].isdigit():
                volume = int(last_part[-1])
                metrics[-1] = ' '.join(last_part[:-1])
            else:
                volume = 1
        except (IndexError, ValueError):
            # If parsing fails, default to volume of 1
            volume = 1

        # Process each entity
        for metric in metrics:
            name = metric.strip()

            # Add the entity and volume to the processed data if the name is not blank
            if name:
                processed_data.append((name, volume))

    # Create a DataFrame from the processed data
    df = pd.DataFrame(processed_data, columns=['Entity', 'Volume'])

    # Group the DataFrame by entity and sum the volumes
    df = df.groupby('Entity').sum().reset_index()

    # Sort the DataFrame by volume in descending order
    df = df.sort_values('Volume', ascending=False)

    return df

def main():
    """
    Main Streamlit application for the Metric Entity Volume Analyser.

    Creates a web interface that allows users to:
    1. Enter pipe-delimited entity data with optional volumes
    2. Process the data to aggregate and sort entities
    3. View a preview of the processed data
    4. Download the results as a CSV file

    The interface includes:
    - Text area for data input
    - Process button to trigger data processing
    - DataFrame preview of results
    - CSV download button

    This function is the entry point for the Streamlit application.
    """
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
