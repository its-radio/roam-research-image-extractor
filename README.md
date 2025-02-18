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

First, you'll need to export a page from roam research from which to extract images. Select "Export Page" from the menu.
![export](https://github.com/user-attachments/assets/cdd3a9ba-1b85-4f55-acc2-42900eec0b16)

Then select "Markdown" and click Export.
![markdown](https://github.com/user-attachments/assets/fe1f08f9-fa08-4bb0-be52-a8f62f7fa8d2)

Make sure to save it in a location you remember.

Finally, simply install the script via the instructions above and run it, providing the location of the newly exported markdown file.

```bash
python3 /path/to/repo/roam-research-image-extractor.py -f /path/to/roam/page.md
```
For a list of options, run:

```bash
python3 /path/to/repo/roam-research-image-extractor.py -h
```

