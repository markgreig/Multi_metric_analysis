"""
Unit tests for the process_data function - basic functionality tests.
Tests core parsing, aggregation, and sorting functionality.
"""
import pytest
import pandas as pd
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Metric_multi_entity_analysis import process_data


class TestBasicFunctionality:
    """Test basic functionality of process_data function"""

    def test_single_entity_without_volume(self):
        """Test single entity defaults to volume of 1"""
        data = "Entity A"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity A'
        assert result.iloc[0]['Volume'] == 1

    def test_single_entity_with_explicit_volume(self):
        """Test single entity with explicit volume at end"""
        data = "Entity A 5"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity A'
        assert result.iloc[0]['Volume'] == 5

    def test_multiple_entities_one_line_pipe_separated(self):
        """Test multiple entities on one line separated by pipes"""
        data = "Entity A|Entity B|Entity C"
        result = process_data(data)

        assert len(result) == 3
        entities = result['Entity'].tolist()
        assert 'Entity A' in entities
        assert 'Entity B' in entities
        assert 'Entity C' in entities
        # All should have volume 1
        assert all(result['Volume'] == 1)

    def test_multiple_lines_different_entities(self):
        """Test multiple lines with different entities"""
        data = "Entity A\nEntity B\nEntity C"
        result = process_data(data)

        assert len(result) == 3
        entities = result['Entity'].tolist()
        assert 'Entity A' in entities
        assert 'Entity B' in entities
        assert 'Entity C' in entities

    def test_aggregation_of_duplicate_entities(self):
        """Test that duplicate entities are aggregated"""
        data = "Entity A\nEntity A\nEntity B"
        result = process_data(data)

        assert len(result) == 2
        entity_a = result[result['Entity'] == 'Entity A']
        entity_b = result[result['Entity'] == 'Entity B']

        assert entity_a.iloc[0]['Volume'] == 2
        assert entity_b.iloc[0]['Volume'] == 1

    def test_volume_summation_for_same_entity(self):
        """Test that volumes are summed for same entity appearing multiple times"""
        data = "Entity A 3\nEntity A 5\nEntity B 2"
        result = process_data(data)

        assert len(result) == 2
        entity_a = result[result['Entity'] == 'Entity A']
        entity_b = result[result['Entity'] == 'Entity B']

        assert entity_a.iloc[0]['Volume'] == 8  # 3 + 5
        assert entity_b.iloc[0]['Volume'] == 2

    def test_pipe_delimited_with_volumes(self):
        """Test pipe-delimited entities where last entity has volume"""
        data = "Entity A|Entity B|Entity C 10"
        result = process_data(data)

        # All three entities should have volume 10 (volume applies to the row)
        assert len(result) == 3
        assert all(result['Volume'] == 10)

    def test_sorting_descending_by_volume(self):
        """Test that results are sorted by volume in descending order"""
        data = "Entity A 5\nEntity B 10\nEntity C 3"
        result = process_data(data)

        assert result.iloc[0]['Entity'] == 'Entity B'  # Highest volume
        assert result.iloc[0]['Volume'] == 10
        assert result.iloc[1]['Entity'] == 'Entity A'
        assert result.iloc[1]['Volume'] == 5
        assert result.iloc[2]['Entity'] == 'Entity C'  # Lowest volume
        assert result.iloc[2]['Volume'] == 3

    def test_dataframe_structure(self):
        """Test that returned DataFrame has correct structure"""
        data = "Entity A"
        result = process_data(data)

        # Check it's a DataFrame
        assert isinstance(result, pd.DataFrame)

        # Check column names
        assert list(result.columns) == ['Entity', 'Volume']

        # Check data types
        assert result['Entity'].dtype == object  # String type
        assert result['Volume'].dtype in [int, 'int64', 'int32']  # Integer type

    def test_whitespace_handling(self):
        """Test that leading/trailing whitespace is stripped"""
        data = "  Entity A  |  Entity B  "
        result = process_data(data)

        assert len(result) == 2
        entities = result['Entity'].tolist()
        assert 'Entity A' in entities
        assert 'Entity B' in entities
        # Verify no whitespace around names
        assert '  Entity A  ' not in entities

    def test_complex_multiline_with_pipes_and_volumes(self):
        """Test realistic complex input with multiple lines, pipes, and volumes"""
        data = """Entity A|Entity B|Entity C 5
Entity A|Entity D 3
Entity B|Entity E"""
        result = process_data(data)

        # Entity A: 5 + 3 = 8
        # Entity B: 5 + 1 = 6
        # Entity C: 5
        # Entity D: 3
        # Entity E: 1
        assert len(result) == 5

        entity_a = result[result['Entity'] == 'Entity A']
        assert entity_a.iloc[0]['Volume'] == 8

        entity_b = result[result['Entity'] == 'Entity B']
        assert entity_b.iloc[0]['Volume'] == 6

        entity_c = result[result['Entity'] == 'Entity C']
        assert entity_c.iloc[0]['Volume'] == 5


class TestVolumeDetection:
    """Test volume detection logic specifically"""

    def test_volume_with_multiple_words_in_entity(self):
        """Test entity with multiple words and volume at end"""
        data = "Entity Name Here 7"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity Name Here'
        assert result.iloc[0]['Volume'] == 7

    def test_no_volume_when_number_not_separated(self):
        """Test that number without space is part of entity name"""
        data = "Entity5"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity5'
        assert result.iloc[0]['Volume'] == 1  # Default volume

    def test_large_volume_number(self):
        """Test handling of large volume numbers"""
        data = "Entity A 999999"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Volume'] == 999999

    def test_single_digit_volume(self):
        """Test single digit volume"""
        data = "Entity A 1"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Volume'] == 1
