import pandas as pd
import sys
import os

# Add the parent directory to the Python path to import the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Metric_multi_entity_analysis import process_data

def test_simple_case():
    data = "Entity A | Entity B"
    df, warnings = process_data(data)
    assert len(df) == 2
    assert warnings == []
    assert df.iloc[0]['Entity'] == 'entity a'
    assert df.iloc[0]['Volume'] == 1
    assert df.iloc[1]['Entity'] == 'entity b'
    assert df.iloc[1]['Volume'] == 1

def test_with_volume():
    data = "Coke | Pepsi 5"
    df, warnings = process_data(data)
    assert len(df) == 2
    assert warnings == []
    # The order is not guaranteed, so we should check by entity name
    assert df.loc[df['Entity'] == 'coke', 'Volume'].iloc[0] == 5
    assert df.loc[df['Entity'] == 'pepsi', 'Volume'].iloc[0] == 5

def test_case_insensitivity():
    data = "Apple\napple"
    df, warnings = process_data(data)
    assert len(df) == 1
    assert warnings == []
    assert df.iloc[0]['Entity'] == 'apple'
    assert df.iloc[0]['Volume'] == 2

def test_entity_with_number():
    # 'Team 1' should be preserved as an entity if it's not the last one.
    data = "Team 1 | Solo"
    df, warnings = process_data(data)
    assert len(df) == 2
    assert warnings == []
    assert 'team 1' in df['Entity'].values
    assert 'solo' in df['Entity'].values
    assert df.loc[df['Entity'] == 'team 1', 'Volume'].iloc[0] == 1
    assert df.loc[df['Entity'] == 'solo', 'Volume'].iloc[0] == 1


def test_entity_with_number_at_end():
    # This tests the ambiguous case documented in the instructions.
    # 'Team 1' will be parsed as entity 'team' and volume 1.
    data = "Solo | Team 1"
    df, warnings = process_data(data)
    assert len(df) == 2
    assert warnings == []
    assert 'solo' in df['Entity'].values
    assert 'team' in df['Entity'].values
    assert df.loc[df['Entity'] == 'solo', 'Volume'].iloc[0] == 1
    assert df.loc[df['Entity'] == 'team', 'Volume'].iloc[0] == 1

def test_empty_input():
    data = ""
    df, warnings = process_data(data)
    assert df.empty
    assert warnings == []

def test_blank_lines():
    data = "\n\nEntity A\n\nEntity B\n"
    df, warnings = process_data(data)
    assert len(df) == 2
    assert warnings == []

def test_malformed_volume():
    data = "Entity A | Entity B 5x"
    df, warnings = process_data(data)
    assert len(df) == 2
    assert len(warnings) == 1
    assert "Could not parse volume" in warnings[0]
    # Volume should default to 1 for all entities on that line
    assert df['Volume'].sum() == 2

def test_volume_with_single_entity():
    data = "Entity A 10"
    df, warnings = process_data(data)
    assert len(df) == 1
    assert warnings == []
    assert df.iloc[0]['Entity'] == 'entity a'
    assert df.iloc[0]['Volume'] == 10
