from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from second_files import sql_restaurant
from tkcalendar import Calendar

from second_files.tkinterCustomButton import TkinterCustomButton


def checkDateFormat(date):
    try:
        return bool(datetime.strptime(date, "%Y-%m-%d"))
    except ValueError:
        return False


def checkIfNumber(v):
    try:
        t = float(v)
        return True
    except:
        return False

class MyTreeView:
    def __init__(self, widget, headings=[], lbls=[], entrys=[], t=[]):
        self.headings = headings
        self.taille = len(headings)
        self.lbls = lbls
        self.entrys = entrys
        self.t = t
        self.tree = ttk.Treeview(widget, column=tuple(i + 1 for i in range(self.taille)), show="headings", height=6)
        for column in self.tree["column"]:
            self.tree.column(column, anchor=CENTER)
        self.scroll = ttk.Scrollbar(widget, orient="vertical", command=self.tree.yview)

    def hide(self):
        self.tree.pack_forget()
        self.scroll.pack_forget()
        if sql_restaurant.Utilisateur.getAcces() >= 1:
            for i in range(4):
                self.lbls[i].grid_forget()
                self.entrys[i].grid_forget()
                self.entrys[i]["state"] = "normal"
                self.entrys[i].unbind("<Double 1>")
            self.t[0].set("")
            self.t[1].set("")
            self.t[2].set("")
            self.t[3].set("")

    def setHeadings(self, headings):
        self.headings = headings

    def edit(self, msg):
        return messagebox.askyesno("Gestion des stocks", msg)

    def isActualItem(self):
        if self.actual_item:
            return True
        else:
            messagebox.showerror("Erreur", "Aucun élément séléctionner actuellement !")
            return False

    def add(self, msg):
        if isinstance(self, CategorieTreeView):
            if self.entrys[1].get() == "":
                messagebox.showerror("Erreur", "Certains champs ne sont pas renseigner.")
                return False
            return True

        for i in self.entrys:
            if i.grid_info():
                if i.get() == "":
                    messagebox.showerror("Erreur", "Certains champs ne sont pas renseigner.")
                    return False
        return messagebox.askyesno("Gestion des stocks", msg)


    def delete(self, msg):
        return messagebox.askyesno("Gestion des stocks", msg)


    def getrow(self, event):
        item = self.tree.item(self.tree.identify("item", event.x, event.y))
        if item and sql_restaurant.Utilisateur.getAcces() >= 1:
            self.actual_item = item["values"]
            return item['values']
        else:
            return None

    def update(self):
        self.tree.delete(*self.tree.get_children())

    def create(self):
        for i in range(self.taille):
            self.tree.heading(i + 1, text=self.headings[i])
        self.tree.pack(side=LEFT, fill="both", expand="yes", anchor='center')
        self.tree.configure(yscrollcommand=self.scroll.set)
        self.tree.bind("<Button-1>", self.getrow)
        self.scroll.pack(side=RIGHT, fill="y", anchor='center')


