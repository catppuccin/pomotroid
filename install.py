# #!/usr/bin/env python3
"""Installation script for installing Pomotroid theme files into the respective directories
corresponding to the user's operating system/file structure."""


import json
import os
from pathlib import Path
import sys

import appdirs
from catppuccin import Flavour
from prompt_toolkit import prompt as ptprompt
from prompt_toolkit.completion import WordCompleter
from rich import print as rprint
from rich.prompt import Confirm
from generate import generate_themes

themes = {
    "latte": Flavour.latte(),
    "mocha": Flavour.mocha(),
    "macchiato": Flavour.macchiato(),
    "frappe": Flavour.frappe(),
}

accents = [
    "Rosewater",
    "Flamingo",
    "Pink",
    "Mauve",
    "Red",
    "Maroon",
    "Peach",
    "Yellow",
    "Green",
    "Teal",
    "Sky",
    "Sapphire",
    "Blue",
    "Lavender",
]

config_dir = appdirs.user_config_dir("pomotroid", roaming=True, appauthor=False)
themes_dir = os.path.join(config_dir, "themes")


def get_theme(theme_name) -> str:
    """Prompt the user for the theme name and return it"""
    accent = ""
    completer = WordCompleter(list(accents), ignore_case=True)
    accent = ptprompt(f"Chosen accent color for {theme_name}: ", completer=completer)
    accent = accent.lower()
    if accent == "":
        accent = "red"
        print("Defaulting to red accent color")
    return accent


def main():
    """Iterate through the themes and create a theme file for each"""
    rprint(
        "[bold]Welcome to the Catppuccin Pomotroid theme installer![/bold]",
        end="\n\n",
    )

    if not Confirm.ask("Proceed with installing all four flavours?", default=True):
        sys.exit(1)

    accent = get_theme("all")

    files = generate_themes()
    for theme, accent_dict in files.items():
        files[theme] = {accent: accent_dict[accent]}

    for theme, base in files.items():
        for accent, value in base.items():
            for path, contents in value.items():
                path = Path(path).resolve().as_posix()
                path = path.split(f"dist/{accent}/", 1)[1]
                theme_path = Path(themes_dir) / path.replace(f"{accent}", "")
                theme_path = theme_path.resolve().as_posix()
                write_files(theme_path, contents)

    rprint("[bold]All themes installed![/bold]")
    rprint(f"[bold]Themes installed to: {themes_dir}[/bold]")


def write_files(theme_path, base):
    """Write the theme file to the specified path"""
    with open(theme_path, "w", encoding="utf-8") as baked_json:
        json.dump(base, baked_json, indent=4)


if __name__ == "__main__":
    main()
