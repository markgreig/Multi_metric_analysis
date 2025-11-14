"""
Integration tests for Streamlit UI components.
Tests the main() function and user interface behavior.
Note: These tests use unittest.mock to simulate Streamlit components.
"""
import pytest
import pandas as pd
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestStreamlitUI:
    """Test Streamlit UI components and main function"""

    @patch('Metric_multi_entity_analysis.st')
    def test_main_displays_title(self, mock_st):
        """Test that main() displays the correct title"""
        from Metric_multi_entity_analysis import main

        # Mock the text_area to return empty string
        mock_st.text_area.return_value = ""
        mock_st.button.return_value = False

        main()

        # Check that title was called with correct text
        mock_st.title.assert_called_once_with('Metric Entity Volume Analyser')

    @patch('Metric_multi_entity_analysis.st')
    def test_main_creates_text_area(self, mock_st):
        """Test that main() creates text area for input"""
        from Metric_multi_entity_analysis import main

        mock_st.text_area.return_value = ""
        mock_st.button.return_value = False

        main()

        # Check that text_area was called with correct parameters
        mock_st.text_area.assert_called_once_with('Enter the data:', height=200)

    @patch('Metric_multi_entity_analysis.st')
    def test_main_creates_process_button(self, mock_st):
        """Test that main() creates process button"""
        from Metric_multi_entity_analysis import main

        mock_st.text_area.return_value = ""
        mock_st.button.return_value = False

        main()

        # Check that button was called
        mock_st.button.assert_called_once_with('Process Data')

    @patch('Metric_multi_entity_analysis.st')
    def test_main_processes_data_when_button_clicked(self, mock_st):
        """Test that data is processed when button is clicked"""
        from Metric_multi_entity_analysis import main

        # Mock user input
        test_data = "Entity A|Entity B 5"
        mock_st.text_area.return_value = test_data
        mock_st.button.return_value = True  # Button clicked

        main()

        # Check that subheader and write were called (results displayed)
        mock_st.subheader.assert_called_once_with('Preview of CSV file:')
        assert mock_st.write.called

    @patch('Metric_multi_entity_analysis.st')
    def test_main_displays_dataframe(self, mock_st):
        """Test that processed DataFrame is displayed"""
        from Metric_multi_entity_analysis import main

        test_data = "Entity A 10\nEntity B 5"
        mock_st.text_area.return_value = test_data
        mock_st.button.return_value = True

        main()

        # Get the DataFrame that was passed to st.write()
        write_call_args = mock_st.write.call_args
        df_displayed = write_call_args[0][0]

        # Check it's a DataFrame
        assert isinstance(df_displayed, pd.DataFrame)
        # Check it has correct data
        assert len(df_displayed) == 2
        assert 'Entity' in df_displayed.columns
        assert 'Volume' in df_displayed.columns

    @patch('Metric_multi_entity_analysis.st')
    def test_main_creates_download_button(self, mock_st):
        """Test that download button is created with correct CSV"""
        from Metric_multi_entity_analysis import main

        test_data = "Entity A 10"
        mock_st.text_area.return_value = test_data
        mock_st.button.return_value = True

        main()

        # Check that download_button was called
        assert mock_st.download_button.called

        # Get the call arguments
        call_kwargs = mock_st.download_button.call_args[1]

        # Check parameters
        assert call_kwargs['label'] == 'Download CSV'
        assert call_kwargs['file_name'] == 'metric_entity_volume.csv'
        assert call_kwargs['mime'] == 'text/csv'

        # Check CSV data is valid
        csv_data = call_kwargs['data']
        assert 'Entity,Volume' in csv_data
        assert 'Entity A,10' in csv_data

    @patch('Metric_multi_entity_analysis.st')
    def test_main_csv_format_correct(self, mock_st):
        """Test that CSV output has correct format"""
        from Metric_multi_entity_analysis import main

        test_data = "Entity A|Entity B 5"
        mock_st.text_area.return_value = test_data
        mock_st.button.return_value = True

        main()

        # Get CSV data from download_button call
        call_kwargs = mock_st.download_button.call_args[1]
        csv_data = call_kwargs['data']

        # Check CSV structure
        lines = csv_data.strip().split('\n')
        assert lines[0] == 'Entity,Volume'  # Header
        assert len(lines) >= 2  # Header + at least one data row

        # Check no index column
        assert not any(line.startswith(',') for line in lines)

    @patch('Metric_multi_entity_analysis.st')
    def test_main_no_processing_without_button_click(self, mock_st):
        """Test that data is not processed if button is not clicked"""
        from Metric_multi_entity_analysis import main

        test_data = "Entity A|Entity B"
        mock_st.text_area.return_value = test_data
        mock_st.button.return_value = False  # Button not clicked

        main()

        # st.write and download_button should not be called
        mock_st.write.assert_not_called()
        mock_st.download_button.assert_not_called()

    @patch('Metric_multi_entity_analysis.st')
    def test_main_handles_empty_input(self, mock_st):
        """Test that main handles empty input gracefully"""
        from Metric_multi_entity_analysis import main

        mock_st.text_area.return_value = ""
        mock_st.button.return_value = True  # Button clicked but no data

        main()

        # Should still display results (empty DataFrame)
        assert mock_st.write.called

        # Get the DataFrame
        df_displayed = mock_st.write.call_args[0][0]
        assert len(df_displayed) == 0

    @patch('Metric_multi_entity_analysis.st')
    def test_main_handles_complex_input(self, mock_st):
        """Test that main handles complex realistic input"""
        from Metric_multi_entity_analysis import main

        test_data = """Entity A|Entity B|Entity C 10
Entity A|Entity D 5
Entity E"""
        mock_st.text_area.return_value = test_data
        mock_st.button.return_value = True

        main()

        # Get displayed DataFrame
        df_displayed = mock_st.write.call_args[0][0]

        # Check correct number of unique entities
        assert len(df_displayed) == 5

        # Check Entity A has aggregated volume (10 + 5 = 15)
        entity_a = df_displayed[df_displayed['Entity'] == 'Entity A']
        assert len(entity_a) == 1
        assert entity_a.iloc[0]['Volume'] == 15