class StockTreeView(MyTreeView):
    def __init__(self, widget, lbls=[], entrys=[], t=[], wrapper=None):
        headings = ["Produit", "Arrive", "Nombre", "Peremption"]
        super(StockTreeView, self).__init__(widget, headings, lbls, entrys, t)
        self.actual_item = None
        if sql_restaurant.Utilisateur.getAcces() >= 1:
            self.wrapper = wrapper
            self.cal = Calendar(wrapper, selectmode='day', locale="fr",year=datetime.now().year, month=datetime.now().month,day=datetime.now().day,date_pattern="yyyy-mm-dd")
            self.arrive_set = TkinterCustomButton(master=self.wrapper, hover_color="#5499C7",fg_color="#2874A6", text_font=("Arial", 10), text="Arrivé", text_color="white", corner_radius=50, width=100, height=20, hover=True, command=self.setArrive)
            self.peremption_set = TkinterCustomButton(master=self.wrapper, hover_color="#5499C7",fg_color="#2874A6", text_font=("Arial", 10), text="Peremption", text_color="white", corner_radius=50, width=100, height=20, hover=True, command=self.setPeremption)

    def primary_key_changed(self):
        return self.actual_item[0] != self.t[0].get() or self.actual_item[1] != self.t[1].get()

    def edit(self, **kwargs):
        if self.isActualItem():
            msg = f"Souhaitez-vous vraiment mettre à jour cet élément ? ({self.actual_item[0]}, {self.actual_item[1]})"
            if super(StockTreeView, self).edit(msg):
                if not self.primary_key_changed():
                    if sql_restaurant.getProductIdByName(self.t[0].get()):
                        if checkDateFormat(self.t[1].get()) and checkDateFormat(self.t[3].get()):
                            if checkIfNumber(self.t[2].get()):
                                sql_restaurant.updateStock(sql_restaurant.getProductIdByName(self.t[0].get()), self.t[1].get(), self.t[2].get(),
                                                           self.t[3].get())
                                messagebox.showinfo("Succes",
                                                f"({self.t[0].get()}, {self.t[1].get()}, {self.t[2].get()}, {self.t[3].get()}) modifier avec succès.")
                                self.update()
                            else:
                                messagebox.showerror("Erreur", "Le nombre de produit doit être un nombre !")
                        else:
                            messagebox.showerror("Erreur", "Erreur dans les formats des dates ! Format attendu: YY-MM-DD")
                    else:
                        messagebox.showerror("Erreur", "Le produit entrée n'existe pas dans la base de données !")
                else:
                    messagebox.showerror("Erreur", "Vous ne pouvez pas modifier les clés primaires (Produit, Date arrivée) !")

    def add(self, **kwargs):
        msg = f"Souhaitez-vous vraiment ajouter cet élément ? ({self.t[0].get()}, {self.t[1].get()})"
        if super(StockTreeView, self).add(msg):
            if sql_restaurant.getProductIdByName(self.t[0].get()):
                if checkDateFormat(self.t[1].get()) and checkDateFormat(self.t[3].get()):
                    if checkIfNumber(self.t[2].get()):
                        sql_restaurant.addStock(self.t[0].get(), self.t[1].get(), self.t[2].get(), self.t[3].get())
                        messagebox.showinfo("Succes",
                                            f"({self.t[0].get()}, {self.t[1].get()}, {self.t[2].get()}, {self.t[3].get()}) ajouter avec succès.")
                        self.update()
                    else:
                        messagebox.showerror("Erreur", "Le nombre de produit doit être un nombre !")
                else:
                    messagebox.showerror("Erreur", "Erreur dans les formats des dates ! Format attendu: YY-MM-DD")
            else:
                messagebox.showerror("Erreur", "Le produit entrée n'existe pas dans la base de données !")

    def delete(self, **kwargs):
        if self.isActualItem():
            msg = f"Souhaitez-vous vraiment supprimer cet élément ? ({self.t[0].get()}, {self.t[1].get()})"
            if super(StockTreeView, self).delete(msg):
                sql_restaurant.remStock(self.t[0].get(), self.t[1].get())
                messagebox.showinfo("Succes", f"({self.t[0].get()}, {self.t[1].get()}, {self.t[2].get()}, {self.t[3].get()}) supprimer avec succès.")
                self.update()
                self.actual_item = None

    def setArrive(self):
        self.t[1].set(self.cal.get_date())

    def setPeremption(self):
        self.t[3].set(self.cal.get_date())

    def getrow(self, event):
        item = super(StockTreeView, self).getrow(event)
        if item:
            self.t[0].set(item[0])
            self.t[1].set(item[1])
            self.t[2].set(item[2])
            self.t[3].set(item[3])

    def update(self):
        super(StockTreeView, self).update()
        for i in sql_restaurant.getStockList():
            i = list(i)
            i[0] = sql_restaurant.getProductNameById(i[0])
            self.tree.insert('', 'end', values=i)

    def create(self):
        super(StockTreeView, self).create()
        self.update()
        if sql_restaurant.Utilisateur.getAcces() >= 1:
            for i in range(4):
                self.lbls[i].configure(text=self.headings[i])
                if i<2:
                    self.lbls[i].grid(row=0, column=i%2, padx=1, sticky="news")
                    self.entrys[i].grid(row=1, column=i%2, padx=1, sticky="n")
                else:
                    self.lbls[i].grid(row=2, column=i%2, padx=1, sticky="news")
                    self.entrys[i].grid(row=3, column=i%2, padx=1, sticky="n")

            self.entrys[0].config(state="disabled")
            self.entrys[1].config(state="disabled")
            self.entrys[0].bind("<Double 1>", self.switch)
            self.entrys[1].bind("<Double 1>", self.switch)
            self.cal.grid(column=5, rowspan=4, row=0, sticky='wse')
            self.arrive_set.grid(column=6, row=1, padx=5, pady=3, sticky='wse')
            self.peremption_set.grid(column=6, row=2, padx=5, pady=3, sticky='wse')

    def hide(self):
        super(StockTreeView, self).hide()
        if sql_restaurant.Utilisateur.getAcces() >= 1:
            self.cal.grid_forget()
            self.arrive_set.grid_forget()
            self.peremption_set.grid_forget()

    def switch(self, event):
        if event.widget["state"] == "disabled":
            event.widget["state"] = "normal"



