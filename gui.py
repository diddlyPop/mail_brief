from tkinter import *
import mail

# gui.py creates a small login gui requiring email and password to an imap email.
# gui.py writes the email and password to a text file (this is not safe)
# gui.py calls mail.start_connection() and runs off the credentials in credentials.txt


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.winfo_toplevel().title("Login Window")
        self.label_banner = Label(text="Mail Brief", bg="blue", fg="white", width="30", height="2", font=("Calibri", 13)).pack()
        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.logbtn = Button(self, text="Load Last", command=self._load_btn_clicked)
        self.logbtn.grid(columnspan=3)

        self.pack()

    def _login_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        with open('credentials.txt', 'w+') as file:
            file.write(username+'\n')
            file.write(password)
            mail.start_connection()
            root.destroy()

    def _load_btn_clicked(self):
        with open('credentials.txt', 'r') as file:
            print(file.read())
            print(file.read())
            mail.start_connection()
            root.destroy()


root = Tk()
lf = LoginFrame(root)
lf.mainloop()
