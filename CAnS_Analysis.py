# Coded by Kai Chuen Tan
# Title: The study between Oryctes Mist coverage area and drone speed
# Last Modified: March 29th, 2021


## Import necessary libraries.
import os # Miscellaneous Operating System Interfaces
import shutil # High-level file operations
import tkinter as tk # Graphic User Interface Programming
from tkinter import messagebox # GUI Button
from tkinter import filedialog # GUI File Selection
import pandas as pd # Data analysis and manipulation tool
import numpy as np # Data struction library
# import matplotlib 
import matplotlib.pyplot as plt # Plotting Library


## Variables' Initialization
max_column = 0


## Log to CSV Conversion
top_bar = tk.Tk()

# Add a title to the window.
top_bar.title("Poladrone")

# Canvas design (master, background color, width, height, border type)
converter_Canvas = tk.Canvas(top_bar, bg='RoyalBlue1', width = 550, height = 230, relief ='raised')
converter_Canvas.pack()

# Add a title text.
title_Text = tk.Label(top_bar, text='Log-to-CSV File Conversion Tool', bg = 'RoyalBlue1')
title_Text.config(font = ('aerial', 24, 'bold')) # Set a font type and font size.
converter_Canvas.create_window(275, 60, window=title_Text) # Position of the title.

# Get flight log file location from user.
def getFileLoc():

    global original_file_path

    original_file_path = filedialog.askopenfilename()

# Button customization.
browse_Button = tk.Button(text="      Browse For Flight Log      ", command = getFileLoc , bg = 'AntiqueWhite1', fg ='gray1', font = ('aerial', 12, 'bold') )
converter_Canvas.create_window(275, 130, window=browse_Button)

# Convert Flight Log to CSV file.
def log_to_csv_Conversion():

    global original_file_path

    try:
        
        file_name = os.path.basename(original_file_path) # Store the exact file name including the extension

        copied_file_path = "Flight_Logs/" + file_name # Path to copy to.
        copied_file_loc = shutil.copyfile(original_file_path, copied_file_path) # Copy and paste the file to a new location.
    
        # Convert log to csv.
        csv_copied_file_path = copied_file_path[:-4] + '.csv' 
        os.rename(copied_file_path, csv_copied_file_path)

        # Override original file path.
        original_file_path = csv_copied_file_path

        Msg_box = tk.messagebox.showinfo('Poladrone', 'Flight Log is Converted to a CSV File!')
    
        if Msg_box == 'ok':
        
            # Exit.
            top_bar.destroy()

    except NameError:

        tk.messagebox.showwarning('Poladrone', 'Please Select a Flight Log to Convert.') # Request user to select a flight log

# Button customization.
convert_Button = tk.Button(text="      Convert Log to CSV      ", command = log_to_csv_Conversion , bg = 'AntiqueWhite1', fg ='gray1', font = ('aerial', 12, 'bold') )
converter_Canvas.create_window(275, 180, window=convert_Button)

top_bar.mainloop()


## Data Extraction
# Determine Number of Rows in the CSV file.
flight_data = pd.read_csv(original_file_path, delimiter = ',', sep = ',', header = None, names = range(21), index_col = 0, low_memory = False) # Store the flight data labels into an array.
#number_of_Rows = len(flight_data) # Store number of rows as an integer.
#print(flight_data) # Print the result to verify.

# Determine the maximum number of columns in this CSV file.
"""for counter in range(number_of_Rows-1):

    # Read row by row of data.
    per_Row_Data = pd.read_csv(original_file_path, delimiter = ',', sep = ',', header = None, nrows = 1, skiprows = counter)
    # Determine that specific row's total number of columns.
    number_of_Columns = len(per_Row_Data.columns)
    print(counter)

    # If the latest number of columns is larger than the previous maximum number of columns
    if number_of_Columns > max_column:

        max_column = number_of_Columns # Rectify the maximum number of columns in the CSV file.
        print(max_column)"""

# Extract necessary data from the flight log.
Duration_Batt = flight_data.loc["BAT"].iloc[:,[0]] # Time in seconds [Battery].
Battery_Voltage = flight_data.loc["BAT"].iloc[:,[1]] # Battery Voltage in Volts.
Duration_HSp = flight_data.loc["GPS"].iloc[:,[0]] # Time in seconds [Speed].
Ground_Speed = flight_data.loc["GPS"].iloc[:,[9]] # Drone Ground Speed in m/s.

# Store the data in a list.
Duration_Batt_List = Duration_Batt.astype('int32').values.tolist()
Duration_Batt_List = np.array(Duration_Batt_List)-np.array(Duration_Batt_List[0]) # Start from zero second.
Duration_Batt_List = (np.array(Duration_Batt_List)-np.array(Duration_Batt_List[0]))/np.array(1000000) # Convert microseconds to seconds
Battery_Voltage_List = Battery_Voltage.astype('float64').values.tolist()

Duration_HSp_List = Duration_HSp.astype('int32').values.tolist()
Duration_HSp_List = np.array(Duration_HSp_List)-np.array(Duration_HSp_List[0]) # Start from zero second.
Duration_HSp_List = (np.array(Duration_HSp_List)-np.array(Duration_HSp_List[0]))/np.array(1000000) # Convert microseconds to seconds
Ground_Speed_List = Ground_Speed.astype('float64').values.tolist()


## Plot and Present Data
# Battery Voltage Plots
figure, axes = plt.subplots(2,1) # Two row one column of subplots

axes[0].plot(Duration_Batt_List, Battery_Voltage_List)
axes[0].set(xlabel='Time (s)', ylabel='Battery Voltage (V)',
       title='Battery Voltage and Ground Speed Analysis During An Auto Mission')
axes[0].grid()

axes[1].plot(Duration_HSp_List, Ground_Speed_List, color ='tab:orange')
axes[1].set(xlabel='Time (s)', ylabel='Ground Speed (m/s)')
axes[1].grid()

figure.savefig("Battery Voltage and Ground Speed Analysis Plot.png")
plt.show()
