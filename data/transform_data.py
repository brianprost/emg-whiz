import pandas as pd

# delete contents of transformed folder
import shutil
shutil.rmtree('transformed')
shutil.os.mkdir('transformed')

file_transformations = [
    {
        'file_to_transform': 'cases main.xlsx',
        'column_transformations': [
            {
                'isDelete': True,
                'column_to_transform': 'case_num',
            },
            {
                'isDelete': False,
                'file_with_name': 'cc names.xlsx',
                'column_to_transform': 'Name',
                'column_with_name': 'Name',
            }
        ],
        'export_file_name': 'cases abnormal nerves transformed.xlsx',
    },
    {
        'file_to_transform': 'cases abnormal nerves.xlsx',
        'column_transformations': [
            {
                'isDelete': False,
                'file_with_name': 'nerves main.xlsx',
                'column_to_transform': 'Name',
                'column_with_name': 'Name',
            }
        ],
        'export_file_name': 'cases abnormal nerves transformed.xlsx',
    },
    {
        'file_to_transform': 'cases abnormal muscles.xlsx',
        'column_transformations': [
            {
                'isDelete': False,
                'file_with_name': 'muscles main.xlsx',
                'column_to_transform': 'Name',
                'column_with_name': 'Name',
            }
        ],
        'export_file_name': 'cases abnormal muscles transformed.xlsx',
    }
]

for file_transformation in file_transformations:
    # Read in the file_to_transform file
    to_transform_df = pd.read_excel(f'original/{file_transformation["file_to_transform"]}')

    # Loop through the column transformations
    for column_transformation in file_transformation['column_transformations']:
        print(f'Transforming {column_transformation["column_to_transform"]} in {file_transformation["file_to_transform"]}')
        # If the column is to be deleted, delete it and continue to the next column transformation
        if column_transformation['isDelete']:
            print(f'Deleting {column_transformation["column_to_transform"]}')
            del to_transform_df[column_transformation['column_to_transform']]
            continue

        # Read in the file_with_name file
        with_name_df = pd.read_excel(f'original/{column_transformation["file_with_name"]}')

        # Create a dictionary to map ID to nerve/muscle names
        name_dict = with_name_df.set_index('ID')[column_transformation['column_with_name']].to_dict()

        # Use the map function to replace the ID in the file_to_transform file with the corresponding nerve/muscle name
        to_transform_df[column_transformation['column_to_transform']] = to_transform_df[column_transformation['column_to_transform']].map(name_dict)

    # Save the modified file_to_transformed file
    to_transform_df.to_excel(
        f'transformed/{file_transformation["export_file_name"]}', index=False)
