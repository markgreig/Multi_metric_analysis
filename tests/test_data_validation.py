"""
Data validation tests for the process_data function.
Tests data format validation, error handling, and malformed inputs.
"""
import pytest
import pandas as pd
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Metric_multi_entity_analysis import process_data


class TestMalformedInput:
    """Test handling of malformed or unusual input formats"""

    def test_only_volume_number(self):
        """Test input with only a number (no entity name)"""
        data = "5"
        result = process_data(data)

        # A single number should be treated as entity name since it's not in format "name number"
        assert len(result) == 1
        assert result.iloc[0]['Entity'] == '5'
        assert result.iloc[0]['Volume'] == 1

    def test_multiple_numbers_at_end(self):
        """Test entity with multiple numbers at end"""
        data = "Entity 5 10"
        result = process_data(data)

        # Last number (10) should be volume, "Entity 5" should be entity name
        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity 5'
        assert result.iloc[0]['Volume'] == 10

    def test_number_in_middle_of_entity_name(self):
        """Test entity with number in the middle of name"""
        data = "Entity 123 Name"
        result = process_data(data)

        # "Name" is not a digit, so no volume extraction
        # Entire string should be entity name
        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity 123 Name'
        assert result.iloc[0]['Volume'] == 1

    def test_alphanumeric_last_word(self):
        """Test entity ending with alphanumeric (not pure digit)"""
        data = "Entity ABC123"
        result = process_data(data)

        # ABC123 is not all digits, so should be part of entity name
        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity ABC123'
        assert result.iloc[0]['Volume'] == 1

    def test_entity_ending_with_number_no_space(self):
        """Test entity name ending with number but no space before it"""
        data = "Entity123"
        result = process_data(data)

        # No space means it's part of the entity name
        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity123'
        assert result.iloc[0]['Volume'] == 1


class TestVolumeParsingRobustness:
    """Test robustness of volume parsing logic"""

    def test_very_large_volume(self):
        """Test handling of very large volume numbers"""
        data = "Entity A 999999999999"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Volume'] == 999999999999

    def test_scientific_notation_treated_as_name(self):
        """Test that scientific notation is treated as part of name"""
        data = "Entity 1e5"
        result = process_data(data)

        # "1e5" contains 'e', so isdigit() returns False
        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity 1e5'
        assert result.iloc[0]['Volume'] == 1

    def test_hexadecimal_treated_as_name(self):
        """Test that hexadecimal numbers are treated as part of name"""
        data = "Entity 0xFF"
        result = process_data(data)

        # "0xFF" contains 'x' and 'F', so isdigit() returns False
        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity 0xFF'
        assert result.iloc[0]['Volume'] == 1


class TestOutputValidation:
    """Test that output always meets expected format and constraints"""

    def test_columns_always_present(self):
        """Test that output always has Entity and Volume columns"""
        test_cases = [
            "",
            "Entity A",
            "Entity A|Entity B",
            "Entity A\nEntity B",
        ]

        for data in test_cases:
            result = process_data(data)
            assert 'Entity' in result.columns
            assert 'Volume' in result.columns
            assert len(result.columns) == 2

    def test_volume_always_integer(self):
        """Test that Volume column is always integer type"""
        data = "Entity A 5\nEntity B 10"
        result = process_data(data)

        assert result['Volume'].dtype in ['int64', 'int32', 'int']

    def test_entity_always_string(self):
        """Test that Entity column is always string/object type"""
        data = "Entity A\nEntity B"
        result = process_data(data)

        assert result['Entity'].dtype == object

    def test_output_is_dataframe(self):
        """Test that output is always a pandas DataFrame"""
        test_cases = [
            "",
            "Entity A",
            "Entity A|Entity B",
        ]

        for data in test_cases:
            result = process_data(data)
            assert isinstance(result, pd.DataFrame)

    def test_sorting_is_stable(self):
        """Test that sorting is stable and consistent"""
        data = "Entity A 10\nEntity B 5\nEntity C 10"
        result = process_data(data)

        # First row should have volume 10 (highest)
        assert result.iloc[0]['Volume'] == 10
        # Last row should have volume 5 (lowest)
        assert result.iloc[2]['Volume'] == 5

    def test_index_is_reset(self):
        """Test that DataFrame index is reset (starts at 0)"""
        data = "Entity C\nEntity A\nEntity B"
        result = process_data(data)

        # Check index is 0, 1, 2 (not the original groupby index)
        assert list(result.index) == [0, 1, 2]


