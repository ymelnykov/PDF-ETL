"""
Extract, Transform and Load pdf files.
This script is to:
1. Get all pdf files from the source directory.
2. Extract year, month and street name data from the files.
3. Define the merged file name based on the above data.
4. Define the merged file destination directory based on the above data.
5. Merge the files and write the merged file to the destination directory.
6. Delete all pdf files in the source directory.
Done!
"""
import os
import regex as re
from PyPDF2 import PdfReader, PdfWriter


# Define global variables
base_dir = 'C:\\Users\\Karenin\\Documents\\- Платежи\\ЖКХ\\'
source_dir = base_dir + 'merge' # directory for files to merge
dest_dir = base_dir # directory for a merged file
merged_file_name = None

# Define the street mapping
street_map = {
    'Новицького':'Novytskogo',
    'Сорочинська':'Sorochynska',
    'Преображенського': 'Preobrazhenskogo'
    }

# Get all pdf files from the source directory
merge_files = [f_name for f_name in os.listdir(source_dir)
               if f_name.endswith('.pdf')]

# Check if there are any pdf files to merge
if len(merge_files) == 0:
    raise FileNotFoundError('No files to merge!')

# Initialize a pdf writer
merger = PdfWriter()

# Process all pdf files in the source directory
for file in merge_files:
    file_path = os.path.join(source_dir, file)

# Extract the year, month and street name from files
# to define the merged file name
    if merged_file_name is None:
        reader = PdfReader(file_path)
        text = reader.pages[0].extract_text()
        dates = re.findall('\d{2}/\d{2}/\d{4}', text)
        if len(dates) != 0:
            yy = dates[0][-2:]
            mm = dates[0][-7:-5]
        else:
            yy = mm = '00'
        for street in street_map:
            if street in text:
                merged_file_name = yy + mm + '_' + street_map[street]
                dest_dir += street + '\\'
                break

# Append each pdf file to the merger
    merger.append(file_path)

# If no merged file name was defined, use the default one
if merged_file_name is None:
    merged_file_name = '0000_merged_file'

# Define the path to save the merged file
merged_file_path = os.path.join(dest_dir, (merged_file_name + '.pdf'))

# If the file with such name exists in the destiantion directory,
# append the file name with an ordinal index
idx = 0
while os.path.exists(merged_file_path):
    idx += 1
    new_file_name = merged_file_name + f' ({idx}).pdf'
    merged_file_path = os.path.join(dest_dir, new_file_name)

# Write the merged file to the destination directory
merger.write(merged_file_path)

merger.close()

# Delete all pdf files in the source directory
for file in merge_files:
    file_path = os.path.join(source_dir, file)
    os.remove(file_path)

print(f'{len(merge_files)} pdf files have been merged and saved to',
      merged_file_path)    