import tkinter as tk
from tkinter import ttk
import sqlite3
from AdsParser import Parser, Ad


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def link_tree(self):
        if self.tree.selection():
            selected_item = self.tree.selection()
            value = self.tree.item(selected_item, option="values")[4]
            import webbrowser
            webbrowser.open('{}'.format(value))


    def init_main(self):
        toolbar = tk.Frame(bg='#cfe8ff', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='lib/add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Искать недвижимость', command=self.open_dialog, bg='#cfe8ff', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='lib/delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#cfe8ff', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.redo_img = tk.PhotoImage(file='lib/redo.gif')
        btn_redo = tk.Button(toolbar, text='Удалить список', bg='#cfe8ff', bd=0, image=self.redo_img,
                               compound=tk.TOP, command=self.redo)
        btn_redo.pack(side=tk.LEFT)

        self.link_img = tk.PhotoImage(file='lib/link.gif')
        btn_link = tk.Button(toolbar, text='Перейти по ссылке', bg='#cfe8ff', bd=0, image=self.link_img,
                             compound=tk.TOP, command=self.link_tree)
        btn_link.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'address', 'description', 'costs', 'total'), height=15, show='headings')

        self.tree.column('ID', minwidth = 0, width=0, anchor=tk.CENTER)
        self.tree.column('address', minwidth = 230, width=230, anchor=tk.CENTER)
        self.tree.column('description', minwidth = 150, width=150, anchor=tk.CENTER)
        self.tree.column('costs', minwidth = 100, width=100, anchor=tk.CENTER)
        self.tree.column('total', minwidth = 0, width=0, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('address', text='Адрес')
        self.tree.heading('description', text='Описание')
        self.tree.heading('costs', text='Цена')
        self.tree.heading('total', text='Ссылка')

        self.tree.pack()

    def records(self, address, description, costs, total):
        self.db.insert_data(address, description, costs, total)
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM memory''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        for row in self.db.c.fetchall():
            self.tree.insert('', 'end', values=row)

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM memory WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def redo(self):
        for selection_item in self.tree.get_children():
            try:
                self.db.c.execute('''DELETE FROM memory WHERE id=?''', (self.tree.set(selection_item, '#1'),))
            except:
                pass
        self.db.conn.commit()
        self.view_records()


    def open_dialog(self):
        child = Child()

            
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def parsing(self, event):
        parser = Parser(city = self.entry_town.get(), buy = self.combobox1.get(), \
        house_type = self.combobox2.get(), price_min = self.entry_sum_min.get(),
        price_max=self.entry_sum_max.get(), metro=self.entry_metro.get())

        if (not parser.price_min):
            parser.price_min = '0'

        parser.page_init_yandex(10)

        k = 0
        i = 1
        while (k < 10) and (i):
            i = parser.get_ad_yandex(k)
            if (i):
                self.view.records(i.address, i.title, i.price, i.url)
                self.grab_set()
                self.focus_set()
                k+=1

        if (k == 0) and (not i):
            error = tk.Tk()
            error.title('Ошибка')
            error.geometry('250x120+480+370')
            label = tk.Label(error, text='По вашему запросу \n ничего не найдено', font='arial 13')
            label.place(x = 45, y = 30)
            
            
        
    def init_child(self):
        self.title('Меню')
        self.geometry('400x250+400+300')
        self.resizable(False, False)

        self.combobox1 = ttk.Combobox(self, values=[u'Снять', u'Купить', u'Посуточно'])
        self.combobox1.current(0)
        self.combobox1.place(x=200, y=20)

        label_description = tk.Label(self, text='Город:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Метро:')
        label_select.place(x=50, y=80)

        self.combobox2 = ttk.Combobox(self, values=[u'Квартира', u'Дом'])
        self.combobox2.current(0)
        self.combobox2.place(x=200, y=110)

        label_sum_min = tk.Label(self, text='Минимальная цена:')
        label_sum_min.place(x=50, y=140)
        label_sum_max = tk.Label(self, text='Максимальная цена:')
        label_sum_max.place(x=50, y=170)

        self.entry_town = ttk.Entry(self)
        self.entry_town.place(x=200, y=50)

        self.entry_metro = ttk.Entry(self)
        self.entry_metro.place(x=200, y=80)

        self.entry_sum_min = ttk.Entry(self)
        self.entry_sum_min.place(x=200, y=140)

        self.entry_sum_max = ttk.Entry(self)
        self.entry_sum_max.place(x=200, y=170)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=200)

        
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=200)
        self.btn_ok.bind('<Button-1>', self.parsing)
        # Здесь надо отправить запрос в парсер
        
        
# Создание базы данных в memory.db
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('lib/memory.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS memory (id integer primary key, address text, description text, costs text, 
            total text)''')
        self.conn.commit()

    def insert_data(self, address, description, costs, total):
        self.c.execute('''INSERT INTO memory(address, description, costs, total) VALUES (?, ?, ?, ?)''',
                       (address, description, costs, total))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("House search")
    root.geometry("500x450+350+200")
    root.resizable(False, False)
    root.mainloop()

