from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from second_files.tkinterCustomButton import TkinterCustomButton
from second_files import sql_restaurant
from second_files.treeCustom import StockTreeView, CategorieTreeView, ProductTreeView, UserTreeView

class LoginWindow:
    """
    Class qui gère la fenêtre principale.
    """
    def __init__(self, master):
        self.master = master
        sql_restaurant.Utilisateur.disconnect()
        for widget in root.winfo_children():
            widget.destroy()

        self.Title = Label(master, text="Gestion des stocks", fg="black", width=100, bg="#a9a083", font=("Futura", 30))
        self.Title.pack()
       
       
        self.string_username = StringVar()
        self.string_username.set("Nom d'utilisateur :")
        self.string_password = StringVar()
        self.string_password.set("Mot de passe :")
       
       
       
        self.username_input = Entry(self.master, font=("Arial", 15), bd=4, textvariable=self.string_username, justify="center")
        self.username_input.bind("<FocusIn>", self.entry_event1)
        self.username_input.bind("<FocusOut>", self.entry_event1)
        self.username_input.bind("<Button-1>", self.entry_event1)
        self.username_input.bind("<Return>", lambda e: self.call_button_login)
        self.username_input.place(relx=.5, rely=.3, anchor="center")
       
        self.password_input = Entry(self.master, font=("Arial", 15), bd=4, textvariable=self.string_password, show='*', justify="center")
        self.password_input.place(relx=.5, rely=.4, anchor="center")
        self.password_input.bind("<FocusIn>", self.entry_event2)
        self.password_input.bind("<FocusOut>", self.entry_event2)
        self.password_input.bind("<Button-1>", self.entry_event2)
        self.password_input.bind("<Return>", lambda e: self.call_button_login)
       
       
       
        self.login_button = TkinterCustomButton(master=self.master, hover_color="#5499C7",bg_color="#2874A6", text_font=("Arial", 10), text="Connexion", text_color="white", corner_radius=0, width=100, height=35, hover=True, command=lambda: self.call_button_login())
        self.login_button.place(relx=.5, rely=.50, anchor="center")
       
       
       
    def entry_event2(self, event):
        """Entree: Un event
           Fonction: Fludifi l'entrée du texte du password.
        """
        if event.type == "9": #FocusIn
            if len(event.widget.get()) == 0 or event.widget.get() == "Mot de passe :":
                event.widget.delete(0, "end")
        if event.type == "10": #FocusOut
            if len(event.widget.get()) == 0:
                event.widget.delete(0, "end")
                event.widget.insert(1, "Mot de passe :")
               
    def entry_event1(self, event):
        """Entree: Un event
           Fonction: Fludifi l'entrée du texte du username.
        """
        if event.type == "9": #FocusIn
            if len(event.widget.get()) == 0 or event.widget.get() == "Nom d'utilisateur :":
                event.widget.delete(0, "end")
        if event.type == "10": #FocusOut
            if len(event.widget.get()) == 0:
                event.widget.delete(0, "end")
                event.widget.insert(1, "Nom d'utilisateur :")
               
   
   
    def call_button_login(self):
        """Entree: un string, correspondant au nom d'utilisateur'.
           Fonction: En cas de nom incorrecte: Affichage de l'erreur sinon affichage de la fenêtre de la séléction de la date
        """
        username = self.username_input.get()
        mdp = self.password_input.get()
        if username == "" or username == "Nom d'utilisateur :":
            messagebox.showerror("Connection", "Merci de rentrer votre nom d'utilisateur.")
        elif mdp == "" or mdp == "Mot de passe:":
            messagebox.showerror("Connection", "Merci de rentrer votre mot de passe.")
        else:
            if sql_restaurant.connection(username, mdp) == True:
                root = MainWindow(self.master)
            else:
                messagebox.showerror("Connection", "Erreur dans la verification de vos informations saisies.")

       
