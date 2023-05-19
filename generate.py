# #!/usr/bin/env python3
"""Generation script for generating Pomotroid theme
files and saving them to a dist"""


import json
import os

from catppuccin import Flavour

themes = {
    "latte": Flavour.latte(),
    "mocha": Flavour.mocha(),
    "macchiato": Flavour.macchiato(),
    "frappe": Flavour.frappe(),
}

accents = [
    "rosewater",
    "flamingo",
    "pink",
    "mauve",
    "red",
    "maroon",
    "peach",
    "yellow",
    "green",
    "teal",
    "sky",
    "sapphire",
    "blue",
    "lavender",
]

files = {}


def generate_themes():
    """Iterate through the themes and create a theme file for each"""

    for accent in accents:
        for theme, flavour in themes.items():
            base = {
                "name": f"Catppuccin {theme.title()}",
                "colors": {
                    "--color-long-round": "#" + flavour.blue.hex,
                    "--color-short-round": "#" + flavour.teal.hex,
                    "--color-focus-round": "#" + flavour.red.hex,
                    "--color-background": "#" + flavour.base.hex,
                    "--color-background-light": "#" + flavour.mantle.hex,
                    "--color-background-lightest": "#" + flavour.text.hex,
                    "--color-foreground": "#" + flavour.text.hex,
                    "--color-foreground-darker": "#" + flavour.subtext0.hex,
                    "--color-foreground-darkest": "#" + flavour.subtext1.hex,
                    "--color-accent": "#" + getattr(flavour, accent).hex,
                },
            }
            theme_file = f"catppuccin-{accent}-{theme}.json"
            theme_path = os.path.join("dist", accent, theme_file)

            if theme not in files:
                files[theme] = {}
            if accent not in files[theme]:
                files[theme][accent] = {}
            files[theme][accent][theme_path] = base

    return files


def write():
    """Write the theme files to the specified path"""

    for content in files.values():
        for theme in content.values():
            for path, json_theme in theme.items():
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as baked_json:
                    json.dump(json_theme, baked_json, indent=4)


if __name__ == "__main__":
    generate_themes()
    write()
