import subprocess
import csv
import datetime
import time
import shutil 
import msvcrt
import os
import tkinter as tk
from tkinter import filedialog

# v1.4 that uses new version of ticket reset with only exe and loc file replacement (SAS 2.0.2)

# Wait for the user to press any key to continue
def wait_for_key():
    print("Press any key to continue...")
    msvcrt.getch()  # Waits for a key press

# Opens GUI window where user navigates to a requested directory to save for future reference in ticket_reset_filepaths.csv
def get_directory_path(row):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory_path = None  # Initialize with a default value

    if row == 0:
        directory_path = filedialog.askdirectory(title="Select 1.10.2 directory")
    elif row == 1:
        directory_path = filedialog.askdirectory(title="Select current version directory")
    elif row == 2:
        directory_path = filedialog.askdirectory(title="Select Steam game directory")

    if directory_path:
        return directory_path
    else:
        return None

# Check if filepaths.csv exists in same directory as ticket reset script, if not make it and have user select filepaths
def check_setup():
    try:
        file_path = 'ticket_reset_filepaths.csv'  #default csv filename

        script_dir = os.path.dirname(__file__)  # Directory of the script
        file_path = os.path.join(script_dir, file_path) 

        if not os.path.exists(file_path):
            print("File " + file_path +" not found. Creating a new CSV file...")
            print("You will not have to select these directories again if ticket_reset_filepaths.csv exists in the same directory as the ticket_reset.py")
            try:
                data_to_write = [
                    ['"1.10.2 location"',''],  
                    ['"Current game version location"',''], 
                    ['"Steam game directory location"',''], 
                    ]

                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for row in data_to_write:
                        writer.writerow(row)
                    print("New CSV file created at: " +file_path)
            except Exception as e:
                print("An error occurred while creating the file: " + str(e))
                input("Press Enter to exit...")

        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        for i, _ in enumerate(rows):
            if not rows[i][1]:
                directory = get_directory_path(i)
                if directory:
                    rows[i][1] = directory
                    print("Directory path " + directory + " appended to row " + str(i+1) + " in " + file_path)
                else:
                    print("No directory selected for row " + str(i+1))

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

    except Exception as e:
        print("An error occurred: " + str(e))

# Reads the csv with the necessary directories
def read_filepaths_csv():
    try:
        file_path = 'ticket_reset_filepaths.csv'  #default csv filename
        script_dir = os.path.dirname(__file__)  # Directory of the script
        file_path = os.path.join(script_dir, file_path) 

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

            directory_1_10_2 = rows[0][1] if rows[0][0] == '"1.10.2 location"' else None
            directory_current = rows[1][1] if rows[1][0] == '"Current game version location"' else None
            directory_game = rows[2][1] if rows[2][0] == '"Steam game directory location"' else None
            print("1.10.2 location: ", directory_1_10_2)
            print("Current game version location: ", directory_current)
            print("Steam game directory location: ", directory_game)

            return directory_1_10_2, directory_current, directory_game
        
    except FileNotFoundError:
        print("File " + file_path + " not found.")
        return None, None, None
    except Exception as e:
        print("An error occurred: " + str(e))
        return None, None, None