class MainWindow:
    def __init__(self, root):
        for widget in root.winfo_children():
            widget.destroy()

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()

        w = sw * 0.7
        h = sh * 0.7

        x = (sw - w) / 2
        y = (sh - h) / 2

        self.root = root
        root.geometry("%dx%d+%d+%d" % (w, h, x, y))

        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=3)

        self.open_wrapper0 = Frame(root, bg="#a9a083")

        self.open_wrapper0.columnconfigure(0, weight=1)
        self.open_wrapper0.grid_rowconfigure(0, weight=1)
        self.open_wrapper0.grid_rowconfigure(1, weight=1)
        self.open_wrapper0.grid_rowconfigure(2, weight=1)
        self.open_wrapper0.grid_rowconfigure(3, weight=1)

        self.userLabel = Label(self.open_wrapper0, bg="#a9a083", text=sql_restaurant.Utilisateur.getName(), fg="black", font=("Futura", 15))
        self.userLabel.grid(column=0, row=0, sticky=N)

        self.accesLabel = Label(self.open_wrapper0, bg="#a9a083", text="Niveau d'acces: " + str(sql_restaurant.Utilisateur.getAcces()), fg="black", font=("Futura", 10))
        self.accesLabel.grid(column=0, row=0, sticky=N, pady=50)

        self.closeButton = TkinterCustomButton(master=self.open_wrapper0, hover_color="#ad686c", fg_color="#A4585C",
                                                  text_font=("Arial", 10), text="Fermer", text_color="white",
                                                  corner_radius=0, height=20, hover=True,
                                                  command=self.testFunction)
        self.closeButton.grid(column=0, row=0, sticky=N, pady=100)

        self.settingsOpenButton = TkinterCustomButton(master=self.open_wrapper0, hover_color="#5499C7", fg_color="#2874A6",
                                                  text_font=("Arial", 10), text="Parametre", text_color="white",
                                                  corner_radius=0, height=20, hover=True,
                                                  command=lambda : SettingsWindow(self.root))
        self.settingsOpenButton.grid(column=0, row=3, sticky=S, pady=50)

        self.disconnectOpenButton = TkinterCustomButton(master=self.open_wrapper0, hover_color="#ad686c", fg_color="#A4585C",
                                                  text_font=("Arial", 10), text="Déconnection", text_color="white",
                                                  corner_radius=0, height=20, hover=True,
                                                  command=lambda : LoginWindow(self.root))
        self.disconnectOpenButton.grid(column=0, row=3, sticky=S)

        self.menuIcon = ImageTk.PhotoImage(Image.open('image/menu.png').resize((40, 40)))
        self.settingsIcon = ImageTk.PhotoImage(Image.open('image/settings.png').resize((40, 40)))
        self.exitIcon = ImageTk.PhotoImage(Image.open('image/exit.png').resize((40, 40)))

        self.openButton = Button(root, image=self.menuIcon, bg="#a9a083", activebackground="#a9a083", relief=SUNKEN, borderwidth=0, command=self.testFunction)
        self.settingsButton = Button(root, image=self.settingsIcon, bg="#a9a083", activebackground="#a9a083", relief=SUNKEN, borderwidth=0, command=lambda : SettingsWindow(self.root))
        self.disconnectButton = Button(root, image=self.exitIcon, bg="#a9a083", activebackground="#a9a083",relief=SUNKEN, borderwidth=0, command=lambda : LoginWindow(self.root))

        self.openButton.grid(column=0, row=0, rowspan=1, sticky=N)
        self.settingsButton.grid(column=0, row=2, sticky=S, pady=65)
        self.disconnectButton.grid(column=0, row=2, sticky=S)

        self.wrapper1 = LabelFrame(root, text="Inventaire", width=1039, height=234)
        self.wrapper2 = LabelFrame(root, text="Filtre", width=1039, height=234)
        self.wrapper3 = LabelFrame(root, text="Modifier mes donnes", width=1039, height=234)
        self.wrapper1.grid(column=1, row=0, stick=NSEW, padx=5, pady=10)
        self.wrapper2.grid(column=1, row=1, stick=NSEW, padx=5, pady=10)
        self.wrapper3.grid(column=1, row=2, stick=NSEW, padx=5, pady=10)

        self.wrapper1.grid_propagate(0)
        self.wrapper2.grid_propagate(0)
        self.wrapper3.grid_propagate(0)

        if sql_restaurant.Utilisateur.getAcces() <= 1:
            self.wrapper3.grid_forget()

        self.t = [StringVar(), StringVar(), StringVar(), StringVar()]
        self.lbls = [Label(self.wrapper3, text="Produit"), Label(self.wrapper3, text="Arrive"), Label(self.wrapper3, text="Nombre"),
                     Label(self.wrapper3, text="Peremption")]
        self.entrys = [Entry(self.wrapper3, textvariable=self.t[0]), Entry(self.wrapper3, textvariable=self.t[1]),
                       Entry(self.wrapper3, textvariable=self.t[2]), Entry(self.wrapper3, textvariable=self.t[3])]

        self.lbl_tree = Label(self.wrapper2, text="Donnees affiché")
        self.lbl_tree.grid(row=0, column=0, padx=5, pady=3)
        self.dict_tree = {"Stock": StockTreeView(self.wrapper1, self.lbls, self.entrys, self.t, self.wrapper3), "Categorie": CategorieTreeView(self.wrapper1, self.lbls, self.entrys, self.t),
                          "Produit": ProductTreeView(self.wrapper1, self.lbls, self.entrys, self.t)}

        if sql_restaurant.Utilisateur.getAcces() == 2:
            self.dict_tree["User"] = UserTreeView(self.wrapper1, self.lbls, self.entrys, self.t)

        self.var_tree = StringVar()
        self.var_tree.set("Stock")
        self.tree_select = OptionMenu(self.wrapper2, self.var_tree, *self.dict_tree.keys(), command=self.change_tree)
        self.tree_select.grid(row=0, column=1, padx=5, pady=3)

        self.tree = self.dict_tree["Stock"]
        self.tree.create()

        self.edit_btn = TkinterCustomButton(master=self.wrapper3, hover_color="#5499C7",fg_color="#2874A6", text_font=("Arial", 10), text="Modifier", text_color="white", corner_radius=50, width=100, height=20, hover=True, command=self.tree.edit)

        self.edit_btn.grid(row=4, column=2, padx=5, pady=3)

        self.add_btn = TkinterCustomButton(master=self.wrapper3, hover_color="#5499C7",fg_color="#2874A6", text_font=("Arial", 10), text="Ajouter", text_color="white", corner_radius=50, width=100, height=20, hover=True, command=self.tree.add)
        self.add_btn.grid(row=4, column=3, padx=5, pady=3)

        self.del_btn = TkinterCustomButton(master=self.wrapper3, hover_color="#5499C7",fg_color="#2874A6", text_font=("Arial", 10), text="Supprimer", text_color="white", corner_radius=50, width=100, height=20, hover=True, command=self.tree.delete)
        self.del_btn.grid(row=4, column=4, padx=5, pady=3)




    def change_tree(self, selected):
        print(self.wrapper1.winfo_width(), self.wrapper1.winfo_height())
        global tree
        self.tree.hide()
        self.tree = self.dict_tree[self.var_tree.get()]
        self.edit_btn.function = self.tree.edit
        self.add_btn.function = self.tree.add
        self.del_btn.function = self.tree.delete
        self.tree.create()

    def testFunction(self):
        if self.open_wrapper0.grid_info():
            self.open_wrapper0.grid_forget()
            self.root.grid_columnconfigure(0, weight=0)
            self.root.grid_columnconfigure(1, weight=3)
            self.openButton.grid(column=0, row=0, rowspan=1, sticky=N)
            self.settingsButton.grid(column=0, row=2, sticky=S, pady=65)
            self.disconnectButton.grid(column=0, row=2, sticky=S)
        else:
            self.openButton.grid_forget()
            self.settingsButton.grid_forget()
            self.disconnectButton.grid_forget()
            self.root.grid_columnconfigure(0, weight=1)
            self.root.grid_columnconfigure(1, weight=3)
            self.open_wrapper0.grid(column=0, row=0, rowspan=3, stick=NSEW, padx=5, pady=10)


