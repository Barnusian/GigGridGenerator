#!/bin/bash

# ---- CONFIG ----
PROJECT_DIR="$PWD"      # must be run from project root
PYTHON_VENV=".venv"
APP_NAME="GigGridGenerator"
ICON_FILE="grid.icns"
REQUIREMENTS="requirements.txt"
ENTRY_POINT="app.py"
PYTHON_VERSION="3.11"

# ---- 1. Install Homebrew if missing ----
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found, installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# ---- 2. Install Python 3.11 + Tkinter if missing ----
if ! brew list python@$PYTHON_VERSION &> /dev/null; then
    echo "Python $PYTHON_VERSION not found, installing..."
    brew install python@$PYTHON_VERSION
    brew install python-tk@$PYTHON_VERSION
fi

# Use Homebrew's symlink to Python 3.11
PYTHON_BIN="/opt/homebrew/bin/python${PYTHON_VERSION}"
PIP_BIN="/opt/homebrew/bin/pip${PYTHON_VERSION}"

# ---- 3. Create and activate virtual environment ----
if [ ! -d "$PYTHON_VENV" ]; then
    $PYTHON_BIN -m venv "$PYTHON_VENV"
fi
source "$PYTHON_VENV/bin/activate"

# ---- 4. Install dependencies ----
$PIP_BIN install --upgrade pip
$PIP_BIN install -r "$REQUIREMENTS"

# ---- 4a. Ensure Pillow is installed for icon handling ----
if ! python -c "import PIL" &> /dev/null; then
    echo "Pillow not found, installing..."
    $PIP_BIN install Pillow
fi

# ---- 5. Build the .app ----
# Use --windowed to hide terminal and --name for bundle name
# Use --onefile + --windowed for a single .app bundle
pyinstaller --windowed --name "$APP_NAME" --icon "$ICON_FILE" --onefile "$ENTRY_POINT"

# Move the single-file .app into a proper .app bundle
APP_BUNDLE="dist/$APP_NAME.app"
if [ -f "dist/$APP_NAME" ]; then
    echo "Wrapping single-file executable into $APP_BUNDLE..."
    mkdir -p "$APP_BUNDLE/Contents/MacOS"
    mv "dist/$APP_NAME" "$APP_BUNDLE/Contents/MacOS/$APP_NAME"
    mkdir -p "$APP_BUNDLE/Contents/Resources"
    cp "$ICON_FILE" "$APP_BUNDLE/Contents/Resources/"
    echo "APPL????" > "$APP_BUNDLE/Contents/PkgInfo"  # minimal PkgInfo for macOS
fi

echo "Build complete! Check $APP_BUNDLE"

# ---- OPTIONAL CLEANUP ----
read -p "Do you want to uninstall Python, Homebrew, and remove the venv? (y/n) " CLEANUP
if [ "$CLEANUP" = "y" ]; then
    deactivate
    rm -rf "$PYTHON_VENV"
    brew uninstall python@$PYTHON_VERSION python-tk@$PYTHON_VERSION
    brew cleanup
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
    echo "Cleanup complete. The only thing left is your built .app in dist/"
fi
