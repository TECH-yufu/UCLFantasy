import pygame
import sys
import csv
import random
import Player
import pandas as pd
import requests
import io
from PIL import Image
import urllib.request

import tkinter as tk
from tkinter import PhotoImage, Toplevel
import urllib.request
from PIL import Image, ImageTk
import io
import pandas as pd
import random

# Initialize Pygame
pygame.init()

# Set the size of the window
screen_width, screen_height = 1000, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the FIFA card images
fifa_card_gold = pygame.image.load('src/cards/gold.png')
fifa_card_silver = pygame.image.load('src/cards/silver.png')
fifa_card_bronze = pygame.image.load('src/cards/bronze.png')

# Create a font object
font = pygame.font.Font(None, 36)  # Use the default font and a size of 36
large_font = pygame.font.Font(None, 72)  # Use the default font and a size of 72

# Initialize the position for the first card and the spinning state
position = screen_width + 100  # Start the cards off the screen
spinning = True
speed = screen_width // 200  # Set the speed to 1/200 of the screen width

# Set the FPS limit
clock = pygame.time.Clock()
FPS = 60

def load_players():
    players = []
    df = pd.read_csv("merged.csv")
    for index, row in df.iterrows():
        players.append(Player.player(row['playerName_x'], row['playerPrice'], row['playerPos'], row['playerClub'], row['playerImg_x'], row['OverallRating'], row['Pace'], row['Shooting'], row['Passing'], row['Dribbling'], row['Defending'], row['Physicality'], row['TeamImg'], row['FlagImg']))
    return players

class ImageManager:
    def __init__(self):
        self._images = {}

    def get_image(self, url):
        if url not in self._images:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            raw_data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
            
            im = Image.open(io.BytesIO(raw_data))
            self._images[url] = pygame.image.fromstring(im.tobytes(), im.size, im.mode)
        
        return self._images[url]

image_manager = ImageManager()

