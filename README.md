# Metric Entity Volume Analyser

![Tests](https://github.com/markgreig/Multi_metric_analysis/workflows/Run%20Tests/badge.svg)
[![codecov](https://codecov.io/gh/markgreig/Multi_metric_analysis/branch/main/graph/badge.svg)](https://codecov.io/gh/markgreig/Multi_metric_analysis)

A Streamlit web application for analyzing and aggregating entity volumes from pipe-delimited text data.

## Features

- **Parse pipe-delimited data**: Process entities separated by `|` characters
- **Volume tracking**: Assign volumes to entities (defaults to 1 if not specified)
- **Automatic aggregation**: Duplicate entities are automatically summed
- **Sorted results**: Output sorted by volume in descending order
- **CSV export**: Download processed data as CSV
- **Web interface**: User-friendly Streamlit interface

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/markgreig/Multi_metric_analysis.git
cd Multi_metric_analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the Streamlit application:

```bash
streamlit run Metric_multi_entity_analysis.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Input Format

Enter data in one of these formats:

**Pipe-separated entities (all get same volume):**
```
Entity A|Entity B|Entity C 5
```
Result: Entity A, B, and C each have volume 5

**Multi-line format:**
```
Entity A
Entity B 10
Entity A 5
```
Result: Entity A has volume 6 (1 + 5), Entity B has volume 10

**Mixed format:**
```
Entity A|Entity B 3
Entity C|Entity A
```
Result: Entity A has volume 4 (3 + 1), Entity B has volume 3, Entity C has volume 1

### Volume Specification

- If a line ends with a number separated by space, that number is the volume for all entities on that line
- If no volume is specified, entities default to volume 1
- Volumes are summed for duplicate entities across all lines

## Development

### Project Structure

```
Multi_metric_analysis/
├── Metric_multi_entity_analysis.py  # Main application
├── tests/                           # Test suite
│   ├── test_process_data.py        # Basic functionality tests
│   ├── test_edge_cases.py          # Edge case tests
│   ├── test_data_validation.py     # Validation tests
│   ├── test_streamlit_ui.py        # UI integration tests
│   └── README.md                   # Test documentation
├── .github/workflows/              # CI/CD configuration
│   └── tests.yml                   # GitHub Actions workflow
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Pytest configuration
├── .coveragerc                     # Coverage configuration
└── README.md                       # This file
```

### Running Tests

**Run all tests:**
```bash
pytest tests/
```

**Run with coverage report:**
```bash
pytest tests/ --cov=. --cov-report=term-missing --cov-report=html
```

**View HTML coverage report:**
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**Run specific test file:**
```bash
pytest tests/test_process_data.py -v
```

### Test Coverage

The project maintains **96.88% code coverage** with **84 tests** covering:

- ✅ Basic functionality (14 tests)
- ✅ Edge cases (53 tests)
- ✅ Data validation (22 tests)
- ✅ Streamlit UI integration (15 tests)

See [tests/README.md](tests/README.md) for detailed test documentation.

### CI/CD

The project uses GitHub Actions for continuous integration:

- **Automated testing** on push and pull requests
- **Multi-version support**: Tests run on Python 3.9, 3.10, and 3.11
- **Coverage reporting** via Codecov
- **Test caching** for faster builds

Workflow configuration: [.github/workflows/tests.yml](.github/workflows/tests.yml)

## API Documentation

### `process_data(data: str) -> pd.DataFrame`

Process pipe-delimited entity data with optional volume counts.

**Parameters:**
- `data` (str): Input text with entities separated by pipes (|) or newlines

**Returns:**
- `pd.DataFrame`: DataFrame with columns ['Entity', 'Volume'], sorted by volume descending

**Example:**
```python
from Metric_multi_entity_analysis import process_data

result = process_data("Entity A|Entity B 5")
# Returns DataFrame:
#    Entity  Volume
# 0  Entity A     5
# 1  Entity B     5
```

### `main()`

Main Streamlit application entry point. Creates the web interface for data input, processing, and CSV export.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Run tests to ensure they pass (`pytest tests/`)
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

### Code Quality

- Maintain or improve test coverage (currently 96.88%)
- Add tests for new features
- Follow existing code style
- Update documentation as needed

## License

This project is available for use under standard open source practices.

## Support

For issues, questions, or contributions, please open an issue on the [GitHub repository](https://github.com/markgreig/Multi_metric_analysis/issues).

## Changelog

### Latest (Unreleased)
- Added comprehensive test suite with 96.88% coverage
- Added input validation to prevent crashes on malformed data
- Added docstrings to all functions
- Added CI/CD with GitHub Actions
- Fixed comment inconsistencies
- Improved code documentation

### Previous Versions
- Initial release with basic entity volume analysis functionality
