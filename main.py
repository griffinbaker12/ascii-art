import os
from math import ceil
from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)

# ASCII characters mapping
# 2 sets for different flavors
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " ", "░", "▒", "▓", "█"]
ASCII_CHARS_2 =  [' ','.',':','-','=','+','*','#','%','@'] 

IMAGE_PATH = "YOUR_FILE_PATH_HERE"
PIL_GRAYSCALE = 'L'
PIL_WIDTH_INDEX = 0
PIL_HEIGHT_INDEX = 1

# Common fonts for different systems
COMMON_MONO_FONT_FILENAMES = [
    '/System/Library/Fonts/Menlo.ttc'  # Update this to the correct path
]

# Resize the image for ASCII conversion
def resize_image(image, new_width=350):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.5)  # Adjust for aspect ratio
    return image.resize((new_width, new_height))

# Grayscale conversion
def grayscale_image(image):
    return image.convert("L")

# Open the image file
def open_image(image_path):
    try:
        return Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")

# Convert pixel values to ASCII characters
num_chars = len(ASCII_CHARS)
def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel_value in pixels:
        ascii_str += ASCII_CHARS[pixel_value * num_chars // 256]  # Map pixel to character
    return ascii_str

# Convert image to ASCII art
def image_to_ascii(image):
    image = resize_image(image)
    image = grayscale_image(image)
    ascii_str = pixel_to_ascii(image)
    img_width = image.width
    ascii_img = "\n".join([ascii_str[i:(i + img_width)] for i in range(0, len(ascii_str), img_width)])
    return ascii_img

# Save the ASCII art as PNG
def ascii_to_image(ascii_art, output_image_path):
    lines = ascii_art.split('\n')

    font = None
    large_font = 50  # Increased the font size for better resolution
    for font_filename in COMMON_MONO_FONT_FILENAMES:
        try:
            font = ImageFont.truetype(font_filename, size=large_font)
            print(f'Using font "{font_filename}".')
            break
        except IOError:
            print(f'Could not load font "{font_filename}". Trying next.')
    if font is None:
        font = ImageFont.load_default()
        print('Using default font.')

    # Calculate image size based on ASCII art
    font_points_to_pixels = lambda pt: round(pt * 96.0 / 72)
    margin_pixels = 30  # Increased margin for better spacing

    # Estimate the image size using font.getbbox()
    def get_text_size(text):
        bbox = font.getbbox(text)
        return bbox[2], bbox[3]  # width and height from bounding box

    tallest_line = max(lines, key=lambda line: get_text_size(line)[PIL_HEIGHT_INDEX])
    max_line_height = font_points_to_pixels(get_text_size(tallest_line)[PIL_HEIGHT_INDEX])
    image_height = int(ceil(max_line_height * len(lines) + 2 * margin_pixels))
    widest_line = max(lines, key=lambda s: get_text_size(s)[PIL_WIDTH_INDEX])
    image_width = int(ceil(get_text_size(widest_line)[PIL_WIDTH_INDEX] + (2 * margin_pixels)))

    # Create an RGBA image for the ASCII art with transparent background
    image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))  # 0 = full transparency
    draw = ImageDraw.Draw(image)

    # Draw the ASCII art onto the image
    font_color = (0, 0, 0, 255)  # Black text with full opacity
    horizontal_position = margin_pixels
    for i, line in enumerate(lines):
        vertical_position = int(round(margin_pixels + (i * max_line_height)))
        draw.text((horizontal_position, vertical_position), line, fill=font_color, font=font)

    # Save the generated image with transparent background
    image.save(output_image_path, "PNG")
    print(f"ASCII art saved as image: {output_image_path}")

# Main function
def main():
    # ASCII art conversion of the image
    img = open_image(IMAGE_PATH)
    ascii_art = image_to_ascii(img)

    # Save ASCII art as a PNG image
    ascii_to_image(ascii_art, './ascii_art.png')

    print(ascii_art)

if __name__ == "__main__":
    main()
