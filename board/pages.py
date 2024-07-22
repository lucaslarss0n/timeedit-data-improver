from flask import Blueprint, render_template, request, redirect, url_for, send_file
import pandas as pd
import os

bp = Blueprint("pages", __name__)
UPLOAD_FOLDER = 'uploads/'

@bp.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' in request.files:
            # Handling the file upload
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            if file:
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)

                # Read the CSV file
                df = pd.read_csv(file_path, skiprows=2)

                # Extract unique class groups and convert to list
                class_groups = df['Studentgrupp'].unique().tolist()
                
                # Render the template with the class groups
                return render_template('home.html', class_groups=class_groups, filename=file.filename)

        elif 'filename' in request.form:
            filename = request.form['filename']
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            df = pd.read_csv(file_path, skiprows=2)
            selected_groups = request.form.getlist('classgroup')
            filtered_df = df[df['Studentgrupp'].isin(selected_groups)]
            
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
            return send_file(output_file, as_attachment=True)
    return render_template('home.html')

@bp.route("/about")
def about():
    return render_template("about.html")
