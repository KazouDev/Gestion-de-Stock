#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 10:31:33 2022

@author: b311-06
"""
import sqlite3
import datetime
from second_files.User import User

con = sqlite3.connect('./Stock.db')
Utilisateur = User()


def createUser(name, password, acces):
    cur = con.cursor()
    if cur.execute(f"SELECT * FROM Users WHERE name='{name}'").fetchone():
        print("Les noms d'utilisateurs doivent être unique.")
        return False
    cur.execute("INSERT INTO Users(name, password, niveau) VALUES (?,?,?)", (name, password, acces))
    con.commit()
    print("Utilisateur créer")
    return True

def removeUser(id):
    cur = con.cursor()
    if cur.execute(f"SELECT * FROM Users WHERE id='{id}'").fetchone():
        cur.execute(f"DELETE FROM Users WHERE id='{id}'")
        print(f"Succes: Utilisateur {id} supprimé")
        return True
    else:
        print(f"Error: Pas d'utilisateur {id}")
        return False

def getUserList():
    cur = con.cursor()
    result = cur.execute("SELECT * FROM Users").fetchall()
    con.commit()
    return result

def modifyUser(id, name, password, acces):
    cur = con.cursor()
    user_list = [i[0] for i in getUserList()]
    if id in user_list:
        cur.execute(f"UPDATE Users SET name = '{name}', password='{password}', niveau='{acces}' WHERE id='{id}'")
        con.commit()
        return True
    else:
        print(f"Users {id} doesn't exist")
        return False

def getUserIdByName(name):
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM Users WHERE name='{name}'").fetchone()
    con.commit()
    if result:
        return result[0]
    else:
        return False

def connection(name, password):
    cur = con.cursor()
    cur.execute(f"SELECT * FROM Users WHERE name='{name}' AND password='{password}'")
    result = cur.fetchone()
    if not result:
        return False
    else:
        Utilisateur.login(result)
        return True


def addCategories(name):
    if Utilisateur.getAcces() == 2:
        cur = con.cursor()
        if cur.execute(f"SELECT * FROM Categories WHERE name='{name}'").fetchone():
            print("Error: Categories with this name is already existing.")
            return False
        else:
            cur.execute("INSERT INTO Categories(name) VALUES (?)", (name,))
            con.commit()
            print(f"Succes: Categories {name} create.")
            return True
    else:
        print("Vous n'avez pas la permission de faire ceci.")
        return False

def removeCategories(name):
    if Utilisateur.getAcces() == 2:
        cur = con.cursor()
        if cur.execute(f"SELECT * FROM Categories WHERE name='{name}'").fetchone():
            cur.execute(f"DELETE FROM Categories WHERE name='{name}'")
            con.commit()
            print("Succes: Categories with this name is now delete.")
            return True
        else:
            print("Error: Categories with this name is not in database.")
            return False
    else:
        print("Vous n'avez pas la permission de faire ceci.")
        return False
    
def getCategoriesList():
    cur = con.cursor()
    result = cur.execute("SELECT * FROM Categories").fetchall()
    con.commit()
    return result

def modifyCategorieName(id, newname):
    cur = con.cursor()
    categories_list = [i[0] for i in getCategoriesList()]
    if id in categories_list:
        cur.execute(f"UPDATE Categories SET name = '{newname}' WHERE id='{id}'")
        con.commit()
        return True
    else:
        print(f"Categorie {id} doesn't exist")
        return False

def categorieIsUsed(name):
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM Produit WHERE idCategorie='{getCategorieIdByName(name)}'").fetchone()
    print(result)
    con.commit()
    if result:
        return True
    else:
        return False

def getCategorieIdByName(name):
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM Categories WHERE name='{name}'").fetchone()
    con.commit()
    if result:
        return result[0]
    else:
        return False

def getCategorieNameById(id):
    cur = con.cursor()
    result = cur.execute(f"SELECT name FROM Categories WHERE id='{id}'").fetchone()
    con.commit()
    if result:
        return result[0]
    else:
        return False

def addProduct(name, pricebuy, pricesell, categorie):
    cur = con.cursor()
    list_product = [i[1] for i in getProductList()]
    if name in list_product:
        print(f"Product {name} already in database")
        return False
    else:
        cur.execute(f"INSERT INTO Produit(name, price_buy, price_sell, idCategorie) VALUES (?, ?, ?, ?)", (name, pricebuy, pricesell, getCategorieIdByName(categorie)))
        con.commit()
        print(f"Product {name} added to database.")
        return True


def getProductList():
    cur = con.cursor()
    result = cur.execute("SELECT * FROM Produit").fetchall()
    con.commit()
    return result

def removeProduct(name):
    cur = con.cursor()
    list_product = [i[1] for i in getProductList()]
    if name in list_product:
        cur.execute(f"DELETE FROM Produit WHERE name = '{name}'")
        con.commit()
        return True
    else:
        print(f"Product {name} not in database.")
        return False

def updateProduct(id, newname=None, pricebuy=None, pricesell=None, idCategorie=None):
    args = [newname, pricebuy, pricesell, idCategorie]
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM Produit WHERE id_prod = '{id}'").fetchone()
    print(result)
    if result:
        for i in range(len(args)):
            if not args[i]:
                args[i] = result[i+1]
        print(args)
        cur.execute(f"UPDATE Produit SET name = '{args[0]}', price_buy = '{args[1]}', price_sell = '{args[2]}', idCategorie = '{idCategorie}' WHERE id_prod = '{id}'")
        con.commit()
        return True
    else:
        return False

def getProductIdByName(name):
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM Produit WHERE name='{name}'").fetchone()
    con.commit()
    if result:
        return result[0]
    else:
        return False

def getProductNameById(id):
    cur = con.cursor()
    result = cur.execute(f"SELECT name FROM Produit WHERE id_prod='{id}'").fetchone()
    con.commit()
    if result:
        return result[0]
    else:
        return False

def productIsUsed(name):
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM Stock WHERE id_prod='{getProductIdByName(name)}'").fetchone()
    con.commit()
    if result:
        return True
    else:
        return False
def addStock(name, date_arr, nombre, date_per):
    cur = con.cursor()
    id = getProductIdByName(name)
    if not date_arr:
        date_arr = datetime.date.today()
    result = cur.execute(f"SELECT * FROM Stock WHERE id_prod = '{id}' AND date_arrive = '{date_arr}'").fetchone()
    if result:
        nombre = float(nombre) + result[2]
        cur.execute(f"UPDATE Stock SET nombre = '{nombre}' WHERE id_prod = '{id}' AND date_arrive = '{date_arr}'")
        con.commit()
        return False
    else:
        cur.execute(f"INSERT INTO Stock(id_prod, date_arrive, nombre, date_per) VALUES (?, ?, ?, ?)", (id, date_arr, nombre, date_per))
        con.commit()
        print("Stock added")
        return True


def remStock(name, date_arr, nombre=None):
    id = getProductIdByName(name)
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM Stock WHERE id_prod = '{id}' AND date_arrive = '{date_arr}'").fetchone()
    if result:
        print(result)
        if nombre:
            nombre = result[2] - nombre
            cur.execute(f"UPDATE Stock SET nombre = '{nombre}' WHERE id_prod = '{id}' AND date_arrive = '{date_arr}'")
            con.commit()
            print("Stock Update")
            return True
        else:
            cur.execute(f"DELETE FROM Stock WHERE id_prod = '{id}' AND date_arrive = '{date_arr}'")
            con.commit()
            print("stock okay")
            return True
        
def updateStock(id_prod, arrive, nombre, per):
    cur = con.cursor()
    cur.execute(f"UPDATE Stock SET id_prod = '{id_prod}', date_arrive = '{arrive}', nombre = '{nombre}', date_per = '{per}' WHERE id_prod = '{id_prod}' AND date_arrive = '{arrive}'")
    con.commit()
    return True


def getStockList():
    cur = con.cursor()
    result = cur.execute("SELECT * FROM Stock")
    con.commit()
    return result.fetchall()
