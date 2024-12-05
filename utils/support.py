from inspect import stack
from os import walk
from pygame import Surface
from pygame.image import load as load_image
from typing import List, Optional, Union

def get_graphics_images_from_folder(folder_path: str) -> Optional[List[Surface]]:
    try:
        images: list[Surface] = list()
        
        for _, __, img_files in walk(folder_path):
            for image in img_files:
                image_path: str = f'{folder_path}/{image}'
                image_surface: Surface = load_image(image_path).convert_alpha()
                images.append(image_surface)
                
        return images
                
    except Exception as error:
        error_name: str = type(error).__name__
        print(f'[Exception]::[{error_name} occured in import_graphics_images_from_folder: {error}]')
        for item in stack():
            print(item.function)
        return None