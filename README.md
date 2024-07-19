# CSV Processor
This CLI tool processes CSV files to format and clean data for use in various applications.

## Installation
### Prerequisites
Ensure you have Python installed on your computer. You can download Python from python.org.

Ensure you have pip installed. pip comes with Python, but you can upgrade it using the following command:

pip install --upgrade pip

### Steps
Clone or Download the Repository:

If you have Git installed, you can clone this repository. Otherwise, you can download it as a ZIP file and extract it.

git clone <repository-url>

cd <repository-folder>

Navigate to the Project Directory:

Change directory to the project folder where setup.py is located.

cd <repository-folder>

Install the Required Dependencies:

Install the necessary Python packages listed in the requirements.txt file.

pip install -r requirements.txt

Install the CLI Tool:

Use the following command to install the CLI tool:

pip install .

## Usage
To process a CSV file, use the following command:

process_csv input.csv output.csv

Replace input.csv with the path to your input file and output.csv with the desired output file path.

### Example
If you have a file named schema.csv in the current directory and you want to save the processed file as nyttschema.csv, run:

process_csv schema.csv nyttschema.csv

## How It Works
The script performs the following steps:

Reads the input CSV file and skips the first two rows to get to the actual header.
Cleans and formats the data by:
Removing leading/trailing whitespace from column names.
Dropping rows where all elements are NaN.
Updates the Undervisningstyp column if it is "Se kommentar".
Combines Kurs and Undervisningstyp into a new column Subject:
Adds an "ⓘ" symbol if there is additional information in the Information till student column.
Adds the room name in parentheses if there is a value in the Lokal column.
Concatenates columns into the Description column with <br/> tags for line breaks.
Deletes unnecessary columns.
Sets the Location to "Linköpings universitet, 581 83 Linköping, Sverige".
Adds a Private column and sets it to True.
Saves the updated DataFrame to the specified output CSV file.
Troubleshooting
Ensure you have all the necessary dependencies installed by running pip install -r requirements.txt.
Make sure you are using the correct paths for your input and output files.
If you encounter any issues, please open an issue in the repository or contact the maintainer.
License
This project is licensed under the MIT License. See the LICENSE file for details.