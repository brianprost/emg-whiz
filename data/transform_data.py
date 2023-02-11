import pandas as pd

# delete contents of transformed folder
import shutil
shutil.rmtree('transformed')
shutil.os.mkdir('transformed')

file_transformations = [
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
        'file_to_transform': 'cases diagnosis.xlsx',
        'column_transformations': [
            {
                'isDelete': False,
                'file_with_name': 'diagnoses names (to destroy).xlsx',
                'column_to_transform': 'Diagnosis',
                'column_with_name': 'diag_name',
                'primary_key': 'diag_name_id',
            },
            {
                'isDelete': False,
                'isSpecial': True,
                'specialTransform': [
                    'cases_diagnosis_ncs_criteria_transformation',
                    'cases_diagnosis_emg_criteria_transformation',
                ],
            }
        ],
    },
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
            {
                'isDelete': False,
                'isSpecial': True,
                'specialTransform': [
                    'cases_main_cc_transformation',
                ],
            }
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
    }
]


def main():
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
                print(
                    f'Deleting {column_transformation["column_to_transform"]}')
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


def cases_main_cc_transformation(cases_main_file, cc_relations_file, cc_names_file, output_file):
    # Use case_id to match item_id in table "cc relations", then get the actual name from table "cc names". Separate names by comma (i.e. "A, B, C")

    # Load the "cases main" table
    df_cases_main = pd.read_excel(f"original/{cases_main_file}")

    # Load the "cc relations" table
    df_relations = pd.read_excel(f"original/{cc_relations_file}")

    # load the "cc names" table
    df_names = pd.read_excel(f"original/{cc_names_file}")

    # Create a dictionary to map ID to nerve/muscle names
    name_dict = df_names.set_index('item_id')['item_name'].to_dict()

    # Loop through each row in the "cases main" table
    for index, row in df_cases_main.iterrows():
        # Create a list to hold the names of the cc's
        cc_names = []

        # Loop through each row in the "cc relations" table
        for index2, row2 in df_relations.iterrows():
            # If the case_id in the "cc relations" table matches the current case_id in the "cases main" table, add the name of the cc to the list
            if row2['case_id'] == row['case_id']:
                cc_names.append(name_dict[row2['item_id']])

        # Add the list of cc names to the "cc" column in the "cases main" table
        df_cases_main.at[index, 'CC'] = ', '.join(cc_names)

    # Save the modified "cases main" table
    df_cases_main.to_excel(f"transformed/{output_file}", index=False)


def muscles_main_root_transformation():
    # Pull from table "muscles roots (to destroy)" matching ID. Separate multiple with comma, then add + for important = Y or - for important = N. Example for ID1: C6+, C5-
    pass


def modules_main_cases_transformation():
    # Create comma separated list by matching ID with "module_id" from table "module cases (to destroy)" and then grabbing "case_num" by matching "case_id" from table "cases main", ideally in the order specified by "case_order"
    pass


def to_xlsx(file_name, sheet_name, df):
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()


def to_csv(file_name, df):
    df.to_csv(file_name, index=False)


if __name__ == '__main__':
    # cases_main_cc_transformation(
    #     'cases main transformed.xlsx', 'cases main.xlsx', 'cc')

    cases_main_cc_transformation(
        "cases main.xlsx", "cc relations.xlsx", "cc names.xlsx", "cases main transformed.xlsx")