class Card:
    def __init__(self, player, font, large_font, fifa_card_silver, fifa_card_gold, fifa_card_bronze):
        self.player = player
        self.card_width = screen_width // 3
        self.card_height = screen_height
        self.font = font
        self.large_font = large_font
        self.fifa_card_silver = fifa_card_silver
        self.fifa_card_gold = fifa_card_gold
        self.fifa_card_bronze = fifa_card_bronze
        self.card_image = self.get_card_image()
        self.name_surface = self.get_name_surface()
        self.stats_surface = self.get_stats_surface()
        self.rating_surface = self.get_rating_surface()
        self.position_surface = self.get_position_surface()
        

    def get_card_image(self):
        if 65 <= int(self.player.overall) <= 74:
            card_image = self.fifa_card_silver
        elif int(self.player.overall) > 74:
            card_image = self.fifa_card_gold
        else:
            card_image = self.fifa_card_bronze
        return pygame.transform.scale(card_image, (self.card_width, self.card_height))
    
    

    def get_name_surface(self):
        return self.font.render(self.player.name, True, (0, 0, 0))

    def get_stats_surface(self):
    # Split the stats into three rows and exclude the overall stat
        stats_text1 = f"    {str(self.player.pace)[:2]} PAC          {str(self.player.dribbling)[:2]} DRI "
        stats_text2 = f"    {str(self.player.shooting)[:2]} SHO          {str(self.player.defending)[:2]} DEF "
        stats_text3 = f"    {str(self.player.passing)[:2]} PAS          {str(self.player.physicality)[:2]} PHY "
        
        # Render each row of stats as a separate surface
        stats_surface1 = self.font.render(stats_text1, True, (0, 0, 0))
        stats_surface2 = self.font.render(stats_text2, True, (0, 0, 0))
        stats_surface3 = self.font.render(stats_text3, True, (0, 0, 0))
    
        return stats_surface1, stats_surface2, stats_surface3

    def get_rating_surface(self):
        return self.large_font.render(str(self.player.overall), True, (0, 0, 0))

    def get_position_surface(self):
        return self.font.render(f"{self.player.position}", True, (0, 0, 0))
    
    def get_picture_surface(self):
        im = image_manager.get_image(self.player.picture_uri)
        im = pygame.transform.scale(im, (im.get_width() * 2, im.get_height() * 2))  # Double the size of the player image
        return im

    def get_club_image_surface(self):
        im = image_manager.get_image(self.player.clubImg)
        im = pygame.transform.scale(im, (im.get_width() // 2, im.get_height() // 2))  # Resize the club image
        return im

    def get_country_image_surface(self):
        im = image_manager.get_image(self.player.contryImg)
        im = pygame.transform.scale(im, (im.get_width() // 2, im.get_height() // 2))  # Resize the country image
        return im
    
    def get_price_surface(self):
        return self.font.render(f"price: {self.player.price}", True, (0, 0, 0))


    

def main():
    players = load_players()
    players = random.sample(players, 100)
    cards = [Card(player, font, large_font, fifa_card_silver, fifa_card_gold, fifa_card_bronze) for player in players]
    current_cards = [random.choice(cards) for _ in range(5)]  # Select 3 random cards

    screen_width, screen_height = 800, 600
    position = screen_width + 100  # Start the cards off the screen
    speed = screen_width // 20
    spinning = True

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # New event handler for mouse click
                if spinning:
                    spinning = False  # Stop spinning when the mouse is clicked
                elif spinning == False:
                    # Check if the click is inside any of the cards
                    print("here")
                    mouse_pos = pygame.mouse.get_pos()
                    for i, card in enumerate(current_cards):
                        card_x = start_x + i * (card.card_image.get_width() + 10)
                        card_y = 0
                        card_width = card.card_image.get_width()
                        card_height = card.card_image.get_height()
                        if card_x <= mouse_pos[0] <= card_x + card_width and card_y <= mouse_pos[1] <= card_y + card_height:
                            print(card.player.name)
                            cards.remove(card)
                            speed = screen_width // 20
                            spinning = True
                            break
            elif event.type == pygame.KEYDOWN:  # New event handler for key press
                if event.key == pygame.K_ESCAPE:  # If the ESC key is pressed
                    pygame.quit()
                    sys.exit()

        # Fill the screen with a black color
        screen.fill((0, 0, 0))

        if spinning or speed > 1:
            for i, current_card in enumerate(current_cards):
                # Calculate the positions of the cards and draw them onto the screen
                x = position + i * (current_card.card_image.get_width() + 20)  # Calculate the x-coordinate
                y = screen_height / 2 - current_card.card_image.get_height() / 2  # Calculate the y-coordinate
                if x + current_card.card_image.get_width() > -100:  # Only draw the card if it's within the visible area
                    screen.blit(current_card.card_image, (x, y))  # Draw the card

            # Decrease the position for the next frame
            position -= speed  # Move to the next card

            # Decelerate the cards when not spinning
            if not spinning:
                speed = max(0, speed - speed / 100)  # Decrease the speed by 1/100 of the original speed each frame

            # If the first card is out of the screen, remove it and add a new one
            if position + current_cards[0].card_image.get_width() < 0:
                position += current_cards[0].card_image.get_width() + 20
                current_cards.pop(0)
                ranodm_card = random.choice(cards)
                #while ranodm_card.player.price < 0 and ranodm_card not in current_cards:
                #    ranodm_card = random.choice(cards)
                current_cards.append(ranodm_card)  # Add a new random card
        else:
            
            # Draw the last cards onto the screen
            start_x = 0  # Calculate the starting x-coordinate for the first card
            for i, current_card in enumerate(current_cards):
                screen.blit(current_card.card_image, (start_x + i * (current_card.card_image.get_width() + 10), 0))
                # Blit the name surface onto the card
                name_surface = current_card.get_name_surface()
                name_x = start_x + i * (current_card.card_image.get_width() + 10) + current_card.card_image.get_width() // 2 - name_surface.get_width() // 2
                screen.blit(name_surface, (name_x, 330)) # Position the name at (10, 10) on the card
                # Blit the three stats surfaces onto the card at 2/3 of the card's height
                stats_surface1, stats_surface2, stats_surface3 = current_card.get_stats_surface()
                stats_y = int(2 / 3 * current_card.card_image.get_height())
                screen.blit(stats_surface1, (start_x + i * (current_card.card_image.get_width() + 20) + 10, stats_y-10))
                screen.blit(stats_surface2, (start_x + i * (current_card.card_image.get_width() + 20) + 10, stats_y + stats_surface1.get_height()+20))
                screen.blit(stats_surface3, (start_x + i * (current_card.card_image.get_width() + 20) + 10, stats_y + stats_surface1.get_height() + stats_surface2.get_height()+45))
                # Blit the rating surface onto the card top left
                screen.blit(current_card.get_rating_surface(), (start_x + i * (current_card.card_image.get_width() + 10) + 40, 70))
                # Blit the position surface onto the card top right
                    # Blit the position surface onto the card top right
                screen.blit(current_card.get_position_surface(), (start_x + i * (current_card.card_image.get_width() + 10) + 40, 120))

                # Blit the country image under the position
                country_image = current_card.get_country_image_surface()
                screen.blit(country_image, (start_x + i * (current_card.card_image.get_width() + 10) + 40, 120 + current_card.get_position_surface().get_height() + 10))

                # Blit the club image under the country
                club_image = current_card.get_club_image_surface()
                screen.blit(club_image, (start_x + i * (current_card.card_image.get_width() + 10) + 40, 120 + current_card.get_position_surface().get_height() + country_image.get_height() + 20))

                # Blit the picture onto the card
                #screen.blit(current_card.get_picture_surface(), (start_x + i * (current_card.card_image.get_width() + 10) + 130, 121))
                            # Blit the picture onto the card
                screen.blit(current_card.get_picture_surface(), (start_x + i * (current_card.card_image.get_width() + 10) + 150, 140))
                #add price top right corner
                screen.blit(current_card.get_price_surface(), (start_x + i * (current_card.card_image.get_width() + 10) + 190, 50))

        # Update the display
        pygame.display.flip()

        # Limit the FPS
        clock.tick(FPS)

if __name__ == "__main__":
    main()