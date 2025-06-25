
import pandas as pd
import os

folder_path = '/content/drive/My Drive/BridgeResearchProject/NBIDataCollected'
file_name = 'California2023.xlsx'
file_path = os.path.join(folder_path, file_name)


columns_to_load = [
    'DATE_OF_INSPECT_090', 'YEAR_BUILT_027', 'YEAR_RECONSTRUCTED_106',
    'ADT_029', 'YEAR_ADT_030', 'UNDWATER_LAST_DATE_093B',
    'FUTURE_ADT_114', 'RIGHT_CURB_MT_050B', 'LEFT_CURB_MT_050A',
    'STRUCTURE_LEN_MT_049', 'DECK_WIDTH_MT_052', 'PERCENT_ADT_TRUCK_109',
    'TRAFFIC_LANES_ON_028A', 'MAIN_UNIT_SPANS_045', 'MAX_SPAN_LEN_MT_048',
    'OPERATING_RATING_064', 'HIGHWAY_DISTRICT_002', 'DESIGN_LOAD_031',
    'STRUCTURE_KIND_043A', 'STRUCTURE_TYPE_043B', 'APPR_KIND_044A',
    'APPR_TYPE_044B', 'DECK_GEOMETRY_EVAL_068', 'DECK_STRUCTURE_TYPE_107',
    'SURFACE_TYPE_108A'
]
df = pd.read_excel(file_path, usecols=columns_to_load)

# Compute AGE
df['Age'] = 2000 + (df['DATE_OF_INSPECT_090'] % 100) - df['YEAR_BUILT_027']

# Reconstructed column
df['Reconstructed'] = df['YEAR_RECONSTRUCTED_106'].apply(lambda x: 0 if x == 0 else 1)

# Extract YI from inspection date
YI = pd.to_datetime(df['UNDWATER_LAST_DATE_093B'], errors='coerce').dt.year % 100

# Compute ADT
df['ADT'] = ((df['FUTURE_ADT_114'] - df['ADT_029']) /
             (df['FUTURE_ADT_114'] - df['YEAR_ADT_030'])) * (YI - df['YEAR_ADT_030']) + df['ADT_029']

# Compute Curb Width
df['Curb_Width'] = df['LEFT_CURB_MT_050A'] + df['RIGHT_CURB_MT_050B']

# Compute Deck Area
df['Deck_Area'] = df['STRUCTURE_LEN_MT_049'].fillna(0) * df['DECK_WIDTH_MT_052'].fillna(0)
# Rename remaining columns to match NBI Variable names
df.rename(columns={
    'PERCENT_ADT_TRUCK_109': 'ADTT',
    'TRAFFIC_LANES_ON_028A': 'Lanes_On',
    'MAIN_UNIT_SPANS_045': 'Number_Spans_Main',
    'MAX_SPAN_LEN_MT_048': 'Length_Max_Span',
    'OPERATING_RATING_064': 'Operating_Rating',
    'HIGHWAY_DISTRICT_002': 'Highway_District',
    'DESIGN_LOAD_031': 'Design_Load',
    'STRUCTURE_KIND_043A': 'Main_Material',
    'STRUCTURE_TYPE_043B': 'Main_Design',
    'APPR_KIND_044A': 'Spans_Material',
    'APPR_TYPE_044B': 'Spans_Design',
    'DECK_GEOMETRY_EVAL_068': 'Deck_Geometry',
    'DECK_STRUCTURE_TYPE_107': 'Deck_Type',
    'SURFACE_TYPE_108A': 'Wearing_Surface'
}, inplace=True)
# Select and order columns as in the image
ordered_columns = [
    'Age', 'ADT', 'ADTT', 'Lanes_On', 'Number_Spans_Main', 'Length_Max_Span',
    'Curb_Width', 'Deck_Area', 'Operating_Rating', 'Highway_District',
    'Design_Load', 'Reconstructed', 'Main_Material', 'Main_Design',
    'Spans_Material', 'Spans_Design', 'Deck_Geometry', 'Deck_Type',
    'Wearing_Surface'
]
final_df = df[ordered_columns]
