"""
Edge case tests for the process_data function.
Tests unusual inputs, boundary conditions, and error scenarios.
"""
import pytest
import pandas as pd
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Metric_multi_entity_analysis import process_data


class TestEmptyAndWhitespaceInputs:
    """Test handling of empty and whitespace inputs"""

    def test_empty_string(self):
        """Test empty string input returns empty DataFrame"""
        data = ""
        result = process_data(data)

        assert len(result) == 0
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ['Entity', 'Volume']

    def test_whitespace_only(self):
        """Test whitespace-only input returns empty DataFrame"""
        data = "   \n  \n   "
        result = process_data(data)

        assert len(result) == 0

    def test_single_newline(self):
        """Test single newline returns empty DataFrame"""
        data = "\n"
        result = process_data(data)

        assert len(result) == 0

    def test_multiple_empty_lines(self):
        """Test multiple empty lines returns empty DataFrame"""
        data = "\n\n\n\n"
        result = process_data(data)

        assert len(result) == 0

    def test_empty_lines_between_entities(self):
        """Test that empty lines between entities are ignored"""
        data = "Entity A\n\n\nEntity B\n\nEntity C"
        result = process_data(data)

        assert len(result) == 3
        entities = result['Entity'].tolist()
        assert 'Entity A' in entities
        assert 'Entity B' in entities
        assert 'Entity C' in entities


class TestPipeDelimiterEdgeCases:
    """Test edge cases with pipe delimiter"""

    def test_only_pipes(self):
        """Test input with only pipe delimiters"""
        data = "|||"
        result = process_data(data)

        assert len(result) == 0

    def test_pipes_with_whitespace(self):
        """Test pipes with only whitespace between them"""
        data = "|  |   |"
        result = process_data(data)

        assert len(result) == 0

    def test_leading_pipe(self):
        """Test entity with leading pipe"""
        data = "|Entity A|Entity B"
        result = process_data(data)

        # Leading pipe creates empty string which should be filtered
        assert len(result) == 2
        entities = result['Entity'].tolist()
        assert 'Entity A' in entities
        assert 'Entity B' in entities

    def test_trailing_pipe(self):
        """Test entity with trailing pipe"""
        data = "Entity A|Entity B|"
        result = process_data(data)

        # Trailing pipe creates empty string which should be filtered
        assert len(result) == 2
        entities = result['Entity'].tolist()
        assert 'Entity A' in entities
        assert 'Entity B' in entities

    def test_consecutive_pipes(self):
        """Test consecutive pipes (empty entities)"""
        data = "Entity A||Entity B"
        result = process_data(data)

        # Double pipe creates empty string which should be filtered
        assert len(result) == 2
        entities = result['Entity'].tolist()
        assert 'Entity A' in entities
        assert 'Entity B' in entities


class TestSpecialCharacters:
    """Test handling of special characters in entity names"""

    def test_entity_with_apostrophe(self):
        """Test entity name with apostrophe"""
        data = "Entity's Name"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == "Entity's Name"

    def test_entity_with_ampersand(self):
        """Test entity name with ampersand"""
        data = "Entity & Co"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == "Entity & Co"

    def test_entity_with_hyphen(self):
        """Test entity name with hyphen"""
        data = "Entity-Name"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == "Entity-Name"

    def test_entity_with_underscore(self):
        """Test entity name with underscore"""
        data = "Entity_Name"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == "Entity_Name"

    def test_entity_with_parentheses(self):
        """Test entity name with parentheses"""
        data = "Entity (Name)"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == "Entity (Name)"

    def test_entity_with_quotes(self):
        """Test entity name with quotes"""
        data = 'Entity "Name"'
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity "Name"'

    def test_entity_with_unicode(self):
        """Test entity name with Unicode characters"""
        data = "Entité|实体|Сущность"
        result = process_data(data)

        assert len(result) == 3
        entities = result['Entity'].tolist()
        assert 'Entité' in entities
        assert '实体' in entities
        assert 'Сущность' in entities

    def test_entity_with_emoji(self):
        """Test entity name with emoji"""
        data = "Entity 🚀"
        result = process_data(data)

        assert len(result) == 1
        # The emoji might be treated as part of the entity or as a non-digit
        # depending on implementation


