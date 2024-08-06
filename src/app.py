import os
import sys
import tomllib
from typing import Dict, Any
import multiprocessing

import customtkinter as ctk
from appdirs import user_config_dir
import darkdetect
from CTkMessagebox import CTkMessagebox

from src.logging import get_logger
from src.games.breakout import game as breakout_game

logger = get_logger()

# Load configuration
CONFIG_DIR = user_config_dir("PixelArcade")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.toml")

if not os.path.exists(CONFIG_FILE):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "wb") as f:
        with open(".config.toml", "rb") as default_config:
            f.write(default_config.read())

with open(CONFIG_FILE, "rb") as f:
    config = tomllib.load(f)

class PixelArcade(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pixel Arcade")
        self.geometry("800x600")

        self.theme = "dark" if darkdetect.isDark() else "light"
        self.load_theme()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.game_frame = ctk.CTkFrame(self)
        self.game_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.load_games()

        self.game_processes = {}

    def load_theme(self):
        theme_config = config["appearance"]["theme"][self.theme]
        ctk.set_appearance_mode(self.theme)
        
        ctk.set_default_color_theme("blue")  # Use a default theme as a base
        
        self.configure(fg_color=f"#{theme_config['background']}")
        ctk.ThemeManager.theme["CTkButton"]["fg_color"] = f"#{theme_config['primary']}"
        ctk.ThemeManager.theme["CTkButton"]["hover_color"] = f"#{theme_config['secondary']}"
        ctk.ThemeManager.theme["CTkButton"]["text_color"] = f"#{theme_config['foreground']}"

    def load_games(self):
        games_dir = os.path.join(os.path.dirname(__file__), "games")
        games = [d for d in os.listdir(games_dir) if os.path.isdir(os.path.join(games_dir, d)) and os.path.exists(os.path.join(games_dir, d, "game.py"))]
        games.sort()

        grid_size = config["game_menu"]["grid_size"]
        for i, game in enumerate(games):
            row = i // grid_size
            col = i % grid_size
            game_button = ctk.CTkButton(self.game_frame, text=game, command=lambda g=game: self.start_game(g))
            game_button.grid(row=row, column=col, padx=5, pady=5)

    def start_game(self, game: str):
        logger.info(f"Starting game: {game}")
        msg = CTkMessagebox(title="Start Game", message=f"Do you want to start {game}?", icon="question", option_1="Yes", option_2="No")
        if msg.get() == "Yes":
            logger.info(f"User confirmed starting {game}")
            if game == "breakout":
                self.launch_game_process(breakout_game.main, game)
            else:
                logger.warning(f"Game {game} not implemented yet")
        else:
            logger.info(f"User cancelled starting {game}")

    def launch_game_process(self, game_func, game_name):
        if game_name in self.game_processes and self.game_processes[game_name].is_alive():
            logger.warning(f"Game {game_name} is already running")
            return

        process = multiprocessing.Process(target=game_func)
        process.start()
        self.game_processes[game_name] = process
        logger.info(f"Started {game_name} in a new process")

    def on_closing(self):
        for game_name, process in self.game_processes.items():
            if process.is_alive():
                logger.info(f"Terminating {game_name} process")
                process.terminate()
                process.join()
        self.destroy()

def main():
    try:
        app = PixelArcade()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as e:
        logger.exception("An error occurred in the main application:")
        error_message = f"An error occurred:\n\n{str(e)}\n\nPlease check the logs for more details."
        CTkMessagebox(title="Error", message=error_message, icon="cancel")
        print(error_message)

if __name__ == "__main__":
    multiprocessing.freeze_support()  # This is necessary for Windows
    main()