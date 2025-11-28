# filepath: d:\Modulo12\pygame\src\utils\loader.py
import pygame
import os

def load_image(name):
    # Get the directory of this file (src/utils/loader.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to 'pygame' root (src/utils -> src -> pygame)
    project_root = os.path.dirname(os.path.dirname(current_dir))
    # Construct path to assets/images
    fullname = os.path.join(project_root, 'assets', 'images', name)
    
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(f"Cannot load image: {name}")
        print(f"Expected path: {fullname}")
        raise SystemExit(message)
    
    return image.convert_alpha()