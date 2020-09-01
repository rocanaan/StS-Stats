For setting up SpireStats:

1. Install Python: https://www.python.org/downloads/
  on Windows this entails downloading an exe and running it. Standard install config is fine.
2. Tweak config.ini to your liking (only change the settings in the [USER] section)
3. Edit streaks.txt to contain your current active streaks
  (format is rotating/ironclad/silent/defect/watcher, each on a new line)
4. If you would like the winrate/streaks to automatically update on your stream:
    - In OBS on the sources pane, click the plus->text->ok
    - Check the "Read from file" box, click "Browse" and navigate to winrate.txt (or streaks.txt)
    - Configure other settings (such as size, font, color, etc) as needed
    - Note: in order for this feature to work, 'fileOutput' in config.ini must be set to True. This is the default
5. If you do not intend to show this automatically on stream, set 'fileOutput' to False so that the winrates
    can be displayed on the terminal window instead

Other various notes:
I am not aware of how things like ModTheSpire, mod characters, and daily runs interact with my script.
If you come across any issues, theGravyTrainTTK#9900 is my discord tag, you can contact me there.
  Reasonable feature accommodations/improvements are also a possibility.
The rotating streak currently doesn't check if you are actually rotating in order,
  it just tracks consecutive runs regardless of character
The rotating winrate (by default) takes N runs from each character, where N = historySize/charCount, rounded down.
  So it will always be a balanced number of runs from each character,
  even if recently you have ran one character more than the others.
  If you would prefer the rotating winrate to take 'historySize' runs from each character, set 'rotatingBehavior' to 1
