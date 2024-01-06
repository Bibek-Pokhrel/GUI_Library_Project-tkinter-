from tkinter import Tk, Button,Label,Scrollbar,Listbox,StringVar,Entry,W,E,N,S,END
from tkinter import ttk
from tkinter import messagebox
from mysql_config import dbconfig
import mysql.connector as pyo
#mybooks=pyo.connect(host="localhost",user="root",password="pokhrel98550")

con = pyo.connect(**dbconfig)
cursor=con.cursor()

class Bookdb:
    def __init__(self) -> None:
        self.con=pyo.connect(**dbconfig)
        self.cursor=con.cursor()
        print("you have connected to the database")
        print(con)

    def __del__(self):
        self.con.close()

    def view(self):
        self.cursor.execute("select * from books")
        rows=self.cursor.fetchall()
        return rows
    

    def insert(self,title,author,isbn):
        sql=("INSERT INTO books(title,author,isbn)VALUES(%s,%s,%s)")
        values=[title,author,isbn]
        self.cursor.execute(sql,values)
        self.con.commit()
        messagebox.showinfo(title="Book Database",message="New Books added to database")


    def update(self,id,title,author,isbn):
        tsql= 'UPDATE books SET title=%s,author=%s,isbn=%s WHERE id=%s'
        self.cursor.execute(tsql,[title,author,isbn,id])
        self.con.commit()
        messagebox.showinfo(title="Book Database",message="Book Updated")


    def delete(self,id):
        delquery='DELETE FROM books WHERE id=%s'
        self.cursor.execute(delquery,[id])
        self.con.commit()
        messagebox.showinfo(title="Book Database",message="Book Deleted")

db=Bookdb()


def get_selected_row(event):
    global selected_tuple
    index= list_box.curselection()[0]
    selected_tuple= list_box.get(index)
    title_entry.delete(0,'end')
    title_entry.insert('end',selected_tuple[1])
    author_entry.delete(0,'end')
    author_entry.insert('end',selected_tuple[2])
    isbn_entry.delete(0,'end')
    isbn_entry.insert('end',selected_tuple[3])

def view_record():
    list_box.delete(0,'end')
    for row in db.view():
        list_box.insert('end',row)

def add_book():
    db.insert(title_text.get(),author_text.get(),isbn_text.get())
    list_box.delete(0,'end')
    list_box.insert('end',(title_text.get(),author_text.get(),isbn_text.get()))
    title_entry.delete(0,"end")
    author_entry.delete(0,"end")
    isbn_entry.delete(0,"end")
    con.commit()


def delete_record():
    db.delete(selected_tuple[0])
    con.commit()


def clear_screen():
    list_box.delete(0,'end')
    title_entry.delete(0,'end')
    author_entry.delete(0,'end')
    isbn_entry.delete(0,'end')


def update_records():
    db.update(selected_tuple[0],title_text.get(),author_text.get(),isbn_text.get())
    title_entry.delete(0,"end")
    author_entry.delete(0,"end")
    isbn_entry.delete(0,"end")
    con.commit()

def on_closing():
    dd=db
    if messagebox.askokcancel("Quit","Do you want to quit?"):
        root.destroy()
        del dd








root = Tk()

root.title("my bookd application")
root.configure(background="light blue")
root.geometry("850x500")
root.resizable(width=False,height=False)

title_label=ttk.Label(root,text="Title",background="light blue",font=("TkDeafultFont",16))
title_label.grid(row=0,column=0,sticky=W)
title_text=StringVar()
title_entry=ttk.Entry(root,width=24,textvariable=title_text)
title_entry.grid(row=0,column=1,sticky=W)

author_label=ttk.Label(root,text="Author",background="light blue",font=("tkDeafultFont",16))
author_label.grid(row=0,column=2,sticky=E)
author_text=StringVar()
author_entry=ttk.Entry(root,width=24,textvariable=author_text)
author_entry.grid(row=0,column=3,sticky=W)

isbn_label=ttk.Label(root,text="ISBN",background="light blue",font=("tkDeafultFont",16))
isbn_label.grid(row=0,column=4,sticky=E)
isbn_text=StringVar()
isbn_entry=ttk.Entry(root,width=24,textvariable=isbn_text)
isbn_entry.grid(row=0,column=5,sticky=W)

add_buttons=Button(root,text="Add Books",bg="blue",fg="white",font="helvetica 10 bold",command=add_book)
add_buttons.grid(row=1,column=3,sticky=W)

list_box=Listbox(root,height=16,width=40,font="helvetica 13",bg="white")
list_box.grid(row=4,column=1,columnspan=14,sticky=W+E,pady=40,padx=15)
list_box.bind('<<Listboxselect>>',get_selected_row)

scroll_bar=Scrollbar(root)
scroll_bar.grid(row=1,column=8,rowspan=14,sticky=W)

list_box.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_box.yview)

modify_btn=Button(root,text="Modify Record",bg="purple",fg="white",font="helvetica 10 bold",command=update_records)
modify_btn.grid(row=15,column=3)

view_btn=Button(root,text="view all record",bg="black",fg="white",font="helvetica 10 bold",command=view_record)
view_btn.grid(row=15,column=1)

delete_btn=Button(root,text="Delete Record",bg="red",fg="white",font="helvetica 10 bold",command=delete_record)
delete_btn.grid(row=15,column=2)

clear_btn=Button(root,text="clear Records",bg="maroon",fg="white",font="helvetica 10 bold",command=clear_screen)
clear_btn.grid(row=15,column=4)

exit_btn=Button(root,text="exit application",bg="blue",fg="white",font="helvetica 10 bold",command=root.destroy)
exit_btn.grid(row=15,column=5)

root.mainloop()