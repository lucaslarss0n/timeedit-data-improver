import pandas as pd
import numpy as np

# Read the CSV file and skip the first two rows to get to the actual header
df = pd.read_csv('schema.csv', skiprows=2)

# Cleaning and formatting the data
df.columns = df.columns.str.strip()  # Remove leading/trailing whitespace from column names
df.dropna(how='all', inplace=True)  # Drop rows where all elements are NaN

# Update 'Undervisningstyp' if it is "Se Kommentar"
df.loc[df['Undervisningstyp'] == 'Se kommentar', 'Undervisningstyp'] = df['Information till student']

# Combine 'Kurs' and 'Undervisningstyp' into a new column 'Subject'
df['Subject'] = df['Kurs'].fillna('') + ' ' + df['Undervisningstyp'].fillna('')

# Define the condition to add "ⓘ" symbol
condition = (df['Information till student'].notna()) & (df['Information till student'] != '') & (df['Undervisningstyp'] != df['Information till student'])

# Update the 'Subject' column to add the "ⓘ" symbol
df['Subject'] = np.where(condition, df['Subject'] + ' ⓘ', df['Subject'])

# Add the room name in parentheses, only if there is a value in the 'Lokal' column
df['Subject'] = np.where(df['Lokal'].notna() & (df['Lokal'] != ''), df['Subject'] + ' (' + df['Lokal'] + ')', df['Subject'])

# Remove any leading/trailing spaces
df['Subject'] = df['Subject'].str.strip()

# Concatenate columns into the 'Description' column with <br/> tags
df['Description'] = (
    'Information till student: ' + df['Information till student'].fillna('') + '<br/>' +
    'Lokal: ' + df['Lokal'].fillna('') + '<br/>' +
    'Studentgrupp: ' + df['Studentgrupp'].fillna('') + '<br/>' +
    'Fria grupper: ' + df['Fria grupper'].fillna('') + '<br/>' +
    'Lärare: ' + df['Lärare'].fillna('')
)

# Delete the unnecessary columns
df = df.drop(columns=['Kurs', 'Undervisningstyp', 'Lokal', 'Kartlänk', 'Lärare', 'Studentgrupp', 'Fria grupper', 'Information till student'])

# Set 'Location' to "Linköpings universitet, 581 83 Linköping, Sverige"
df['Location'] = ""

# Add 'Private' column and set it to True
df['Private'] = True

# Save the updated DataFrame to a new CSV file
df.to_csv('nyttschema.csv', index=False)
