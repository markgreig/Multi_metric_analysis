# Test Suite for Multi_metric_analysis

This directory contains comprehensive tests for the Metric Entity Volume Analyser application.

## Test Coverage: 96.88%

All 84 tests pass successfully, covering the main application logic with 96.88% code coverage.

## Test Structure

### test_process_data.py
**Basic functionality tests** for the core `process_data()` function.

- Single entity processing (with and without volumes)
- Multiple entities (pipe-delimited and multi-line)
- Entity aggregation and volume summation
- Sorting by volume (descending order)
- DataFrame structure validation
- Whitespace handling
- Volume detection logic

**14 tests** covering fundamental parsing and aggregation behavior.

### test_edge_cases.py
**Edge case tests** for unusual inputs and boundary conditions.

Test categories:
- Empty and whitespace inputs
- Pipe delimiter edge cases (consecutive pipes, leading/trailing pipes)
- Special characters (apostrophes, ampersands, Unicode, emojis)
- Volume edge cases (zero, negative numbers, decimals)
- Case sensitivity
- Long inputs (500+ character entity names, 1000+ entities)
- Data integrity (no duplicates, volume preservation, no nulls)

**53 tests** ensuring robustness against unusual inputs.

### test_data_validation.py
**Data validation tests** for malformed inputs and output consistency.

Test categories:
- Malformed input (numbers only, multiple numbers, alphanumeric)
- Volume parsing robustness (large numbers, scientific notation, hexadecimal)
- Output validation (correct columns, data types, sorting, index reset)
- Real-world scenarios (company names, teams, special characters)
- Consistency across different input formats

**22 tests** validating data integrity and format handling.

### test_streamlit_ui.py
**UI integration tests** for Streamlit components using mocks.

Test categories:
- UI component creation (title, text area, buttons)
- Data processing on button click
- DataFrame display
- CSV export (download button, format, content)
- Complete user flow (input → process → display → download)
- CSV re-import validation

**15 tests** ensuring proper UI behavior and CSV export functionality.

## Running Tests

### Run all tests:
```bash
pytest tests/
```

### Run with coverage report:
```bash
pytest tests/ --cov=. --cov-report=term-missing --cov-report=html
```

### Run specific test file:
```bash
pytest tests/test_process_data.py -v
```

### Run specific test:
```bash
pytest tests/test_process_data.py::TestBasicFunctionality::test_single_entity_without_volume -v
```

## Coverage Report

After running tests with coverage, an HTML report is generated in `htmlcov/`:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Test Results Summary

```
84 tests total
✓ 84 passed
✗ 0 failed

Code Coverage: 96.88%
Missing: Line 75 only (if __name__ == '__main__' guard)
```

## Key Test Findings

### Confirmed Behavior
- Empty strings in pipe-delimited lists are filtered out
- Case is preserved (entities are NOT converted to lowercase despite comment)
- Volume applies to all entities on the same line
- Whitespace is properly stripped from entity names
- Special characters and Unicode are supported

### Areas Covered
- ✓ Basic parsing and aggregation
- ✓ Volume detection and summation
- ✓ Sorting and DataFrame structure
- ✓ Empty/whitespace handling
- ✓ Special characters and Unicode
- ✓ Edge cases (large numbers, long names)
- ✓ Data integrity and consistency
- ✓ CSV export and re-import
- ✓ Streamlit UI components

## Future Test Enhancements

Potential areas for additional testing:
1. Performance benchmarks for large datasets
2. Memory usage profiling
3. Concurrent user testing (if deployed)
4. Browser-based E2E tests for Streamlit UI
5. Security testing (injection attacks, malicious input)

## Dependencies

Test dependencies are listed in `requirements.txt`:
- pytest>=7.4.0
- pytest-cov>=4.1.0
- streamlit>=1.28.0
- pandas>=2.0.0
