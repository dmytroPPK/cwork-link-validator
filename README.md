# LinkValidator

Welcome to the awesome project! )

## Description

This application is able to parse two types of resources: url of the site and a pdf file. After parsing resource, one grabs and validates urls. Then these urls are written to the corresponding files: valid_links.txt and broken_links.txt

## Installation

1. Clone the repository: git clone git@github.com:dmytroPPK/cwork-link-validator.git
2. Create virtual environment: python -m venv env
3. Activate created venv: source env/bin/activate 
4. Install the dependencies: pip install -r requirements.txt

## Usage

To run the project, use one of the following commands:
1. ' python main.py ' - set resource by user input
2. ' python main.py --pdf path_to_pdf '
3. ' python main.py --url url_to_site '
#### *Also, you can change main.py file and explicitly set resource via constructor of LinkValidator class

## Features

- run python main.py -h to show help.
- destination of *links.txt files is output folder by default
- logs are written to the logs.txt file

