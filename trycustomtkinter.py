import customtkinter

def button_callback():
    print("Button Pressed")


app = customtkinter.CTk()
app.title("Python E-learning")
app.geometry("600x900")

button = customtkinter.CTkButton(app, text="Print Button", command=button_callback)
button.grid(row=0, column=0, padx=20, pady=20)

app.mainloop()