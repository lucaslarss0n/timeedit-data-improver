from flask import Blueprint, render_template, request, redirect, url_for, send_file
import pandas as pd
import os
import numpy as np

bp = Blueprint("pages", __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@bp.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' in request.files:
            # Handling the file upload
            file = request.files['file']
            if file.filename == '':
                print("No file selected.")
                return redirect(request.url)
            if file:
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                print(f"Saving file to: {file_path}")
                file.save(file_path)

                # Read the CSV file
                df = pd.read_csv(file_path, skiprows=2)

                # Replace NaN/empty values in "Fria grupper" with "Blank"
                df['Fria grupper'] = df['Fria grupper'].fillna('Blank')

                # Extract unique "Fria grupper" and convert to list
                fria_grupper = df['Fria grupper'].unique().tolist()
                print(f"Fria grupper: {fria_grupper}")

                # Render the template with the "Fria grupper" options
                return render_template('home.html', fria_grupper=fria_grupper, filename=file.filename)

        elif 'filename' in request.form:
            filename = request.form['filename']
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            print(f"Processing file: {file_path}")
            df = pd.read_csv(file_path, skiprows=2)

            # Replace NaN/empty values in "Fria grupper" with "Blank"
            df['Fria grupper'] = df['Fria grupper'].fillna('Blank')

            selected_groups = request.form.getlist('fria_grupper')
            print(f"Selected groups: {selected_groups}")
            filtered_df = df[df['Fria grupper'].isin(selected_groups)].copy()

            # Apply your existing transformations to the filtered_df
            filtered_df.columns = filtered_df.columns.str.strip()
            filtered_df.dropna(how='all', inplace=True)
            filtered_df.loc[filtered_df['Undervisningstyp'] == 'Se kommentar', 'Undervisningstyp'] = filtered_df['Information till student']
            filtered_df['Subject'] = filtered_df['Kurs'].fillna('') + ' ' + filtered_df['Undervisningstyp'].fillna('')
            condition = (filtered_df['Information till student'].notna()) & (filtered_df['Information till student'] != '') & (filtered_df['Undervisningstyp'] != filtered_df['Information till student'])
            filtered_df['Subject'] = np.where(condition, filtered_df['Subject'] + ' ⓘ', filtered_df['Subject'])
            filtered_df['Subject'] = np.where(filtered_df['Lokal'].notna() & (filtered_df['Lokal'] != ''), filtered_df['Subject'] + ' (' + filtered_df['Lokal'] + ')', filtered_df['Subject'])
            filtered_df['Subject'] = filtered_df['Subject'].str.strip()
            filtered_df['Description'] = (
                'Information till student: ' + filtered_df['Information till student'].fillna('') + '<br/>' +
                'Lokal: ' + filtered_df['Lokal'].fillna('') + '<br/>' +
                'Studentgrupp: ' + filtered_df['Studentgrupp'].fillna('') + '<br/>' +
                'Fria grupper: ' + filtered_df['Fria grupper'].fillna('') + '<br/>' +
                'Lärare: ' + filtered_df['Lärare'].fillna('')
            )
            filtered_df = filtered_df.drop(columns=['Kurs', 'Undervisningstyp', 'Lokal', 'Kartlänk', 'Lärare', 'Studentgrupp', 'Fria grupper', 'Information till student'])
            filtered_df['Location'] = ""
            filtered_df['Private'] = True

            output_file = os.path.join(UPLOAD_FOLDER, 'output.csv')
            filtered_df.to_csv(output_file, index=False)

            # Verify that the output file exists before attempting to send it
            if os.path.exists(output_file):
                print(f"Sending file: {output_file}")
                return send_file(output_file, as_attachment=True)
            else:
                return f"Error: The file {output_file} was not found."

    return render_template('home.html')

@bp.route("/about")
def about():
    return render_template("about.html")
