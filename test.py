import customtkinter

# Set up the appearance mode and theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Initialize the main application window
app = customtkinter.CTk()
app.title("CustomTkinter Checklist Example")
app.geometry("400x300")

# Define a function to execute when the checkbox is toggled
def checkbox_event():
    print("Checkbox state changed to:", check_var.get())

# 1. Create a variable to store the checkbox state ("on" or "off")
check_var = customtkinter.StringVar(value="off")

# 2. Instantiate the CTkCheckBox widget
checkbox = customtkinter.CTkCheckBox(
    master=app,
    text="Complete Daily Task",
    command=checkbox_event,
    variable=check_var,
    onvalue="on",
    offvalue="off"
)

# 3. Position the checkbox on the window
checkbox.pack(padx=20, pady=20)

# Run the application loop
app.mainloop()
