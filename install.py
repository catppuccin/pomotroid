# #!/usr/bin/env python3
"""Installation script for installing Pomotroid theme files into the respective directories
corresponding to the user's operating system/file structure."""


import json
import os
import sys

import appdirs
from catppuccin import Flavour
from prompt_toolkit import prompt as ptprompt
from prompt_toolkit.completion import WordCompleter
from rich import print as rprint
from rich.progress import track
from rich.prompt import Confirm

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


def main():
    """Iterate through the themes and create a theme file for each"""
    rprint(
        "[bold]Welcome to the Catppuccin Pomotroid theme installer![/bold]",
        end="\n\n",
    )

    if not Confirm.ask("Proceed with installing all four flavours?", default=True):
        sys.exit(1)
    accent = get_theme("all")

    for theme in track(themes, description="Creating theme files..."):
        base = {
            "name": f"Catppuccin {theme.title()}",
            "colors": {
                "--color-long-round": "#" + themes[theme].blue.hex,
                "--color-short-round": "#" + themes[theme].teal.hex,
                "--color-focus-round": "#" + themes[theme].red.hex,
                "--color-background": "#" + themes[theme].base.hex,
                "--color-background-light": "#" + themes[theme].mantle.hex,
                "--color-background-lightest": "#" + themes[theme].text.hex,
                "--color-foreground": "#" + themes[theme].text.hex,
                "--color-foreground-darker": "#" + themes[theme].subtext0.hex,
                "--color-foreground-darkest": "#" + themes[theme].subtext1.hex,
                "--color-accent": "#" + getattr(themes[theme], accent).hex,
            },
        }

        theme_file = f"catppuccin-{theme}.json"
        theme_path = os.path.join(themes_dir, theme_file)
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(theme_path), exist_ok=True)

        # Create file if it doesn't exist
        if not os.path.exists(theme_path):
            with open(theme_path, "x", encoding="utf-8") as baked_json:
                baked_json.close()

        # Write JSON data to file
        with open(theme_path, "w", encoding="utf-8") as baked_json:
            json.dump(base, baked_json, indent=4)
            baked_json.close()

    rprint("[bold]All done![/bold]")
    rprint("Installed themes can be found in:")
    rprint(f"[bold]{themes_dir}[/bold]")


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


if __name__ == "__main__":
    main()
