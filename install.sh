#!/bin/bash

# Variables
THEMES_DIR=""
ACCENT=""

# Prompt user for accent color
echo "What is your desired accent color? (Rosewater, Flamingo, Pink, Mauve, Red, Maroon, Peach, Yellow, Green, Teal, Blue, Sapphire, Sky, Lavender, Gray)"
read -p "> " ACCENT

# Force all lowercase for $ACCENT
ACCENT=$(echo "$ACCENT" | tr '[:upper:]' '[:lower:]')

# List of theme names
THEMES=("mocha" "macchiato" "frappe" "latte")

# Loop through each theme
for THEME in "${THEMES[@]}"; do
    # Read accent color hex code from JSON file by accessing the [$THEME] object and the [$ACCENT] property's hex value
    HEX=$(jq -r ".$THEME.$ACCENT.hex" palette.json)

    # Check if hex code is valid
    if ! [[ $HEX =~ ^#[0-9a-fA-F]{6}$ ]]; then
        echo "Invalid accent color"
        echo "got $HEX"
        exit 1
    fi

    # Replace accent color in theme file
    sed "s|<accent>|$HEX|g" theme.json >"catppuccin-$THEME.json"

    # Replace theme name in theme file
    sed "s|<theme>|$THEME|g" "catppuccin-$THEME.json" >"temp.json" && mv "temp.json" "catppuccin-$THEME.json"

    # Replace placeholders in theme file
    grep -o '<[^>]*>' "catppuccin-$THEME.json" | tr '\n' '\0' | while IFS= read -r -d '' VAR; do
        # Extract the variable name from the placeholder
        COLOR="$(echo "$VAR" | sed 's/<\(.*\)>/\1/')"

        # Get the hex code from the JSON file
        HEX=$(jq -r ".$THEME.$COLOR.hex" "palette.json")

        # Replace the placeholder with the hex code
        sed "s|$VAR|$HEX|g" "catppuccin-$THEME.json" >"temp.json" && mv "temp.json" "catppuccin-$THEME.json"
    done

    # Determine appData directory based on operating system
    case "$(uname -s)" in
    Linux*) THEMES_DIR="$HOME/.config/pomotroid/themes" ;;
    Darwin*) THEMES_DIR="$HOME/Library/Application Support/pomotroid/themes" ;;
    CYGWIN*) THEMES_DIR="$APPDATA/pomotroid/themes" ;;
    MINGW*) THEMES_DIR="$APPDATA/pomotroid/themes" ;;
    *)
        echo "Unsupported operating system"
        exit 1
        ;;
    esac

    # Copy theme file to themes directory
    cp "catppuccin-$THEME.json" "$THEMES_DIR"

    echo "New theme file created: catppuccin-$THEME.json"
    echo "Theme file copied to $THEMES_DIR"
    # delete catppuccin-$THEME.json
    rm "catppuccin-$THEME.json"
done

echo "Thank you for using Pomotroid Catppuccin! Have a productive yet soothing session! :)"
