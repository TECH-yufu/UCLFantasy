import pandas as pd

# Load the first CSV file
df1 = pd.read_csv('src/data/UCLFantasyPlayers_knockout.csv')

# Load the second CSV file
df2 = pd.read_csv('player_stats.csv')

# Load the matched names CSV file
matched_names_df = pd.read_csv('matched_names.csv')

# Merge df1 with the matched names DataFrame
df1 = pd.merge(df1, matched_names_df, left_on='playerName', right_on='playerName')

# Merge df1 (now containing the matched names) with df2
merged_df = pd.merge(df1, df2, left_on='match_name', right_on='playerName')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged.csv', index=False)