import tkinter as tk
from tkinter import PhotoImage, Toplevel
import urllib.request
from PIL import Image, ImageTk
import io
import pandas as pd
import random
from tkVideoPlayer import TkinterVideo
import matplotlib.pyplot as plt

def get_player_image(image_url, image_width=100, image_height=100):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    raw_data = urllib.request.urlopen(urllib.request.Request(image_url, headers=headers)).read()
    
    im = Image.open(io.BytesIO(raw_data))
    
    # Resize the image to the desired size (e.g., 75x75 pixels)
    im = im.resize((image_width, image_height))  # Use Image.ANTIALIAS for high-quality resizing

    player_image = ImageTk.PhotoImage(im)
    
    return player_image

def pick_new_players():

    # Pick three new random players without repetitions
    Ns = random.sample(list(range(len(df))), 3)

    players_info = [get_player_info(idx) for idx in Ns]

    player_names = [player['Name'].lower() for player in players_info]

    for name in player_names:
        if "k. mbappé" == name:
            walkout(r"src/videos/mbappe.mkv")
            break
        elif "e. haaland" == name:
            walkout(r"src/videos/haaland.mkv")
            break

    # Update the buttons with the new players    
    update_button_info(option1_button, players_info[0])
    update_button_info(option2_button, players_info[1])
    update_button_info(option3_button, players_info[2])

def get_player_info(idx):
    return {
        "Name": f"{df.iloc[idx]['playerName']}",
        "Price": f"{df.iloc[idx]['playerPrice']}m €",
        "Position": f"{df.iloc[idx]['playerPos']}",
        "Club": f"{df.iloc[idx]['playerClub']}",
        "Image": f"{df.iloc[idx]['playerImg']}",
        "Total Points": f"{df.iloc[idx]['TotalPoints']}",
        "Goals": f"{df.iloc[idx]['Goals']}",
        "Assists": f"{df.iloc[idx]['Assists']}",
        "Balls Recovered": f"{df.iloc[idx]['BallsRecov']}"
    }

def update_button_info(button, player):
    button.config(text=f"{player['Name']}\nPrice: {player['Price']}\nPosition: {player['Position']}\nClub: {player['Club']}")
    player_image = get_player_image(player['Image'])
    if player_image:
        button.image = player_image
        button.config(image=player_image)
        button.config(command=lambda: show_player_info(player))

def show_player_info(player):
    info_label.config(text=f"Name: {player['Name']}\nPrice: {player['Price']}\nPosition: {player['Position']}\nClub: {player['Club']}\nTotal Points: {player['Total Points']}\nGoals: {player['Goals']}\nAssists: {player['Assists']}\nBalls Recovered: {player['Balls Recovered']}")

def close_video(win):
    win.destroy()

def walkout(video_path):
    window = tk.Toplevel()
    window.lift()

    window.state('zoomed')  # maximize the window

    player = TkinterVideo(master=window, scaled=True)
    player.load(video_path)
    player.pack(expand=True, fill="both")

    # Set the player size to the screen size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    player.set_size((screen_width, screen_height))

    window.attributes('-topmost', True)    

    window.after(25000, close_video, window) # close win after 20 sec
    player.bind("<<Ended>>", lambda event: close_video(window)) # close the win if video ended

    player.play() # play the video

df = pd.read_csv("src/data/UCLFantasyPlayers_knockout.csv") 
print(df.columns)

# Filter out players with price less than x
df = df.loc[df['playerPrice'] >= 10.0]

# Create the main window
root = tk.Tk()
root.title("Player Select Screen")

# Create a frame to center the buttons horizontally
center_frame = tk.Frame(root)
center_frame.pack(expand=True)

# Create clickable options with large rectangular buttons and images
button_width = 400
button_height = 200

option1_button = tk.Button(center_frame, width=button_width, height=button_height, compound=tk.TOP)
option2_button = tk.Button(center_frame, width=button_width, height=button_height, compound=tk.TOP)
option3_button = tk.Button(center_frame, width=button_width, height=button_height, compound=tk.TOP)

# Pack the buttons horizontally
option1_button.pack(side=tk.LEFT, padx=10)
option2_button.pack(side=tk.LEFT, padx=10)
option3_button.pack(side=tk.LEFT, padx=10)

# walkout animation

# players_info = pick_players()
# player_names = [player['Name'].lower() for player in players_info]

# if "mbappe" in player_names:
#     walkout()

# walkout()

# Create a label to display player information
info_label = tk.Label(root, text="", padx=10, pady=10)
info_label.pack()

# Pick initial players and update buttons
pick_new_players()

### play video here ###

# Button to pick new players
new_players_button = tk.Button(root, text="Pick New Players", command=pick_new_players)
new_players_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()

# if __name__ == "__main__":
#     df = pd.read_csv("src/data/UCLFantasyPlayers_knockout.csv") 

#     df = df.loc[df['playerPrice'] >= 5.0]

   