class TestRealWorldScenarios:
    """Test realistic real-world data scenarios"""

    def test_csv_like_input(self):
        """Test CSV-like input data"""
        data = "Entity A, Entity B, Entity C"
        result = process_data(data)

        # Commas are not delimiters, so this is one entity
        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity A, Entity B, Entity C'

    def test_mixed_delimiters(self):
        """Test input with both pipes and commas"""
        data = "Entity A|Entity B, Name|Entity C"
        result = process_data(data)

        # Only pipes are delimiters
        assert len(result) == 3
        entities = result['Entity'].tolist()
        assert 'Entity A' in entities
        assert 'Entity B, Name' in entities
        assert 'Entity C' in entities

    def test_entities_with_numbers_in_names(self):
        """Test realistic entities that contain numbers"""
        data = "Team 1|Team 2|Team 3 5"
        result = process_data(data)

        # All three teams with volume 5
        assert len(result) == 3
        assert all(result['Volume'] == 5)
        entities = result['Entity'].tolist()
        assert 'Team 1' in entities
        assert 'Team 2' in entities
        assert 'Team 3' in entities

    def test_company_names_with_special_chars(self):
        """Test realistic company names with special characters"""
        data = "ABC Corp|XYZ Inc.|Smith & Sons|O'Reilly Media 10"
        result = process_data(data)

        assert len(result) == 4
        entities = result['Entity'].tolist()
        assert 'ABC Corp' in entities
        assert 'XYZ Inc.' in entities
        assert 'Smith & Sons' in entities
        assert "O'Reilly Media" in entities
        assert all(result['Volume'] == 10)

    def test_name_with_parenthetical(self):
        """Test entity names with parenthetical information"""
        data = "Entity A (Primary)|Entity B (Secondary) 3"
        result = process_data(data)

        assert len(result) == 2
        entities = result['Entity'].tolist()
        assert 'Entity A (Primary)' in entities
        assert 'Entity B (Secondary)' in entities

    def test_repeated_processing_same_result(self):
        """Test that processing same data twice gives same result"""
        data = "Entity A|Entity B|Entity C 5"

        result1 = process_data(data)
        result2 = process_data(data)

        # Results should be identical
        pd.testing.assert_frame_equal(result1, result2)


class TestConsistency:
    """Test consistency of behavior across different inputs"""

    def test_pipe_vs_newline_same_entities(self):
        """Test that pipes and newlines produce same aggregation"""
        data_pipes = "Entity A|Entity A|Entity B"
        data_newlines = "Entity A\nEntity A\nEntity B"

        result_pipes = process_data(data_pipes)
        result_newlines = process_data(data_newlines)

        # Both should have same entities and volumes
        assert len(result_pipes) == len(result_newlines) == 2

        # Sort both by entity name for comparison
        result_pipes_sorted = result_pipes.sort_values('Entity').reset_index(drop=True)
        result_newlines_sorted = result_newlines.sort_values('Entity').reset_index(drop=True)

        pd.testing.assert_frame_equal(result_pipes_sorted, result_newlines_sorted)

    def test_whitespace_normalization(self):
        """Test that different whitespace is normalized consistently"""
        test_cases = [
            "Entity A",
            " Entity A ",
            "  Entity A  ",
            "\tEntity A\t",
        ]

        results = [process_data(data) for data in test_cases]

        # All should produce same entity name
        for result in results:
            assert result.iloc[0]['Entity'] == 'Entity A'
            assert result.iloc[0]['Volume'] == 1
