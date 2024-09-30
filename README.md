# arxiv_downloder

## Description
`arxiv_downloder` is a simple Python tool designed for mass downloading of arXiv papers. It fetches PDF files of papers from arXiv based on provided arXiv IDs.

## Features
- Retrieve and download PDFs of arXiv papers.
- Automatically sanitize file names for the downloaded PDFs.
- Maintain a list of completed downloads to avoid duplicates.

## Installation
To use this tool, you need to have Python installed on your system. You also need to install the required dependencies. You can install them using pip:

```bash
pip install -r requirements.txt
```

## Usage
You can use the script by providing a file containing arXiv IDs or directly passing the IDs as arguments.

### Command Line Arguments
- `-f`, `--file`: Path to a file containing arXiv IDs (default: `arxiv_ids.txt`).
- `-i`, `--ids`: List of arXiv IDs.

### Examples

#### Using a file with arXiv IDs
```bash
python arxiv_downloader.py -f path/to/arxiv_ids.txt
```

#### Using a list of arXiv IDs
```bash
python arxiv_downloader.py -i 1234.56789 9876.54321
```

## File Structure
- `arxiv_downloader.py`: Main script to download arXiv papers.
- `arxiv_ids.txt`: Default file containing arXiv IDs.
- `completed_ids.txt`: File maintaining the list of already downloaded arXiv IDs.
- `arxiv_papers/`: Directory where downloaded PDFs are saved.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.
