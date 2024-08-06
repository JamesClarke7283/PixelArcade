# Plan for Pixel Arcade

When you first startup Pixel Arcade, you are greeted with a Menu, showing all the different list of games available, we render this list of games by looking in src/games/*, each package is a new game, if it has a `game.py` in the game folder we put it on the screen, the game tiles are rendered on the screen in customtkinter, each with the name of the game, also, we sort them in alphabetical order, in a grid, left to right, up to down, in a `8x8` grid. We store this `game_menu_grid_size` inside a `.config.toml` in the project root, we use the builtin `tomllib` library to read from it. When we click on the game tile, it asks you using a `CTkMessagebox`, if you want to start the game, if you click yes, it closes the launcher, and starts the game. each game is a `pygame` game.

## Project Structure
.
├── docs
│   └── PLAN.md
├── LICENSE
├── pyproject.toml
├── README.md
├── .config.toml - Contains all the constants for the program, we always keep code and data seperate here.
└── src
    ├── app.py  - The entrypoint to the launcher menu(Main Window).
    ├── components - All the GUI components for the Main Window.
    ├── core       - Core logic for the Main Window and the components.
    └── games      - Contains a directory for each game we make for PixelArcade.
        └── breakout  - An example game we make first in the first version
            └── game.py - This file is run, specifically the 'main' function, in order to play the given game.


## Extras

### Logging
Please use `python-dotenv` to load the `LOG_LEVEL` environment variable, also get the envvar from just the application run, in case its passed as a envvar like so `LOG_LEVEL=DEBUG pixelarcade` always convert the log level to uppercase in case they use lowercase, also store a log file with the datetime timestamp in British Date layout with a `.log` like so `2000-08-30_5-45-22.log` or (`pixelarcade_%Y-%m-%d_%H-%M-%S.log`) make sure you put the `log` file in an appropriate directory in the users home directory, use `appdirs` to figure out where to put it, the directory will be `PixelArcade` put the log files in that. Also add a new log level called `TRACE` and can be called with the `logger.trace` method, reserve using this for highly verbose logging(and please do use verbose logging throughout the application).

IT IS PARAMOUNT YOU ADD LOGGING AT DIFFERENT LEVELS, THROUGHOUT THE APPLICATION, THIS IS ESSENTIAL TO CATCH BUGS, INCLUDE LOGGING FOR BACKEND LOGIC AND FRONTEND GUI. ALSO PLEASE MAKE IT SO AT THE END OF THE LOG LINE IT SHOWS THE LINE AT WHICH THE FILE PATH LOGGER IS BEING CALLED FROM AND THE LINE NUMBER. ALSO MAKE SURE THE LOGGER IS COLOURISED, WITH DIFFERENT COLOUR CODES FOR DIFFERENT LOG LEVELS, BUT DO NOT INCLUDE THESE COLOUR CODES IN THE LOG FILE.

USE THE COLOREDLOGS PYPI PACKAGE TO MAKE LOGS COLORED.

### Error Handling
IT IS IMPORTANT THAT ANY ERROR THE APP THROWS SHOWS UP IN A TEXTBOX that can be copied to the CLIPBOARD, and pops up in both the GUI and the CONSOLE. THIS ENSURES WE CAN EASILY VIEW THE ERROR AND CORRECT IT. ALSO INCLUDE ROBUST ERROR HANDLING SO THAT MOST ERRORS HAVE HUMAN ERROR MESSAGES, FALLBACK TO A PRINTOUT OF THE RAW ERROR IF WE DONT HAVE A HUMAN ERROR.

### Themes
We need to have a Light and Dark theme, which is selected based on weather we are in dark or light mode on our OS, we use `darkdetect` for this.
THEME COLOURS MUST BE CONSISTENT THROUGHOUT THE APPLICATION AND WE READ ALL THEME OPTIONS FROM THE PROJECT DIRECTORIES `.config.toml` it will be in this format:

```toml
[appearance.theme.light]
background = "FFFFFF"
foreground = "000000"
primary = "0000FF"
secondary = "00FF00"
tertiary = "FF0000"

[appearance.theme.dark]
foreground = "FFFFFF"
background = "000000"
primary = "0000FF"
secondary = "00FF00"
tertiary = "FF0000"
```

We store the `config.toml` in the appropriate appdirs path, on linux it will be `~/.config/PixelArcade/config.toml`. if that file does not exist, we create it and fill it with the default config in the project root called `.config.toml`

## Planning Phases

We need to complete this program in phases.


### Phase 1: Making the launcher

Implement the launcher as described above, including logging, error handling, etc.

### Phase 2: Making the first game

We will make our first game: breakout, the classic arcade game. we will in the `games` folder have the `breakout` folder of course, and inside that we will have `components` (contains the components for all the game elements in pygame), `core` (the core logic of the game, put python files here for various parts of non pygame stuff like logic), and of course we will have the entrypoint `game.py`, which the launcher runs the `main` method inside of from the menu.
