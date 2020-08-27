For setting up SpireStats:

1. Install Python: https://www.python.org/downloads/
  on Windows this entails downloading an exe and running it. Standard install config is fine.
2. Tweak config.ini to your liking (only change the settings in the [USER] section)
3. Edit streaks.txt to contain your current active streaks
  (format is rotating/ironclad/silent/defect/watcher, each on a new line)
4. If you would like the winrate/streaks to automatically update on your stream:
    - In OBS on the sources pane, click the plus->text->ok
    - Check the "Read from file" box, click "Browse" and navigate to streaks.txt (or winrate.txt)
    - Configure other settings (such as size, font, color, etc) as needed
    - Note: in order for this feature to work, 'fileOutput' in config.ini must be set to True. This is the default

Other various notes:
I am not aware of how things like ModTheSpire, mod characters, and daily runs interact with my script.
If you come across any issues, theGravyTrainTTK#9900 is my discord tag, you can contact me there.
  Reasonable feature accommodations/improvements are also a possibility.
The rotating streak currently doesn't check if you are actually rotating in order,
  it just tracks consecutive runs regardless of character
The rotating winstreak takes N runs from each character, where N = historySize/charCount, rounded down.
  So it will always be a balanced number of runs from each character,
  even if recently you have ran one character more than the others.
  The exception being your historySize > a specific characters run count.
