import pandas as pd

# delete contents of transformed folder
import shutil
shutil.rmtree('transformed')
shutil.os.mkdir('transformed')

file_transformations = [
    {
        'file_to_transform': 'cc relations.xlsx',
        'column_transformations': [
            {
                'isDelete': False,
                'file_with_name': 'cc names.xlsx',
                'column_to_transform': 'item_id',
                'column_with_name': 'item_name',
                'primary_key': 'item_id',
            }
        ],
        'export_file_name': 'cc relations transformed.xlsx',
    },
    {
        'file_to_transform': 'cases main.xlsx',
        'column_transformations': [
            {
                'isDelete': True,
                'column_to_transform': 'case_num',
            },
            # {
            #     # TODO this is the CC transformation and it's fucking hard
            #     'isDelete': False,
            #     'file_with_name': 'cc relations.xlsx',
            #     'column_to_transform': 'CC',
            #     'column_with_name': 'item_id',
            #     'primary_key': 'case_id',
            # }
        ],
        'export_file_name': 'cases main transformed.xlsx',
    },
    {
        'file_to_transform': 'modules main.xlsx',
        'column_transformations': [
            {
                'isDelete': True,
                'column_to_transform': 'ID',
            },
        ],
    },
    {
        'file_to_transform': 'cases abnormal nerves.xlsx',
        'column_transformations': [
            {
                'isDelete': False,
                'file_with_name': 'nerves main.xlsx',
                'column_to_transform': 'Name',
                'column_with_name': 'Name',
                'primary_key': 'ID',
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
                'primary_key': 'ID',
            }
        ],
        'export_file_name': 'cases abnormal muscles transformed.xlsx',
    }
]

for file_transformation in file_transformations:
    # Read in the file_to_transform file
    to_transform_df = pd.read_excel(
        f'original/{file_transformation["file_to_transform"]}')

    # Loop through the column transformations
    for column_transformation in file_transformation['column_transformations']:
        print(
            f'Transforming {column_transformation["column_to_transform"]} in {file_transformation["file_to_transform"]}')
        # If the column is to be deleted, delete it and continue to the next column transformation
        if column_transformation['isDelete']:
            print(f'Deleting {column_transformation["column_to_transform"]}')
            del to_transform_df[column_transformation['column_to_transform']]
            continue

        # Read in the file_with_name file
        with_name_df = pd.read_excel(
            f'original/{column_transformation["file_with_name"]}')

        # Create a dictionary to map ID to nerve/muscle names
        name_dict = with_name_df.set_index(
            column_transformation['primary_key'])[column_transformation['column_with_name']].to_dict()

        # Use the map function to replace the ID in the file_to_transform file with the corresponding nerve/muscle name
        to_transform_df[column_transformation['column_to_transform']
                        ] = to_transform_df[column_transformation['column_to_transform']].map(name_dict)
    # Save the modified file_to_transformed file
    to_transform_df.to_excel(
        f'transformed/{file_transformation["export_file_name"]}', index=False)


transformations_dict = {
    'cases main': {
        'cases_diagnosis_diagnosis_transformation': cases_diagnosis_diagnosis_transformation,
        'cases_diagnosis_ncs_criteria_transformation': cases_diagnosis_ncs_criteria_transformation,
        'cases_diagnosis_emg_criteria_transformation': cases_diagnosis_emg_criteria_transformation,
        'cases_differential_diagnosis_transformation': cases_differential_diagnosis_transformation,
        'cases_differential_criteria_transformation': cases_differential_criteria_transformation,
    }
}



def cases_diagnosis_diagnosis_transformation():
    # Get "diag_name" from table "diagnoses names (to destroy)" where Diagnosis = "diag_name_id"
    return


def cases_diagnosis_ncs_criteria_transformation():
    # Get from table "diagnoses relations (to destroy)" columns ns_compounds and ns_logic
    pass


def cases_diagnosis_emg_criteria_transformation():
    # Get from table "diagnoses relations (to destroy)" columns ms_compounds and ms_logic
    pass


def cases_differential_diagnosis_transformation():
    # Get "diag_name" from table "diagnoses names (to destroy)" where Diagnosis = "diag_name_id"
    pass


def cases_differential_criteria_transformation():
    # Get from logic tab below
    pass


def cases_main_cc_transformation():
    # Use case_id to match item_id in table "cc relations", then get the actual name from table "cc names". Separate names by comma (i.e. "A, B, C")
    pass
    

def muscles_main_root_transformation():
    # Pull from table "muscles roots (to destroy)" matching ID. Separate multiple with comma, then add + for important = Y or - for important = N. Example for ID1: C6+, C5-
    pass


def modules_main_cases_transformation():
    # Create comma separated list by matching ID with "module_id" from table "module cases (to destroy)" and then grabbing "case_num" by matching "case_id" from table "cases main", ideally in the order specified by "case_order"
    pass
