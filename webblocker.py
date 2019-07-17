import sys, os, time, tkinter, datetime
from tkinter import messagebox

# Redirect
REDIRECT = "127.0.0.1"

# Main GUI Window
class Main_Application:

    # Create the GUI
    def __init__(self):
        # Window
        self.window = tkinter.Tk()
        self.window.title("Productive Website Blocker")
        self.window.geometry("342x280")
        self.window.resizable(0, 0)

        # Sleep input
        self.timer_text = tkinter.Label(self.window, text="You would like to be productive for ")
        self.timer_text.grid(column=0, row=3, pady=15, columnspan=3, sticky="W")
        self.spin = tkinter.Spinbox(self.window, from_ = 0, to=300, width=3)
        self.spin.grid(column=0, row=3, columnspan=3, pady=15, padx=235, sticky="W")
        self.spin_text = tkinter.Label(self.window, text="minutes.")
        self.spin_text.grid(column=0, row=3, pady=15, padx=280, columnspan=3)

        # Website input
        self.website_list = tkinter.Listbox(self.window, selectmode="multiple", height="6", exportselection=False, yscrollcommand="scrollbar.set")
        self.website_list.insert(1, "facebook.com")
        self.website_list.insert(2, "instagram.com")
        self.website_list.insert(3, "reddit.com")
        self.website_list.insert(4, "netflix.com")
        self.website_list.insert(5, "youtube.com")
        self.website_list.insert(6, "twitch.tv")
        self.website_list.grid(column=0, row=2, sticky="W", pady=5, padx=90)
        self.website_text = tkinter.Label(self.window, text="Select the websites you would like to block:")
        self.website_text.grid(column=0, row=1, sticky="W")

        # Start and end time
        self.start_time = tkinter.Label(self.window, text="Start:\n00:00:00 AM")
        self.start_time.grid(column=0, row=4, sticky="W", padx=44)
        self.end_time = tkinter.Label(self.window, text="End:\n00:00:00 AM")
        self.end_time.grid(column=0, row=4, sticky="W", padx=220)

        # Start button
        self.begin_button = tkinter.Button(self.window, text="Start!", state="normal", command= lambda: self.clickedButton())
        self.begin_button.grid(column=0, row=5, sticky="W", pady=10, padx=142)

        self.window.mainloop()
    
    # Default state of the application (when it not being used)
    def default_state(self):
        self.begin_button.config(state="normal")
        self.start_time.config(text="Start:\n00:00:00 AM")
        self.end_time.config(text="End:\n00:00:00 AM")
    
    # Active state of the application (in use)
    def active_state(self, sleep_time):
        # Disables the start button to prevent more user input
        self.begin_button.config(state="disable")

        # Put the start and end time on the GUI
        time_now = datetime.datetime.now()
        time_end = time_now + datetime.timedelta(seconds=sleep_time)
        self.start_time.config(text=f"Start:\n{time_now.strftime('%I:%M:%S %p')}")    
        self.end_time.config(text=f"End:\n{time_end.strftime('%I:%M:%S %p')}")

    # Processes the user information and starts the application
    def clickedButton(self):
        # Get the user's input time
        sleep_time = float(self.spin.get())

        # Convert to seconds
        sleep_time *= 60

        # Get the indexes and sites
        indexes = self.website_list.curselection()
        sites = self.get_selected_sites()
        
        # Check if the user input is valid
        if len(indexes) == 0 or sleep_time == 0 or not self.confirm():
            return

        # Create new host lines
        new_hosts_lines = create_new_host_lines(sites)

        # Put the application in the active state
        self.active_state(sleep_time)

        # Update the window before webblock function (because it uses time.sleep())
        self.window.update()

        # Block websites user selected
        webblocker(new_hosts_lines, sleep_time)

        # When time is up alert the user
        messagebox.showinfo("Completed!","The sites have been unblocked. Good Job!")

        # Put application back to default state
        self.default_state()

    # Gets the websites that the user selected from the ListBox
    def get_selected_sites(self):
        # Add newline because these are the lines we are writing to hosts file
        sites = []

        # Get indexs of the list
        indexes = self.website_list.curselection()

        # Get the websites and append to the list
        for index in indexes:
            sites.append(self.website_list.get(index))
            sites.append("www." + self.website_list.get(index))
                
        return sites

    # Confirms if the user wants to lock websites
    def confirm(self):
        confirmation = messagebox.askyesno("Confirmation",f"Are you sure to lock these websites for {self.spin.get()} minutes?")

        return confirmation

# Create new hosts lines to be put into file
def create_new_host_lines(sites):
    sites_list = ["\n"]
    for site in sites:
        sites_list.append(REDIRECT + " " + site + "\n")
    
    print(sites_list)
    return sites_list

def webblocker(new_host_lines, sleep_time):
    # Change directory to linux's hosts file directory and open it
    os.chdir("/etc/")
    host_file = open("hosts", "a+")

    # Move to start of file and put all lines into host_content var
    host_file.seek(0)
    host_content = host_file.readlines()

    # Write block website to hosts file
    for line in new_host_lines:
        # If already existed then do not write again
        if line in host_content:
            continue
        
        # Write to host file
        host_file.write(line)
    
    # Update host_content
    host_file.seek(0)
    host_content = host_file.readlines()

    # Close file
    host_file.close()

    # Sleep for user's desired duration
    time.sleep(sleep_time)
    
    # Remove websites from host file
    host_file = open("hosts", "w")
    for line in host_content:
        # If the website we block ignore 
        if line in new_host_lines:
            continue
        
        # Write if not the website we block
        host_file.write(line)

    # Close hosts file
    host_file.close()

if __name__ == "__main__":
    app = Main_Application()