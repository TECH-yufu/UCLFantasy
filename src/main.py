import tkinter as tk
import urllib.request
from PIL import Image, ImageTk
import io
import pandas as pd
import random
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import vlc

class DraftSystem():

    def __init__(self, df):
        self.df = df
        self.walkout_dict = {"rúben dias": r"src\videos\dias.mp4",
                             "g. donnarumma": r"src\videos\donnarumma.mp4",
                             "k. mbappé": r"src\videos\mbappe.mp4",
                             "e. mbappe": r"src\videos\mbappe.mp4",
                             "e. haaland": r"src\videos\haaland.mp4",
                             "k. de bruyne": r"src\videos\kdb.mp4",
                             "t. kroos": r"src\videos\kroos.mp4",
                             "r. lewandowski": r"src\videos\lewandowski.mp4",
                             "marquinhos": r"src\videos\marquinhos.mp4",
                             "l. modrić": r"src\videos\modric.mp4",
                             "m. ødegaard": r"src\videos\odegaard.mp4",
                             "n. schlotterbeck": r"src\videos\schlotterbeck.mp4",
                             "m. ter stegen": r"src\videos\ter stegen.mp4",
                             "vinícius júnior": r"src\videos\vinicius.mp4",
                             "d. rice": r"src\videos\rice.mp4",
                             "j. álvarez": r"src\videos\alvarez.mp4",}

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Player Select Screen")

        # Create a frame to center the buttons horizontally
        self.center_frame = tk.Frame(self.root)
        self.center_frame.pack(expand=True)

        # Create clickable options with large rectangular buttons and images
        self.button_width = 400
        self.button_height = 200

        self.option1_button = tk.Button(self.center_frame, width=self.button_width, height=self.button_height, compound=tk.TOP)
        self.option2_button = tk.Button(self.center_frame, width=self.button_width, height=self.button_height, compound=tk.TOP)
        self.option3_button = tk.Button(self.center_frame, width=self.button_width, height=self.button_height, compound=tk.TOP)

        # Pack the buttons horizontally
        self.option1_button.pack(side=tk.LEFT, padx=10)
        self.option2_button.pack(side=tk.LEFT, padx=10)
        self.option3_button.pack(side=tk.LEFT, padx=10)

        # Create a label to display player information
        self.info_label = tk.Label(self.root, text="", padx=10, pady=10)
        self.info_label.pack()

        # Pick initial players and update buttons
        self.pick_new_players()

        # Button to pick new players
        self.new_players_button = tk.Button(self.root, text="Pick New Players", command=self.pick_new_players)
        self.new_players_button.pack(pady=10)

        # Start the Tkinter main loop
        self.root.mainloop()



    def get_player_image(self, image_url, image_width=100, image_height=100):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        raw_data = urllib.request.urlopen(urllib.request.Request(image_url, headers=headers)).read()
        
        im = Image.open(io.BytesIO(raw_data))
        
        # Resize the image to the desired size (e.g., 75x75 pixels)
        im = im.resize((image_width, image_height))  # Use Image.ANTIALIAS for high-quality resizing

        player_image = ImageTk.PhotoImage(im)
        
        return player_image
    
    def pick_new_players(self):

        # Pick three new random players without repetitions
        Ns = random.sample(list(range(len(self.df))), 3)

        players_info = [self.get_player_info(idx) for idx in Ns]

        player_names = [player['Name'].lower() for player in players_info]

        for name in player_names:
            if name in self.walkout_dict.keys():
                self.walkout(self.walkout_dict[name])
                break
           

        # Update the buttons with the new players    
        self.update_button_info(self.option1_button, players_info[0])
        self.update_button_info(self.option2_button, players_info[1])
        self.update_button_info(self.option3_button, players_info[2])

    def get_player_info(self,idx):
        return {
            "Name": f"{self.df.iloc[idx]['playerName']}",
            "Price": f"{self.df.iloc[idx]['playerPrice']}m €",
            "Position": f"{self.df.iloc[idx]['playerPos']}",
            "Club": f"{self.df.iloc[idx]['playerClub']}",
            "Image": f"{self.df.iloc[idx]['playerImg']}",
            "Total Points": f"{self.df.iloc[idx]['TotalPoints']}",
            "Goals": f"{self.df.iloc[idx]['Goals']}",
            "Assists": f"{self.df.iloc[idx]['Assists']}",
            "Balls Recovered": f"{self.df.iloc[idx]['BallsRecov']}"
    }

    def update_button_info(self, button, player):
        button.config(text=f"{player['Name']}\nPrice: {player['Price']}\nPosition: {player['Position']}\nClub: {player['Club']}")
        player_image = self.get_player_image(player['Image'])
        if player_image:
            button.image = player_image
            button.config(image=player_image)
            button.config(command=lambda: self.show_player_info(player))

    def show_player_info(self, player):
        self.info_label.config(text=f"Name: {player['Name']}\nPrice: {player['Price']}\nPosition: {player['Position']}\nClub: {player['Club']}\nTotal Points: {player['Total Points']}\nGoals: {player['Goals']}\nAssists: {player['Assists']}\nBalls Recovered: {player['Balls Recovered']}")

    def get_handle(self, window):
        return window.winfo_id()

    def walkout(self, video_path):
        # create window
        window = tk.Toplevel()
        window.lift()

        window.state('zoomed')  # maximize the window

        window.attributes('-topmost', True)    

        # play video
        instance = vlc.Instance()
        player = instance.media_player_new()

        Media = instance.media_new(video_path)
        Media.get_mrl()
        player.set_media(Media)

        player.set_hwnd(self.get_handle(window))
        player.toggle_fullscreen()

        player.play()


if __name__ == "__main__":
    df = pd.read_csv("src/data/UCLFantasyPlayers_knockout.csv") 
    print(df.columns)

    # Filter out players with price less than x
    df = df.loc[df['playerPrice'] >= 4.0]
    df = df.loc[df['TotalPoints'] > 0]

    draft = DraftSystem(df)