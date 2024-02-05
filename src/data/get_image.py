import urllib.request
from PIL import Image
import io

def get_player_image(image_url, image_width=150, image_height=150):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    raw_data = urllib.request.urlopen(urllib.request.Request(image_url, headers=headers)).read()
    
    im = Image.open(io.BytesIO(raw_data))
    
    # Resize the image to the desired size (e.g., 75x75 pixels)
    im = im.resize((image_width, image_height))  # Use Image.ANTIALIAS for high-quality resizing
    
    return im

# Example usage

if __name__ == "__main__":
    image_url = "https://img.uefa.com/imgml/TP/players/1/2024/75x75/250103758.jpg?v=4.07"
    im = get_player_image(image_url)
    im.show()  # Show the image in a new window