import pandas as pd

file_to_transform = 'cases abnormal muscles'
file_with_name = 'muscles main'

# Read in the file_to_transform file
cases_df = pd.read_excel(f"{file_to_transform}.xlsx")

# Read in the file_with_name file
nerves_df = pd.read_excel(f'{file_with_name}.xlsx')

# Create a dictionary to map ID to nerve/muscle names
name_dict = nerves_df.set_index('ID')['Name'].to_dict()

# Use the map function to replace the ID in the file_to_transform file with the corresponding nerve/muscle name
cases_df['Name'] = cases_df['Name'].map(name_dict)

# Save the modified file_to_transformed file
cases_df.to_excel(f"{file_to_transform} transformed.xlsx", index=False)
