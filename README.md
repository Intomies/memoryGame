# Memory Game 

This is a simple memory game made with python. It consists of few classes that handle the gameplay.

To run the game you first need to install requirements. Use ```pip install -r requirements.txt``` to install them.
Currently you also need to populate the ```./data/images/``` folder with following folders:

- /back/
    - This folder contains images that are rendered as the card backside images
- /front/
    - This folder contains the front side of the cards, e.g. what you are trying to find pairs of in the game. There should be atleast 32 unique images if you are playing with default settings. Alternatively, you can navigate to ```./utils/settings.py``` and edit the card amount in ```Cards.amount``` to change the number of rendered cards for the game. This will currently also affect the layout of the game, so no quarantee is given on what it will look like if the amount is changed.
- /main_menu/
    - This folder contains the background images for the main menu.
- /table/
    - This folder contains the background images for the game table.

In those folders you can put whatever images you want, but I suggest you use .png as the file format, as the game uses alpha channel in some parts. The ```./back```, ```./main_menu``` and ```./table``` folders must contain atleast one image each. For the ```./front``` folder 32 images is the optimal amount. 

The game can be started by running ```./main.py```

## What the game looks like

Here are some screenshots from the game. I used Minecraft-themed images as game graphics.

### Main screen
This is the main screen of the game. You can play by yourself, or with a friend.
![Main Menu](https://github.com/Intomies/memoryGame/blob/main/data/demo/main_menu.png)

### Player setup
You can give your player a name and choose your avatar.
![Player Setup](https://github.com/Intomies/memoryGame/blob/main/data/demo/player_setup.png)

### Avatar selection
All your favourite avatars are available (these are the same images that are used as playing cards).
![Avatar Select](https://github.com/Intomies/memoryGame/blob/main/data/demo/avatar_select.png)

### Gameplay screen
The game is filled with action packed memory game excitement!
![Gameplay](https://github.com/Intomies/memoryGame/blob/main/data/demo/gameplay.png)

### End screen
Game ends and the winner is announced when all the pairs have been found (or if you choose to end it early). 
![Game End](https://github.com/Intomies/memoryGame/blob/main/data/demo/game_end.png)
