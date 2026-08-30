# Rogue Joker - A recreation of Balatro in Python

## The hit indie game, but with an accelerated pace, that you can play in your CLI.

## Demo
![demo](https://files.catbox.moe/i5rl2h.webp)

## How To Install
Recommended: Use a virtual environment to avoid conflicts with system Python packages.

Windows (PowerShell)
```
git clone https://github.com/devin-zhou/Rogue-Joker.git
cd Rogue-Joker/src
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r ..\requirements.txt
python game.py
```

macOS / Linux
```
git clone https://github.com/devin-zhou/Rogue-Joker.git
cd Rogue-Joker/src
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r ../requirements.txt
python3 game.py
```

Note: Use `python` on Windows and `python3` on macOS/Linux. Requires Python 3.8+.

## Known Issues / Future Additions
* UI overhaul
* New Jokers
* Brainstorm doesn't work with one time Jokers
* 0 indexed inputs