class TestVolumeEdgeCases:
    """Test edge cases related to volume numbers"""

    def test_zero_volume(self):
        """Test entity with zero volume"""
        data = "Entity A 0"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity A'
        assert result.iloc[0]['Volume'] == 0

    def test_negative_volume_treated_as_entity_name(self):
        """Test that negative number is treated as part of entity name"""
        data = "Entity -5"
        result = process_data(data)

        # -5 starts with minus, so isdigit() returns False
        # Should be treated as part of entity name
        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity -5'
        assert result.iloc[0]['Volume'] == 1

    def test_decimal_volume_treated_as_entity_name(self):
        """Test that decimal number is treated as part of entity name"""
        data = "Entity 1.5"
        result = process_data(data)

        # "1.5" contains a dot, so isdigit() returns False
        # Should be treated as part of entity name
        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity 1.5'
        assert result.iloc[0]['Volume'] == 1

    def test_multiple_spaces_before_volume(self):
        """Test entity with multiple spaces before volume"""
        data = "Entity Name    10"
        result = process_data(data)

        # Multiple spaces should be handled correctly by split()
        assert len(result) == 1
        assert result.iloc[0]['Entity'] == 'Entity Name'
        assert result.iloc[0]['Volume'] == 10

    def test_tab_separated_volume(self):
        """Test entity with tab before volume"""
        data = "Entity Name\t5"
        result = process_data(data)

        # Tab should be treated as whitespace
        assert len(result) == 1
        # Result might vary based on how tabs are handled


class TestCaseSensitivity:
    """Test case sensitivity in entity names"""

    def test_different_case_same_entity(self):
        """Test that entities with different cases are treated as different"""
        data = "Entity A\nentity a\nENTITY A"
        result = process_data(data)

        # Currently the code doesn't convert to lowercase despite the comment
        # So these should be 3 different entities
        assert len(result) == 3
        entities = result['Entity'].tolist()
        assert 'Entity A' in entities
        assert 'entity a' in entities
        assert 'ENTITY A' in entities

    def test_mixed_case_entity(self):
        """Test entity with mixed case"""
        data = "EnTiTy NaMe"
        result = process_data(data)

        assert len(result) == 1
        # Case should be preserved
        assert result.iloc[0]['Entity'] == 'EnTiTy NaMe'


class TestLongInputs:
    """Test handling of very long inputs"""

    def test_very_long_entity_name(self):
        """Test entity with very long name"""
        long_name = "A" * 500
        data = f"{long_name} 5"
        result = process_data(data)

        assert len(result) == 1
        assert result.iloc[0]['Entity'] == long_name
        assert result.iloc[0]['Volume'] == 5

    def test_many_entities_on_one_line(self):
        """Test many pipe-separated entities on one line"""
        entities = [f"Entity{i}" for i in range(100)]
        data = "|".join(entities)
        result = process_data(data)

        assert len(result) == 100

    def test_many_lines(self):
        """Test many lines of input"""
        lines = [f"Entity{i}" for i in range(1000)]
        data = "\n".join(lines)
        result = process_data(data)

        assert len(result) == 1000


class TestDataIntegrity:
    """Test data integrity in output"""

    def test_no_duplicate_entities_in_output(self):
        """Test that output has no duplicate entity names"""
        data = "Entity A\nEntity A\nEntity B\nEntity B"
        result = process_data(data)

        # Check no duplicates
        assert len(result) == 2
        assert len(result['Entity'].unique()) == 2

    def test_total_volume_preserved(self):
        """Test that total volume is preserved"""
        data = "Entity A 10\nEntity B 20\nEntity C 30"
        result = process_data(data)

        total_volume = result['Volume'].sum()
        assert total_volume == 60

    def test_no_null_values(self):
        """Test that there are no null values in output"""
        data = "Entity A|Entity B|Entity C 5"
        result = process_data(data)

        assert not result['Entity'].isnull().any()
        assert not result['Volume'].isnull().any()

    def test_volume_always_positive_or_zero(self):
        """Test that all volumes are non-negative integers"""
        data = "Entity A 5\nEntity B 0\nEntity C 100"
        result = process_data(data)

        assert all(result['Volume'] >= 0)
        assert all(result['Volume'].apply(lambda x: isinstance(x, (int, int))))
