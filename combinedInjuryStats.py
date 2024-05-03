import pandas as pd

# Load the datasets
df_injuries = pd.read_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/cleaned_injuries.csv')
df_batting = pd.read_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/cleaned_batting.csv')
df_pitching = pd.read_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/cleaned_pitching.csv')


#rename column to player and year in batting and pitching files
df_batting.rename(columns={'Name': 'Player'}, inplace=True)
df_pitching.rename(columns={'Name': 'Player'}, inplace=True)

# Merge the dataframes on 'Player' and 'Year'
# Ensure that both DataFrames have 'Player' and 'Year' columns with the same data types
merged_batting_data = pd.merge(df_batting, df_injuries, on=['Player', 'Year'], how='left')
merged_pitching_data = pd.merge(df_pitching, df_injuries, on=['Player', 'Year'], how='left')
print(merged_batting_data)

# Define specific injury columns for batting data
injury_columns_batting = [col for col in merged_batting_data.columns if col in ['10-day DL', '15-day DL', '60-day DL', 'Day to Day']]

# Fill missing values with 0 in specified injury columns for batting data
merged_batting_data[injury_columns_batting] = merged_batting_data[injury_columns_batting].fillna(0)
merged_batting_data['Injured'] = (merged_batting_data[injury_columns_batting].sum(axis=1) > 0).astype(int).replace({1: 'Yes', 0: 'No'})


# Define specific injury columns for pitching data
injury_columns_pitching = [col for col in merged_pitching_data.columns if col in ['10-day DL', '15-day DL', '60-day DL', 'Day to Day']]

# Fill missing values with 0 in specified injury columns for pitching data
merged_pitching_data[injury_columns_pitching] = merged_pitching_data[injury_columns_pitching].fillna(0)
merged_pitching_data['Injured'] = (merged_pitching_data[injury_columns_pitching].sum(axis=1) > 0).astype(int).replace({1: 'Yes', 0: 'No'})

# Now each DataFrame should have their respective columns filled correctly

# Save the merged DataFrame to a new CSV file
merged_batting_data.to_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/merged_batting_data.csv', index=False)
merged_pitching_data.to_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/merged_pitching_data.csv', index=False)

