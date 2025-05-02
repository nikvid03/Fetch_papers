# Papers Fetcher

A Python tool to fetch research papers with authors from pharmaceutical or biotech companies from PubMed.

## Features

- Searches PubMed using its full query syntax
- Identifies papers with at least one author affiliated with a pharmaceutical or biotech company
- Outputs results as a CSV file with detailed information

## Installation

### Prerequisites

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/papers-fetcher.git
   cd papers-fetcher
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

This will create a virtual environment with all required dependencies and install the `get-papers-list` command.

## Usage

### Basic Usage

```bash
get-papers-list "your pubmed query"
```

This will search PubMed for the given query, identify papers with authors from pharmaceutical or biotech companies, and print the results to the console.

### Available Options

- `-h, --help`: Display usage instructions
- `-d, --debug`: Print debug information during execution
- `-f, --file FILENAME`: Specify the filename to save the results (if not provided, print to console)
- `-m, --max-results NUMBER`: Maximum number of results to fetch (default: 100)
- `-e, --email EMAIL`: Email address for PubMed API (default: user@example.com)

### Examples

1. Search for papers on COVID-19 vaccines and print to console:
   ```bash
   get-papers-list "COVID-19 vaccines"
   ```

2. Search for papers on cancer immunotherapy, save to file, and show debug info:
   ```bash
   get-papers-list "cancer immunotherapy" -f results.csv -d
   ```

3. Search for papers by a specific author with a company affiliation:
   ```bash
   get-papers-list "Smith J[Author] pharma"
   ```

## Code Organization

The project is organized as follows:

- `papers_fetcher/`: Main package
  - `__init__.py`: Package initialization
  - `api.py`: PubMed API interaction using Biopython
  - `parser.py`: Parsing and processing API responses
  - `filters.py`: Filtering for non-academic authors
  - `output.py`: CSV output handling
  - `cli.py`: Command-line interface
- `pyproject.toml`: Poetry configuration
- `README.md`: This documentation

## How It Works

1. **Search**: The program searches PubMed for papers matching the query
2. **Fetch**: It fetches detailed information for each paper
3. **Parse**: It extracts relevant information like authors and affiliations
4. **Filter**: It identifies authors affiliated with pharmaceutical or biotech companies using keyword matching
5. **Output**: It formats the results and outputs them as a CSV file

## Identifying Non-Academic Authors

The program uses several heuristics to identify authors with pharmaceutical or biotech company affiliations:

1. **Affiliation Text Analysis**: Looks for company-related keywords (e.g., "pharma", "biotech", "inc", "ltd") and excludes academic keywords (e.g., "university", "hospital", "institute")
2. **Email Domain Check**: Checks email domains (.com, .co, etc. vs .edu, .ac.uk, etc.)
3. **Company Name Extraction**: Attempts to extract formal company names from affiliations using regular expressions

## Tools Used

- [Biopython](https://biopython.org/): For interfacing with the PubMed API (Entrez)
- [Poetry](https://python-poetry.org/): For dependency management and packaging

## License

This project is available under the MIT License.