class ProductTreeView(MyTreeView):
    def __init__(self, widget, lbls=[], entrys=[], t=[]):
        headings = ["Nom", "Prix Achat", "Prix Vente", "Categorie"]
        super(ProductTreeView, self).__init__(widget, headings, lbls, entrys, t)
        self.actual_item = None

    def edit(self, **kwargs):
        if self.isActualItem():
            msg = f"Souhaitez-vous vraiment mettre à jour cet élément ? ({self.actual_item[0]}, {self.actual_item[1]})"
            if super(ProductTreeView, self).edit(msg):
                if not sql_restaurant.getProductIdByName(self.t[0].get()):
                    sql_restaurant.updateProduct(sql_restaurant.getProductIdByName(self.actual_item[0]), self.t[0].get(), self.t[1].get(), self.t[2].get(), sql_restaurant.getCategorieIdByName(self.t[3].get()))
                    messagebox.showinfo("Succes", f"({self.t[0].get()}, {self.t[1].get()}, {self.t[2].get()}, {self.t[3].get()}) modifier avec succès.")
                    self.update()
                else:
                    messagebox.showerror("Erreur", f"Un produit se nomme déjà {self.t[0].get()}")

    def add(self, **kwargs):
        msg = f"Souhaitez-vous vraiment ajouter cet élément ? ({self.t[0].get()}, {self.t[1].get()})"
        if super(ProductTreeView, self).add(msg):
            if not sql_restaurant.getProductIdByName(self.t[0].get()):
                if sql_restaurant.getCategorieIdByName(self.t[3].get()):
                    sql_restaurant.addProduct(self.t[0].get(), self.t[1].get(), self.t[2].get(), self.t[3].get())
                    messagebox.showinfo("Succes", f"({self.t[0].get()}, {self.t[1].get()}, {self.t[2].get()}, {self.t[3].get()}) ajouter avec succès.")
                    self.update()
                else:
                    messagebox.showerror("Erreur", "La catégorie entrée n'existe pas dans la base de données !")
            else:
                messagebox.showerror("Erreur", f"Un produit se nomme déjà {self.t[0].get()}")


    def delete(self, **kwargs):
        if self.isActualItem():
            msg = f"Souhaitez-vous vraiment supprimer cet élément ? ({self.t[0].get()}, {self.t[1].get()})"
            if super(ProductTreeView, self).delete(msg):
                if not sql_restaurant.productIsUsed(self.actual_item[0]):
                    sql_restaurant.removeProduct(self.t[0].get())
                    messagebox.showinfo("Succes", f"({self.t[0].get()}, {self.t[1].get()}, {self.t[2].get()}, {self.t[3].get()}) supprimer avec succès.")
                    self.update()
                    self.actual_item = None
                else:
                    messagebox.showerror("Erreur", f"({self.actual_item[0]}) est lié à certains enregistrement dans le stock, merci de changé d'abord les produits.")

    def getrow(self, event):
        item = super(ProductTreeView, self).getrow(event)
        if item:
            print(item[3])
            self.t[0].set(item[0])
            self.t[1].set(item[1])
            self.t[2].set(item[2])
            self.t[3].set(item[3])

    def create(self):
        super(ProductTreeView, self).create()
        self.update()
        if sql_restaurant.Utilisateur.getAcces() >= 1:
            for i in range(4):
                self.lbls[i].configure(text=self.headings[i])
                if i < 2:
                    self.lbls[i].grid(row=0, column=i % 2, padx=1, sticky="news")
                    self.entrys[i].grid(row=1, column=i % 2, padx=1, sticky="n", pady=15)
                else:
                    self.lbls[i].grid(row=2, column=i % 2, padx=1, sticky="news")
                    self.entrys[i].grid(row=3, column=i % 2, padx=1, sticky="n", pady=15)

    def update(self):
        super(ProductTreeView, self).update()
        for i in sql_restaurant.getProductList():
            i = list(i)
            i.pop(0)
            i[3] = sql_restaurant.getCategorieNameById(i[3])
            print(i[3])
            self.tree.insert('', 'end', values=i)