# Check if SAS4 is running, and if so, close it
def close_process(process_name):
    msg1 = "Checking if " + process_name + " is open..."
    print(msg1)
    try:
        while True:
            # Run tasklist command to get a list of processes
            output = subprocess.check_output(['tasklist', '/fo', 'csv', '/nh']).decode('utf-8').strip()

            process_found = False

            # Split the output into lines and check if the process exists
            for line in output.split('\n'):
                if process_name in line:
                    pid = int(line.split(',')[1].strip(' "'))
                    process_found = True
                    msg2 = "Process " + process_name + " found with PID: " + str(pid) + ". Terminating..."
                    print(msg2)
                    subprocess.run(['taskkill', '/F', '/PID', str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    msg3 = "Process " + process_name + " terminated."
                    print(msg3)
                    break  # Exit the for loop since the process is terminated
                
            if not process_found:
                msg4 = "Process " + process_name + " not found. Continuing..."
                print(msg4)
                break  # Exit the while loop if the process is not found

            # Wait for a short interval before checking again
            time.sleep(1)

    except subprocess.CalledProcessError as e:
        msg5 = "Error: " + str(e)
        print(msg5)

# Copy files from source to destination
def copy_files(source_dir, destination_dir, program_name):
    try:
        if not source_dir.strip() or not destination_dir.strip():
            # print("At least one of the filepaths is undefined. Run the setup script")
            raise Exception("At least one of the filepaths is undefined. Run the setup script")
        
        source_dir_1 = source_dir + r'\Assets\Loc'
        destination_dir_1 = destination_dir + r'\Assets\Loc'

        source_dir_2 = source_dir + '\\' + program_name
        destination_dir_2 = destination_dir + '\\' + program_name

        # Remove the destination directory if it already exists
        shutil.rmtree(destination_dir_1, ignore_errors=True)
        # Copy all files and sub-directories from source to destination
        shutil.copytree(source_dir_1, destination_dir_1)
        msg1 = "Successfully replaced \\Assets\\Loc in " + destination_dir
        print(msg1)

        if os.path.exists(destination_dir_2):
            os.remove(destination_dir_2)
             
        shutil.copy2(source_dir_2, destination_dir_2)
        msg2 = "Successfully replaced " + program_name + " in " + destination_dir
        print(msg2)
        
    except FileNotFoundError:
        print("File not found or could not copy the program.")
    except Exception as e:
        msg3 = "Error: " + str(e)
        print(msg3)

# Start program located in directory_game\program_name (SAS4-Win.exe)
def start_program(directory_game, program_name):
    if not directory_game.strip():
        # print("At least one of the filepaths is undefined. Run the setup script")
        raise Exception("Game directory is undefined. Run the setup script")
    program_path = directory_game + '\\' + program_name
    try:
        subprocess.Popen(program_path)
        msg1 = program_name + " started successfully."
        print(msg1)
    except FileNotFoundError:
        msg2 = "Error: " + program_path + " not found."
        print(msg2)
    except Exception as e:
        msg3 = "Error: " + str(e)
        print(msg3)

from datetime import date, timedelta
import subprocess

def change_system_date_forward():
  """
  Attempts to change the system date forward by one day and returns the original date.

  Returns:
    A datetime.date object representing the original date (or None on error).
  """
  try:
    # Get the current date
    current_date = date.today()

    # Increment the date by one day
    next_date = current_date + timedelta(days=1)

    # Format the next date for the system's expected format
    formatted_date = next_date.strftime("%d-%m-%Y")

    # Set the system date using Command Prompt (requires administrative privileges)
    subprocess.run(['date', formatted_date], shell=True, check=True)

    # Print success message
    msg1 = "System date changed forward by one day to: " + str(next_date)
    print(msg1)

    return current_date  # Return the original current date

  except subprocess.CalledProcessError as e:
    # Print error message
    msg2 = "Error: " + str(e)
    print(msg2)
    return None  # Return None in case of an error

def change_system_date_back(original_date):
  """
  Attempts to change the system date back to the provided original_date.

  Args:
    original_date: A datetime.date object representing the original date.

  Returns:
    True if the date change was successful, False otherwise.
  """
  date_formats = ["%d-%m-%Y"]  # Use only the system's format.

  # Only attempt to change the date back if it was successfully changed forward
  if original_date:
    for date_format in date_formats:
      try:
        # Format the original date for the system's expected format
        formatted_date = original_date.strftime(date_format)
        subprocess.run(['date', formatted_date], shell=True, check=True)

        # Print success message
        print(f"System date changed back to: {formatted_date} using format: {date_format}")
        return True

      except subprocess.CalledProcessError as e:
        # Print error message for each format attempt
        print(f"Error trying date format '{original_date}': {str(e)}")

  # If all formats fail or original_date is None, indicate overall failure
  print(f"Failed to change system date back to: {original_date}")
  return False

if __name__ == "__main__":

    # Process name of SAS4, shouldn't have to be replaced
    program_name = "SAS4-Win.exe" 
    
    # Sees if ticket_reset_filepaths.csv exists, and if not, makes it
    check_setup() # works

    # Reads above csv file for necessary ticket reset directories
    directory_1_10_2, directory_current, directory_game = read_filepaths_csv() # works

    # Closes SAS if you already have SAS open, will continue on if SAS is closed
    close_process(program_name) # works

    # Copies version 1.10.2 files and pastes them in game directory
    copy_files(directory_1_10_2, directory_game, program_name) # works
    
    # Opens SAS from game directory (version 1.10.2)
    start_program(directory_game, program_name) # works

    # Have to be on MP screen when changing date, waits for user to do so manually
    print("Go to multiplayer screen and enter menu. Press any key to continue when ready.")
    wait_for_key() # works

    # Changes date to tomorrow and also returns current date as original_date
    original_date = change_system_date_forward() # works
    
    # Have to be force backup-ed or gracefully close out of SAS in order for save to update, waits for user to do so manually
    print("Force backup then press any key to continue")
    wait_for_key() # works

    # Closes out of SAS version 1.10.2
    close_process(program_name) # works

    # Copies version 2.0.1 files and pastes them in game directory
    copy_files(directory_current, directory_game, program_name) # works

    # Returns date back to original_date
    change_system_date_back(original_date)
    print("ez")
    wait_for_key()  # Replace with your user input function

    # Opens SAS from game directory (version 2.0.1)
    start_program(directory_game, program_name) # works

    print("Done") #works! - miikie

    # Waits for three seconds before program completes and terminal closes
    time.sleep(5)
