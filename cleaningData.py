import pandas as pd
import re

# Load the datasets
df_injuries = pd.read_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/injury_pivot.csv')
df_batting = pd.read_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/PLayerBatterStats.csv')
df_pitching = pd.read_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/PLayerPitcherStats.csv')


def standardize_name(name):
    if isinstance(name, str):
        name = re.sub(r"\s*\([^)]*\)", "", name)
        name = name.replace("•", "").strip()
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[-1]}, {' '.join(parts[:-1])}"
        return name
    return None


def extract_and_remove_parentheses(text):
    """Extracts content within parentheses and cleans the original string."""
    if isinstance(text, str):
        content = re.findall(r"\(([^)]+)\)", text)
        cleaned_text = re.sub(r"\s*\([^)]*\)", "", text).strip()
        return cleaned_text, ', '.join(content) if content else None
    return text, None


# Apply functions to the 'Relinquished' and 'Notes' columns
df_injuries['Player'] = df_injuries['Player'].apply(standardize_name)
#df_injuries[['cleaned_notes', 'designation']] = df_injuries['Notes'].apply(
   # lambda x: pd.Series(extract_and_remove_parentheses(x)))


# Ensure the year in batting and pitching datasets are integers
df_batting['Year'] = df_batting['Year'].astype(int)
df_pitching['Year'] = df_pitching['Year'].astype(int)


#saved stats and merged .csv files
df_injuries.to_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/cleaned_injuries.csv', index=False)
df_batting.to_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/cleaned_batting.csv', index=False)
df_pitching.to_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/cleaned_pitching.csv', index=False)