class CategorieTreeView(MyTreeView):
    def __init__(self, widget, lbls=[], entrys=[], t=[]):
        headings = ["ID", "Nom"]
        super(CategorieTreeView, self).__init__(widget, headings, lbls, entrys, t)
        self.actual_item = None

    def edit(self, **kwargs):
        if self.isActualItem():
            msg = f"Souhaitez-vous vraiment mettre à jour cet élément ? ({self.actual_item[0]}, {self.actual_item[1]})"
            if super(CategorieTreeView, self).edit(msg):
                if not sql_restaurant.getCategorieIdByName(self.t[1].get()):
                    sql_restaurant.modifyCategorieName(self.actual_item[0], self.t[1].get())
                    messagebox.showinfo("Succes", f"({self.actual_item[0]}) modifier avec succès.")
                    self.update()
                else:
                    messagebox.showerror("Erreur", f"Une catégorie se nomme déjà {self.t[1].get()}")

    def add(self, **kwargs):
        msg = f"Souhaitez-vous vraiment ajouter cet élément ? ({self.t[1].get()})"
        if super(CategorieTreeView, self).add(msg):
            if not sql_restaurant.getCategorieIdByName(self.t[1].get()):
                sql_restaurant.addCategories(self.t[1].get())
                messagebox.showinfo("Succes", f"({self.t[1].get()}) ajouter avec succès.")
                self.update()
            else:
                messagebox.showerror("Erreur", "La catégorie entrée existe déjà dans la base de données !")

    def delete(self, **kwargs):
        if self.isActualItem():
            msg = f"Souhaitez-vous vraiment supprimer cet élément ? ({self.actual_item[0]}, {self.t[1].get()})"
            if super(CategorieTreeView, self).delete(msg):
                if not sql_restaurant.categorieIsUsed(self.actual_item[1]):
                    sql_restaurant.removeCategories(self.actual_item[1])
                    self.update()
                    messagebox.showinfo("Succes", f"({self.actual_item[0]}, {self.actual_item[1]}) supprimer avec succès.")
                    self.actual_item = None
                else:
                    messagebox.showerror("Erreur", f"({self.actual_item[0]}, {self.actual_item[1]}) est lié à certains produits, merci de changé d'abord les produits.")

    def getrow(self, event):
        item = super(CategorieTreeView, self).getrow(event)
        if item:
            self.t[0].set(item[0])
            self.t[1].set(item[1])

    def create(self):
        super(CategorieTreeView, self).create()
        self.update()
        if sql_restaurant.Utilisateur.getAcces() >= 1:
            for i in range(2):
                self.lbls[i].configure(text=self.headings[i])
                self.lbls[i].grid(row=i, column=0, padx=5, pady=3, sticky='wse')
                self.entrys[i].grid(row=i, column=1, padx=5, pady=3, sticky='wse')
            self.entrys[0].configure(state="disabled")

    def update(self):
        super(CategorieTreeView, self).update()
        for i in sql_restaurant.getCategoriesList():
            self.tree.insert('', 'end', values=i)