class SettingsWindow:
    def __init__(self, main):
        self.main = main
        self.root = Tk()
        self.root.background = "#0000"
        self.root.title("Gestion de Stock")
        self.darkmode = Button(self.root, text="Dark Mode", bg="#a9a083", activebackground="#a9a083",relief=SUNKEN, borderwidth=0, command=lambda : self.darkmode_function(self.main))
        self.darkmode.pack()
        self.root.mainloop()

    def darkmode_function(self, main_widget):
        for widget in main_widget.winfo_children():
            if isinstance(widget, (Frame, LabelFrame)):
                self.main["background"] = "#181818"
                widget["background"] = "#181818"
                if isinstance(widget, LabelFrame):
                    widget["foreground"] = "#E01414"
                self.darkmode_function(widget)
            else:
                print("okkkkkkkkk")
                if "fg_color" in widget.config():
                    widget["fg_color"] = "#181818"
                if "activebackground" in widget.config():
                    widget["activebackground"] = "#181818"
                if "disabledbackground" in widget.config():
                    widget["disabledbackground"] = "#3B3B3B"
                if "insertbackground" in widget.config():
                    widget["insertbackground"] = 'white'
                if "bg" in widget.config():
                    widget["bg"] = "#181818"
                if "fg" in widget.config():
                    widget["fg"] = "#E01414"
                if "text_color" in widget.config():
                    widget["text_color"] = "#E01414"




root = Tk()
root.background = "#0000"
root.title("Gestion de Stock")
root.bind_all("<Button-1>", lambda event: event.widget.focus_set())
width = root.winfo_screenwidth()-65
height = root.winfo_screenheight()-100
root.configure(background="#a9a083")

# set the position of the window to the center of the screen
root.geometry(f'{604}x{461}')
my_gui = LoginWindow(root)
root.mainloop()



