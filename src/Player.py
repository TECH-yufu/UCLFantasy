import pandas as pd 

# Load the first CSV file



class player:
    def __init__(self, name, price,position,short_club,picture_uri, overall, pace, shooting, passing, dribbling, defending, physicality,clubImg,contryImg):
        self.name = name
        self.price = price
        self.position = position
        self.short_club = short_club
        self.picture_uri = picture_uri
        self.overall = overall
        self.pace = pace
        self.shooting = shooting
        self.passing = passing
        self.dribbling = dribbling
        self.defending = defending
        self.physicality = physicality
        self.clubImg = clubImg
        self.contryImg = contryImg

    def __str__(self):
        return f"{self.name} has an overall rating of {self.overall} and a pace of {self.pace}"

    def __repr__(self):
        return f"Player({self.name}, {self.overall}, {self.pace}, {self.shooting}, {self.passing}, {self.dribbling}, {self.defending}, {self.physicality})"
    


if __name__ == "__main__":
    df1 = pd.read_csv('merged.csv')

    players = []
    for index, row in df1.iterrows():
        players.append(player(row['playerName_y'], row['playerPrice'], row['playerPos'], row['playerClub'], row['playerImg'], row['OverallRating'], row['Pace'], row['Shooting'], row['Passing'], row['Dribbling'], row['Defending'], row['Physicality']))