class UserTreeView(MyTreeView):
    def __init__(self, widget, lbls=[], entrys=[], t=[]):
        headings = ["ID", "Nom", "Mot de passe", "Acces"]
        super(UserTreeView, self).__init__(widget, headings, lbls, entrys, t)
        self.actual_item = None

    def edit(self, **kwargs):
        if self.isActualItem():
            msg = f"Souhaitez-vous vraiment mettre à jour cet élément ? ({self.actual_item[0]}, {self.actual_item[1]}, {self.actual_item[2]}, {self.actual_item[3]})"
            if super(UserTreeView, self).edit(msg):
                if not sql_restaurant.Utilisateur.getId() == (self.actual_item[0]):
                    if (self.actual_item[1] == self.t[1].get() or not sql_restaurant.getUserIdByName(self.t[1].get())):
                        sql_restaurant.modifyUser(self.actual_item[0], self.t[1].get(), self.t[2].get(), self.t[3].get())
                        messagebox.showinfo("Succes", f"({self.actual_item[0]}, {self.t[1].get()}, {self.t[2].get()}, {self.t[3].get()}) modifier avec succès.")
                        self.update()
                    else:
                        messagebox.showerror("Erreur", f"Un utilisateur se nomme déjà {self.t[1].get()}")
                else:
                    messagebox.showerror("Erreur", f"Vous ne pouvez pas modifier l'utilisateur avec lequel vous êtes connecté.")

    def add(self, **kwargs):
        msg = f"Souhaitez-vous vraiment ajouter cet élément ? ({self.t[0].get()}, {self.t[1].get()})"
        if super(UserTreeView, self).add(msg):
            if not sql_restaurant.getUserIdByName(self.t[1].get()):
                sql_restaurant.createUser(self.t[1].get(), self.t[2].get(), self.t[3].get())
                messagebox.showinfo("Succes", f"({self.t[1].get()}, {self.t[2].get()}, {self.t[3].get()}) ajouter avec succès.")
                self.update()
            else:
                messagebox.showerror("Erreur", f"Un utilisateur se nomme déjà {self.t[1].get()}")


    def delete(self, **kwargs):
        if self.isActualItem():
            msg = f"Souhaitez-vous vraiment supprimer cet élément ? ({self.t[0].get()}, {self.t[1].get()})"
            if super(UserTreeView, self).delete(msg):
                if not sql_restaurant.Utilisateur.getId() == (self.actual_item[0]):
                    sql_restaurant.removeUser(self.actual_item[0])
                    messagebox.showinfo("Succes", f"({self.actual_item[0]}, {self.actual_item[1]}, {self.actual_item[2]}, {self.actual_item[3]}) supprimer avec succès.")
                    self.update()
                    self.actual_item = None
                else:
                    messagebox.showerror("Erreur", f"Vous ne pouvez pas supprimer l'utilisateur avec lequel vous êtes connecté.")

    def getrow(self, event):
        item = super(UserTreeView, self).getrow(event)
        if item:
            self.t[0].set(item[0])
            self.t[1].set(item[1])
            self.t[2].set(item[2])
            self.t[3].set(item[3])

    def create(self):
        super(UserTreeView, self).create()
        for i in range(4):
            self.lbls[i].configure(text=self.headings[i])
            if i < 2:
                self.lbls[i].grid(row=0, column=i % 2, padx=1, sticky="news")
                self.entrys[i].grid(row=1, column=i % 2, padx=1, sticky="n", pady=15)
            else:
                self.lbls[i].grid(row=2, column=i % 2, padx=1, sticky="news")
                self.entrys[i].grid(row=3, column=i % 2, padx=1, sticky="n", pady=15)
        self.entrys[0].configure(state="disabled")
        self.update()

    def update(self):
        super(UserTreeView, self).update()
        for i in sql_restaurant.getUserList():
            i = list(i)
            self.tree.insert('', 'end', values=i)