class TestCSVExport:
    """Test CSV export functionality"""

    @patch('Metric_multi_entity_analysis.st')
    def test_csv_can_be_reimported(self, mock_st):
        """Test that exported CSV can be re-imported without data loss"""
        from Metric_multi_entity_analysis import main
        import io

        test_data = "Entity A 10\nEntity B 5"
        mock_st.text_area.return_value = test_data
        mock_st.button.return_value = True

        main()

        # Get CSV data
        csv_data = mock_st.download_button.call_args[1]['data']

        # Try to re-import it
        df_imported = pd.read_csv(io.StringIO(csv_data))

        # Check structure is preserved
        assert list(df_imported.columns) == ['Entity', 'Volume']
        assert len(df_imported) == 2

        # Check data is preserved
        assert 'Entity A' in df_imported['Entity'].values
        assert 'Entity B' in df_imported['Entity'].values

    @patch('Metric_multi_entity_analysis.st')
    def test_csv_handles_special_characters(self, mock_st):
        """Test that CSV properly escapes special characters"""
        from Metric_multi_entity_analysis import main
        import io

        # Entity with comma (requires CSV escaping)
        test_data = "Entity A, Inc|Entity B"
        mock_st.text_area.return_value = test_data
        mock_st.button.return_value = True

        main()

        # Get CSV data
        csv_data = mock_st.download_button.call_args[1]['data']

        # Re-import to verify proper escaping
        df_imported = pd.read_csv(io.StringIO(csv_data))

        # Entity name with comma should be preserved
        assert 'Entity A, Inc' in df_imported['Entity'].values

    @patch('Metric_multi_entity_analysis.st')
    def test_csv_includes_all_rows(self, mock_st):
        """Test that CSV includes all processed rows"""
        from Metric_multi_entity_analysis import main

        # Create data with multiple entities
        entities = [f"Entity{i}" for i in range(10)]
        test_data = "|".join(entities)

        mock_st.text_area.return_value = test_data
        mock_st.button.return_value = True

        main()

        # Get CSV data
        csv_data = mock_st.download_button.call_args[1]['data']

        # Count lines (header + 10 data rows)
        lines = csv_data.strip().split('\n')
        assert len(lines) == 11  # 1 header + 10 entities


class TestUIFlow:
    """Test complete user interaction flows"""

    @patch('Metric_multi_entity_analysis.st')
    def test_complete_user_flow(self, mock_st):
        """Test complete user flow from input to download"""
        from Metric_multi_entity_analysis import main

        # Simulate user entering data
        user_input = "Entity A|Entity B|Entity C 10"
        mock_st.text_area.return_value = user_input
        mock_st.button.return_value = True

        # Run main function
        main()

        # Verify complete flow
        # 1. Title displayed
        assert mock_st.title.called

        # 2. Text area created
        assert mock_st.text_area.called

        # 3. Button created
        assert mock_st.button.called

        # 4. Data processed and displayed
        assert mock_st.subheader.called
        assert mock_st.write.called

        # 5. Download button created
        assert mock_st.download_button.called

    @patch('Metric_multi_entity_analysis.st')
    def test_multiple_button_clicks(self, mock_st):
        """Test behavior with multiple button clicks (re-processing)"""
        from Metric_multi_entity_analysis import main

        # First click
        mock_st.text_area.return_value = "Entity A"
        mock_st.button.return_value = True
        main()

        first_call_count = mock_st.write.call_count

        # Reset mocks for second click
        mock_st.reset_mock()

        # Second click with different data
        mock_st.text_area.return_value = "Entity B"
        mock_st.button.return_value = True
        main()

        # Should process again
        assert mock_st.write.called
