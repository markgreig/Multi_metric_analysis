#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import streamlit as st
import pandas as pd

st.title('My App')

# Function to clean and process the clipboard data
def process_clipboard_data(clipboard_data):
    # Split the clipboard data into lines
    lines = clipboard_data.strip().split('\n')

    # Initialize a list to store cleaned and split data
    cleaned_data = []

    # Regular expression pattern to match spokesperson and frequency
    pattern = r'(.+?)\s+(\d+)'

    for line in lines:
        match = re.match(pattern, line)
        if match:
            spokesperson = match.group(1)
            frequency = int(match.group(2))

            # Append each cleaned entry to the list
            cleaned_data.append([spokesperson, frequency])

    # Create a DataFrame from the cleaned data
    df = pd.DataFrame(cleaned_data, columns=['Spokesperson', 'Frequency'])

    return df

# Get the text from the clipboard
text = st.text_input("Paste text here")

# Process clipboard data
if text:
    df = process_clipboard_data(text)

    # Sort by Frequency in descending order
    result = df.sort_values(by='Frequency', ascending=False)

    st.write(result)

    # Provide a download link for the data as CSV
    @st.cache
    def convert_df(result):
        return result.to_csv(index=False).encode('utf-8')

    csv = convert_df(result)

    st.download_button(
         label="Download data as CSV",
         data=csv,
         file_name='top_spokespeople.csv',
         mime='text/csv',
     )
# In[ ]:
