#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from collections import defaultdict

st.title('Spokesperson Frequency Counter')

input_text = st.text_area("Enter spokespeople data", """
Ryan Truswel (Craft Beer Buyer, Asda), Michael Gleeson (CFO, Asda) 1
Unnamed Spokesperson, Carol (Customer trading manage, Asda) 3
""")

# Split the input by lines
lines = input_text.split('\n')

# Create a dictionary to hold the spokespeople and their frequencies
spokespeople_freq = defaultdict(int)

# Iterate over each line
for line in lines:
    # Split the line by ', ' to separate the spokespeople
    spokespeople_data = line.split(', ')

    # Get the frequency for this line
    freq = int(spokespeople_data[-1].split()[-1])

    # Remove the frequency from the list
    spokespeople_data = spokespeople_data[:-1]

    # Iterate over each spokesperson
    for spokesperson in spokespeople_data:
        # Add the frequency to the dictionary
        spokespeople_freq[spokesperson] += freq

# Display the spokespeople and their frequencies in a table
st.table(list(spokespeople_freq.items()))

# In[ ]:
