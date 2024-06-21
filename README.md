# SAS4-Python-Ticket-Reset
There are 2 files in this repository for resetting tickets, the main ticket_reset.py and an optional ticket_reset_cmd.bat. All of the actual process is done in the python script, while the batch script is only for convenience of running the python script and no longer for elevating to administrator privileges which was required in earlier versions. You'll have to change the filepath in the batch script to match where the python script is located and then double click to run and successfully reset your tickets. Alternatively, you can use VS Code or your favorite way to run python scripts instead.

In order to use the current version, you will have to download NirSoft's RunAsDate (not the x64 version, since SAS is 32 bit):
https://www.nirsoft.net/utils/run_as_date.html

This program injects the desired date into the process rather than changing the system date, providing several significant benefits over the previous approach, particularly removing issues arising due to regional variations in Windows date formatting as well as no longer requiring administrator privileges.

**Note that this will remove fairground purchase from your account** (if you have it) because fairground did not exist in 1.10.2. You can probably restore purchases or contact NK support with receipts, but be aware that you will lose fairground items. No other items should be affected.

When you first run the script, you should be directed to navigate to four directories:
1. SAS4 version 1.10.2 (or earlier) - The earlier game version still allows for the ticket reset exploit
2. SAS4 version 2.0.2 (or whatever is the current version) - You revert back to this version after resetting your tickets in 1.10.2 in order to play multiplayer
3. SAS4 game directory (should be something like: C:\Program Files (x86)\Steam\steamapps\common\SAS Zombie Assault 4) - Where SAS4 is loaded
4. RunAsDate.exe directory - After downloading RunAsDate from the above website and unzipping

These are saved as ticket_reset_filepaths.csv in the same directory as ticket_reset.py so you don't have to re-navigate to these filepaths in the future

You will still have to navigate to the multiplayer menu, press a key, force backup, and press another key as part of the ticket reset process, since this script is not yet fully automated

To download previous versions of SAS, follow this video: https://youtu.be/foUFfT7jzXo

To see the process of what's happening done manually, watch this video: https://youtu.be/r8ep9r_LSB8
