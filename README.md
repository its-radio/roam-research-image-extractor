# roam-research-image-extractor
A tool to extract and download images stored in a roam research page or graph.


## Requirements

- Python 3.6 or higher
- [requests](https://pypi.org/project/requests/) - HTTP library for making requests in Python

### Built-in Libraries
The project also uses the following built-in Python libraries:
- argparse - Parser for command-line options and arguments
- urllib.parse - URL parsing utilities
- re - Regular expression operations

## Installation

Git clone the repo

```bash
git clone https://github.com/its-radio/roam-research-image-extractor.git
```

cd into it

```bash
cd roam-research-image-extractor
```

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Usage
NOTE: This project currently only supports extracting images from individual pages. However, in the future I may implement extraction from entire exported graphs. If you want it, let me know and I'll implement it.

First, you'll need to export a page from roam research from which to extract images.

