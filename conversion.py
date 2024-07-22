import pandas as pd
import numpy as np
import argparse

def process_csv(input_file, output_file):
    # Read the CSV file and skip the first two rows to get to the actual header
    df = pd.read_csv(input_file, skiprows=2)

    # Cleaning and formatting the data
    df.columns = df.columns.str.strip()  # Remove leading/trailing whitespace from column names
    df.dropna(how='all', inplace=True)  # Drop rows where all elements are NaN

    # Update 'Undervisningstyp' if it is "Se Kommentar"
    df.loc[df['Undervisningstyp'] == 'Se kommentar', 'Undervisningstyp'] = df['Information till student']

    # Combine 'Kurs' and 'Undervisningstyp' into a new column 'Subject'
    df['Subject'] = df['Kurs'].fillna('') + ' ' + df['Undervisningstyp'].fillna('')

    # Adds a condition that if there is info in the "Information till student" column, a "ⓘ" symbol is added to the title of the event
    condition = (df['Information till student'].notna()) & (df['Information till student'] != '') & (df['Undervisningstyp'] != df['Information till student'])
    df['Subject'] = np.where(condition, df['Subject'] + ' ⓘ', df['Subject'])

    # Add the room name in parentheses, only if there is a value in the 'Lokal' column
    df['Subject'] = np.where(df['Lokal'].notna() & (df['Lokal'] != ''), df['Subject'] + ' (' + df['Lokal'] + ')', df['Subject'])
    df['Subject'] = df['Subject'].str.strip()

    # Concatenate columns into the 'Description' column with <br/> tags
    df['Description'] = (
        'Information till student: ' + df['Information till student'].fillna('') + '<br/>' +
        'Lokal: ' + df['Lokal'].fillna('') + '<br/>' +
        'Studentgrupp: ' + df['Studentgrupp'].fillna('') + '<br/>' +
        'Fria grupper: ' + df['Fria grupper'].fillna('') + '<br/>' +
        'Lärare: ' + df['Lärare'].fillna('')
    )

    # Delete columns that are no longer needed
    df = df.drop(columns=['Kurs', 'Undervisningstyp', 'Lokal', 'Kartlänk', 'Lärare', 'Studentgrupp', 'Fria grupper', 'Information till student'])

    df['Location'] = ""
    df['Private'] = True

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a CSV file.')
    parser.add_argument('input_file', type=str, help='The input CSV file')
    parser.add_argument('output_file', type=str, help='The output CSV file')
    args = parser.parse_args()

    process_csv(args.input_file, args.output_file)
