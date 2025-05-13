from Screens.login_screen import LoginApp
from db import initialize_database

if __name__ == "__main__":
    initialize_database()
    app = LoginApp()
    app.mainloop()