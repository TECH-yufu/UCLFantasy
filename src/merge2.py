import pandas as pd
from fuzzywuzzy import process

# Load the first CSV file
df1 = pd.read_csv('src/data/UCLFantasyPlayers_knockout.csv')

# Load the second CSV file
df2 = pd.read_csv('player_stats.csv')

# Function to match name and return closest match
# Function to match name and return closest match
def match_name(name, list_names, min_score=0):
    # -1 score incase we don't get any matches
    max_score = -1
    # Returning empty name for no match as well
    max_name = ""
    # Iternating over all names in the other
    for name2 in list_names:
        #Finding fuzzy match score
        score = process.extractOne(name, [name2], score_cutoff=min_score)
        # Checking if we are above our threshold and have a better score
        if score and score[1] > max_score and name[0] == name2[0]:  # Check if the first letters match
            max_name = score[0]
            max_score = score[1]
    if not max_name:  # If no match was found, retry without the "name[0] == name2[0]" check
        for name2 in list_names:
            score = process.extractOne(name, [name2], score_cutoff=min_score)
            if score and score[1] > max_score:
                max_name = score[0]
                max_score = score[1]
    if max_name:  # Check if a match was found
        print(f"Matched {name} with {max_name} with a score of {max_score}")  # Print the match result
    else:
        print(f"No match found for {name}")
    return max_name, max_score

# List for dicts for easy dataframe creation
dict_list = []
# iterating over players names to get a match in second dataframe
for name in df1.playerName:
    # Use our method to find best match, we can set a threshold here
    match = match_name(name, df2.playerName, 70)
    
    # New dict for storing data
    dict_ = {}
    dict_.update({"playerName" : name})
    dict_.update({"match_name" : match[0]})
    dict_.update({"score" : match[1]})
    dict_list.append(dict_)
    
merge_table = pd.DataFrame(dict_list)
# Display results
print(merge_table)

# Merge the two DataFrames on the "match_name" column
merged_df = pd.merge(df1, merge_table, left_on='playerName', right_on='match_name')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged.csv', index=False)