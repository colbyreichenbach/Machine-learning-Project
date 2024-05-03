import pandas as pd

# Load the data
df = pd.read_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/mlb_injury_transactionsv1.csv')
# Convert dates to pandas datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Normalize the player names into a single column
df['Player'] = df['Relinquished'].fillna(df['Acquired'])

# Determine if it's an injury or return
df['Status'] = df.apply(lambda x: 'Injury' if pd.notna(x['Relinquished']) else 'Return', axis=1)

# Sort by player and date to ensure the order is correct
df = df.sort_values(by=['Player', 'Date'])

# Create a list to store DataFrame rows
injury_rows = []

# Loop through each player
for player in df['Player'].unique():
    player_data = df[df['Player'] == player]
    injuries = player_data[player_data['Status'] == 'Injury']
    returns = player_data[(player_data['Status'] == 'Return') & (player_data['Notes'].str.contains('returned to lineup'))]

    for i, injury in injuries.iterrows():
        return_entry = returns[returns['Date'] > injury['Date']].iloc[0] if not returns[returns['Date'] > injury['Date']].empty else None
        if return_entry is not None:
            days_injured = (return_entry['Date'] - injury['Date']).days
            if days_injured <= 10:
                injury_type = 'Day to Day'  # Assuming you meant "Day to Day" for <=10 days
            elif 10 < days_injured <= 15:
                injury_type = '10-day DL'
            elif 15 < days_injured <= 60:
                injury_type = '15-day DL'
            elif days_injured > 60:
                injury_type = '60-day DL'


            injury_rows.append({
                'Player': player,
                'Injury Date': injury['Date'],
                'Return Date': return_entry['Date'],
                'Days Injured': days_injured,
                'Injury Type': injury_type
            })

# Convert list of dicts to DataFrame
injury_classification = pd.DataFrame(injury_rows)

# Define the data types correctly
injury_classification['Injury Date'] = pd.to_datetime(injury_classification['Injury Date'])
injury_classification['Return Date'] = pd.to_datetime(injury_classification['Return Date'])
injury_classification['Days Injured'] = injury_classification['Days Injured'].astype(int)


# Save or display the result
injury_classification.to_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/injury_classification.csv', index=False)


# Create DataFrame
df = injury_classification

# Convert 'Injury Date' to datetime and extract year
df['Injury Date'] = pd.to_datetime(df['Injury Date'])
df['Year'] = df['Injury Date'].dt.year

# Group by player, year, and injury type and count occurrences
grouped = df.groupby(['Player', 'Year', 'Injury Type']).size().reset_index(name='Count')

# Pivot the data to have columns for each injury type
pivot_table = grouped.pivot_table(index=['Player', 'Year'], columns='Injury Type', values='Count', fill_value=0)

# Ensure all categories are present
required_categories = ['Day to Day', '10-day DL', '15-day DL', '60-day DL']
for category in required_categories:
    if category not in pivot_table.columns:
        pivot_table[category] = 0

# Order columns as per the requirement
pivot_table = pivot_table[required_categories]

# Flatten the columns after pivoting
pivot_table.columns = [f"{col}" if col else 'Total' for col in pivot_table.columns]  # Flatten the columns

pivot_table.to_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/injury_pivot.csv', index=True)

