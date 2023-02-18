import json
import pandas as pd
import shutil
import sys

# delete contents of transformed folder
shutil.rmtree('transformed')
shutil.os.mkdir('transformed')

file_transformations = [
    {
        'file_to_transform': 'cases abnormal muscles.xlsx',
        'column_transformations': [
            {
                'transformation': 'simple_transformation',
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
                'transformation': 'simple_transformation',
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
        'file_to_transform': 'cases diagnoses.xlsx',
        'column_transformations': [
            {
                'transformation': 'simple_transformation',
                'isDelete': False,
                'file_with_name': 'diagnoses names (to destroy).xlsx',
                'column_to_transform': 'Diagnosis',
                'column_with_name': 'diag_name',
                'primary_key': 'diag_name_id',
            },
            {
                'transformation': 'cases_diagnosis_ncs_criteria_transformation'
            },
            {
                'transformation': 'cases_diagnosis_emg_criteria_transformation'
            },
        ],
        'export_file_name': 'cases diagnoses transformed.xlsx',
    },
    {
        'file_to_transform': 'cases differential.xlsx',
        'column_transformations': [
            {
                'transformation': 'simple_transformation',
                # get "diag_name" from table "diagnoses names (to destroy)" where Diagnosis = "diag_name_id"
                'isDelete': False,
                'file_with_name': 'diagnoses names (to destroy).xlsx',
                'column_to_transform': 'Diagnosis',
                'column_with_name': 'diag_name',
                'primary_key': 'diag_name_id',
            },
            {
                'transformation': 'cases_differential_criteria_transformation'
            },
        ],
        'export_file_name': 'cases differential transformed.xlsx',
    },
    {
        'file_to_transform': 'cases main.xlsx',
        'column_transformations': [
            # {
            #     'transformation': 'simple_transformation',
            #     'isDelete': True,
            #     'column_to_transform': 'case_num',
            # },
            {
                'transformation': 'cases_main_cc_transformation',
            },
        ],
        'export_file_name': 'cases main transformed.xlsx',
    },
    {
        'file_to_transform': 'cc relations.xlsx',
        'column_transformations': [
            {
                'transformation': 'simple_transformation',
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
        'file_to_transform': 'modules main.xlsx',
        'column_transformations': [
            {
                'transformation': 'modules_main_cases_transformation',
            },
            # {
            #     'transformation': 'simple_transformation',
            #     'isDelete': True,
            #     'column_to_transform': 'ID',
            # },
        ],
        'export_file_name': 'modules main transformed.xlsx',
    },
    {
        'file_to_transform': 'muscles main.xlsx',
        'column_transformations': [
            {
                'transformation': 'muscles_main_root_transformation',
            },
            # {
            #     'transformation': 'simple_transformation',
            #     'isDelete': True,
            #     'column_to_transform': 'ID',
            # },
        ],
        'export_file_name': 'muscles main transformed.xlsx',
    }
    # {
    #     'file_to_transform': 'nerves main.xlsx',
    #     'column_transformations': [
    #         {
    #             'transformation': 'simple_transformation',
    #             'isDelete': True,
    #             'column_to_transform': 'ID',
    #         },
    #     ],
    #     'export_file_name': 'nerves main transformed.xlsx',
    # }
]


def main():
    transformations_dict = {
        'simple_transformation': simple_transformation,
        'cases_diagnosis_diagnosis_transformation': cases_diagnosis_diagnosis_transformation,
        'cases_diagnosis_ncs_criteria_transformation': cases_diagnosis_ncs_criteria_transformation,
        'cases_diagnosis_emg_criteria_transformation': cases_diagnosis_emg_criteria_transformation,
        'cases_differential_diagnosis_transformation': cases_differential_diagnosis_transformation,
        'cases_differential_criteria_transformation': cases_differential_criteria_transformation,
        'cases_main_cc_transformation': cases_main_cc_transformation,
        'muscles_main_root_transformation': muscles_main_root_transformation,
        'modules_main_cases_transformation': modules_main_cases_transformation,
    }

    # Loop through the file transformations objects
    for file_transformation in file_transformations:
        print(f'\n\nStarting {file_transformation["file_to_transform"]}')

        # Read in the file_to_transform file
        to_transform_df = pd.read_excel(
            f'original/{file_transformation["file_to_transform"]}')

        # sequentially loop through each column transformations objects
        for column_transformation in file_transformation['column_transformations']:

            # if this transformation is a simple transformation, then run it
            if column_transformation.get('transformation') == 'simple_transformation':

                # read in the file_with_name file
                if not column_transformation.get('isDelete'):
                    with_name_df = pd.read_excel(
                        f'original/{column_transformation["file_with_name"]}')

                # Run the simple transformation
                to_transform_df = simple_transformation(to_transform_df, with_name_df, column_transformation)
            else:
                try:
                    # Get the transformation function from the transformations_dict
                    to_transform_df = transformations_dict[column_transformation['transformation']](
                        to_transform_df)
                except Exception as e:
                    print(
                        f'\n\n    OH SHIT    \n\nError in {column_transformation}\nError was {e}\n\n')
            # Export the transformed file
            to_transform_df.to_excel(
                f'transformed/{file_transformation["export_file_name"]}', index=False)


def simple_transformation(to_transform_df, with_name_df, column_transformation):
    # return updated dataframe

    print(f"    Starting {column_transformation['column_to_transform']}")
    # print as json column_transformation
    print(f"    {json.dumps(column_transformation, indent=4)}")
    # If the column is to be deleted, delete it and continue to the next column transformation
    if column_transformation['isDelete']:
        print(f"    Deleting column: {column_transformation['column_to_transform']}")
        print(f"typeof to_transform_df[column_transformation['column_to_transform']]: {type(to_transform_df[column_transformation['column_to_transform']])}")
        del to_transform_df[column_transformation['column_to_transform']]
    else:
        # Create a dictionary to map ID to nerve/muscle names
        name_dict = with_name_df.set_index(
            column_transformation['primary_key'])[column_transformation['column_with_name']].to_dict()

        # Use the map function to replace the ID in the file_to_transform file with the corresponding nerve/muscle name
        to_transform_df[column_transformation['column_to_transform']] = to_transform_df[column_transformation['column_to_transform']].map(
            name_dict)
    return to_transform_df


def cases_diagnosis_diagnosis_transformation(to_transform_df):
    # Get "diag_name" from table "diagnoses names (to destroy)" where Diagnosis = "diag_name_id"
    # return updated dataframe
    print('running cases_diagnosis_diagnosis_transformation')

    # Read in the diagnoses names (to destroy) file
    diagnoses_names_df = pd.read_excel('original/diagnoses names (to destroy).xlsx')

    # Create a dictionary to map ID to diagnosis names
    name_dict = diagnoses_names_df.set_index('Diagnosis')['diag_name'].to_dict()

    # Use the map function to replace the ID in the file_to_transform file with the corresponding diagnosis name

    to_transform_df['Diagnosis'] = to_transform_df['Diagnosis'].map(name_dict)

    return to_transform_df


def cases_diagnosis_ncs_criteria_transformation(to_transform_df):
    # Get from table "diagnoses relations (to destroy)" columns ns_compounds and ns_logic
    # return updated dataframe
    print('running cases_diagnosis_ncs_criteria_transformation')

    # Read in the diagnoses relations (to destroy) file
    diagnoses_relations_df = pd.read_excel('original/diagnoses relations (to destroy).xlsx')

    # Create a dictionary to map ID to ncs criteria
    name_dict = diagnoses_relations_df.set_index('Diagnosis')['ns_compounds'].to_dict()

    # Use the map function to replace the ID in the file_to_transform file with the corresponding ncs criteria
    to_transform_df['Criteria'] = to_transform_df['Diagnosis'].map(name_dict)

    # Create a dictionary to map ID to ncs logic
    name_dict = diagnoses_relations_df.set_index('Diagnosis')['ns_logic'].to_dict()

    # Use the map function to replace the ID in the file_to_transform file with the corresponding ncs logic

    to_transform_df['Logic'] = to_transform_df['Diagnosis'].map(name_dict)

    return to_transform_df


def cases_diagnosis_emg_criteria_transformation(to_transform_df):
    # Get from table "diagnoses relations (to destroy)" columns ms_compounds and ms_logic
    # return updated dataframe
    print('would be running cases_diagnosis_emg_criteria_transformation')


def cases_differential_diagnosis_transformation(to_transform_df):
    # Get "diag_name" from table "diagnoses names (to destroy)" where Diagnosis = "diag_name_id"
    # return updated dataframe
    print('would be running cases_differential_diagnosis_transformation')


def cases_differential_criteria_transformation(to_transform_df):
    # Get from logic tab below
    # return updated dataframe
    print('would be running cases_differential_criteria_transformation')


def cases_main_cc_transformation(df_cases_main):
    # Use case_id to match item_id in table "cc relations", then get the actual name from table "cc names". Separate names by comma (i.e. "A, B, C")
    # return updated dataframe
    print('running cases_main_cc_transformation')

    # Load the "cc relations" table
    df_relations = pd.read_excel(f"original/cc relations.xlsx")

    # load the "cc names" table
    df_names = pd.read_excel(f"original/cc names.xlsx")

    # Create a dictionary to map ID to nerve/muscle names
    name_dict = df_names.set_index(
        'item_id')['item_name'].apply(str.strip).to_dict()

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

    # return the updated dataframe
    return df_cases_main


def muscles_main_root_transformation(to_transform_df):
    # Pull from table "muscles roots (to destroy)" matching ID. Separate multiple with comma, then add + for important = Y or - for important = N. Example for ID1: C6+, C5-
    # return updated dataframe
    print('would be running muscles_main_root_transformation')


def modules_main_cases_transformation(to_transform_df):
    # Create comma separated list by matching ID with "module_id" from table "module cases (to destroy)" and then grabbing "case_num" by matching "case_id" from table "cases main", ideally in the order specified by "case_order"
    # return updated dataframe
    print('would be running modules_main_cases_transformation')


def to_xlsx(file_name, sheet_name, df):
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()


def to_csv(file_name, df):
    df.to_csv(file_name, index=False)


if __name__ == '__main__':

    main()

    # # get from command line argument the desired output type
    # output_type = sys.argv[1]

    # # if output type is not csv or xlsx, exit
    # if output_type != 'csv' and output_type != 'xlsx':
    #     print('Invalid output type. Must only be "csv" or "xlsx"')
    #     exit()

    # cases_main_cc_transformation(
    #     "cases main.xlsx", "cc relations.xlsx", "cc names.xlsx", "cases main transformed.xlsx")
