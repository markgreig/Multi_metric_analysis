#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import re
from collections import defaultdict

st.title('Spokesperson Frequency Counter')

input_text = st.text_area("Enter spokespeople data")

# Split the input by lines
lines = input_text.split('\n')

# Create a dictionary to hold the spokespeople and their frequencies
spokespeople_freq = defaultdict(int)

# Iterate over each line
for line in lines:
    # Split the line by ', ' or '|'
    parts = re.split(r'[,|]\s*', line)

    # Merge any parts that end with '(' with the next part
    i = 0
    while i < len(parts) - 1:
        if parts[i].endswith('('):
            parts[i] += parts[i+1]
            del parts[i+1]
        else:
            i += 1

    # Check if the line has a frequency
    if len(parts) > 0 and ' ' in parts[-1]:
        # Get the frequency for this line
        freq = int(parts[-1].split()[-1])

        # Remove the frequency from the list
        parts = parts[:-1]

        # Iterate over each spokesperson
        for spokesperson in parts:
            # Add the frequency to the dictionary
            spokespeople_freq[spokesperson] += freq

# Display the spokespeople and their frequencies in a table
st.table(list(spokespeople_freq.items()))
# In[ ]:
