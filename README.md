### NAE KNN CLassifier
Extracts biofingerprints - interpupillary distance and colour/chromacity from NAE images. Signals classified using KNN classification.

## Requirements

* `python3`
* `pip`
* `virtualenv`

## Usage

1. Setup a virtual environment using the command `virtualenv venv`
2. Activate the virtual environment using `source venv/bin/activate`
3. Install package dependencies using `pip install -r requirements.txt`
4. Execute using the following

# Extracting interpupillary distance and colour/chromacity
	`python3 main.py -i path-to-image -c class
		Test files: raw_images
Data is appended to distcolour.csv

# Splitting data into training and test data
	`python3 split.py`

# KNN Classification
	`python3 knn.py`