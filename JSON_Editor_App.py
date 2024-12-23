import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import tkinter.filedialog

###Arvind Ram###
###arvind02.ram@gmail.com###
###https://github.com/Arvind2002###
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JSON Creation Utility - Created by https://github.com/Arvind2002")


        # self.state("zoomed")
        self.geometry("370x500")
        # self.geometry("115x300")
        self.save_name = 'LR-EMR-status-mapping.json'
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=1)
        self.fields = {}
        self.tab_list = {}
        # self.config_file_path = "./resources/resources.json"
        # self.resource_config = ''
        # with open(self.config_file_path,"r") as f:
        #     self.resource_config = json.load(f)
        # self.save_name = self.resource_config.get("default_file_name")
        self.filename = None
        self.selected_tab = None
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open File", command=self.open_json_file)
        file_menu.add_command(label="New File", command=self.new_json_file)
        menubar.add_cascade(label="File", menu=file_menu)
        config_menu = tk.Menu(menubar, tearoff=0)
        config_menu.add_command(label="Set Default File Path and Name", command=self.set_default_file)
        menubar.add_cascade(label="Configure", menu=config_menu)
        self.config(menu=menubar)

        my_canvas = tk.Canvas(self.frame)
        my_canvas.pack(side="left", fill="both", expand=True)
        my_scrollbar1 = ttk.Scrollbar(self.frame, orient="vertical", command=my_canvas.yview)
        my_scrollbar1.pack(side="right", fill="y")
        # my_scrollbar2 = ttk.Scrollbar(self.frame, orient="horizontal", command=my_canvas.xview)
        # my_scrollbar2.pack(side="bottom", fill="x")
        # my_canvas.configure(yscrollcommand=my_scrollbar1.set, xscrollcommand=my_scrollbar2.set)
        my_canvas.configure(yscrollcommand=my_scrollbar1.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
        self.second_frame = tk.Frame(my_canvas)
        my_canvas.create_window((0, 0), window=self.second_frame, anchor="nw")

        self.notebook = ttk.Notebook(self.second_frame)
        self.notebook.grid(row=10, column=0, columnspan=3, sticky="nsew")
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.filename_label = tk.Label(self.second_frame, text="Create a New File")
        self.filename_label.grid(row=0, column=0, columnspan=3, pady=5)

        self.add_tab_button = tk.Button(self.second_frame, text="Add Tab", command=self.add_tab)
        self.add_tab_button.grid(row=1, column=0, pady=10)
        self.delete_tab_button = tk.Button(self.second_frame, text="Delete Tab", command=self.delete_tab)
        self.delete_tab_button.grid(row=1, column=1, pady=10)
        self.edit_tab_button = tk.Button(self.second_frame, text="Edit Tab", command=self.edit_tab)
        self.edit_tab_button.grid(row=1, column=2, pady=10)

        self.checkbox_var = tk.BooleanVar()

        self.checkbox = tk.Checkbutton(self.second_frame, text="Enable current tab as list", variable=self.checkbox_var,
                                       command=self.on_checkbox_click)
        self.checkbox.grid(row=2, column=1)

        self.add_button = tk.Button(self.second_frame, text="+", command=self.add_text_fields)
        self.add_button.grid(row=4, column=0, pady=10)

        self.remove_button = tk.Button(self.second_frame, text="-", command=self.remove_text_fields)
        self.remove_button.grid(row=4, column=2)

        self.save_button = tk.Button(self, text="Save", command=self.save_data)
        self.save_button.pack(pady=(10, 0))

        self.save_as_button = tk.Button(self, text="Save as", command=self.save_as_data)
        self.save_as_button.pack(pady=(0, 10))

        self.start_up()

    def start_up(self):
        new_tab_name = tk.simpledialog.askstring("Add Tab", "Enter the name for the new tab:")
        if new_tab_name:
            self.add_tab(new_tab_name = new_tab_name)
        else:
            messagebox.showinfo("Welcome", "Please Select a file to Open")
            filename = tkinter.filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if filename:
                self.open_json_file(filename)
            else:
                self.show_error("Please add a tab or Choose a file to Open")
                quit()



    def on_tab_change(self,event):
        if len(self.fields)!=0:
            current_tab = self.notebook.select()
            tab_index = self.notebook.index(current_tab)
            self.set_checkbox_state(self.tab_list[tab_index])

    def set_default_file(self):
        curr_filename = tkinter.filedialog.asksaveasfilename(defaultextension=".json",
                                                             filetypes=[("JSON files", "*.json")],
                                                             initialdir=os.getcwd(),
                                                             initialfile=self.save_name)
        if curr_filename:
            self.save_name = curr_filename
            # self.resource_config['default_file_name'] = os.path.basename(self.save_name)
            # with open(self.config_file_path, 'w') as f:
            #     json.dump(self.resource_config, f)

    def on_checkbox_click(self):
        if len(self.fields) != 0:
            tab = self.notebook.select()
            if tab is not None:
                tab_index = self.notebook.index(tab)
                self.clear_tab(tab_index)
                if self.checkbox_var.get():
                    self.tab_list[tab_index] = True
                else:
                    self.tab_list[tab_index] = False
                self.add_text_fields()


    def set_checkbox_state(self, value):
        self.checkbox_var.set(value)

    def add_tab(self, new_tab_name=None, islist=None):
        new_flag = False
        if new_tab_name is None:
            new_flag = True;
            new_tab_name = tk.simpledialog.askstring("Add Tab", "Enter the name for the new tab:")
        if new_tab_name:
            new_frame = ttk.Frame(self.notebook)
            self.notebook.add(new_frame, text=new_tab_name)
            tab_index = self.notebook.index("end") - 1  # get the index of the newly added tab
            self.notebook.select(tab_index)
            self.fields[tab_index] = []
            if islist is None:
                islist = False
            self.tab_list[tab_index] = islist
            self.set_checkbox_state(islist)
            if new_flag:
                self.add_text_fields()
            return tab_index

    def delete_tab(self):
        current_tab = self.notebook.select()
        if current_tab:
            tab_index = self.notebook.index(current_tab)
            self.notebook.forget(current_tab)
            del self.fields[tab_index]
            self.fields = {i: v for i, (k, v) in enumerate(sorted(self.fields.items()))}
            del self.tab_list[tab_index]
            self.tab_list = {i: v for i, (k, v) in enumerate(sorted(self.tab_list.items()))}
            if len(self.fields) == 0:
                self.geometry("370x500")
            print(self.fields)
            print(self.tab_list)


    def edit_tab(self):
        current_tab = self.notebook.select()
        if current_tab:
            new_tab_name = tk.simpledialog.askstring("Edit Tab", "Enter the new name for the tab:")
            if new_tab_name:
                self.notebook.tab(current_tab, text=new_tab_name)

    def get_tab_frame(self, tab):
        return self.notebook.nametowidget(tab)

    def get_tab_name_from_index(self, tab_index):
        return self.notebook.tab(tab_index, "text")

    def add_text_fields(self, key=None, value=None, tab=None):
        if len(self.fields) == 0:
            self.show_error("No tabs Added")
        else:
            if tab is None:
                tab = self.notebook.select()
            self.geometry("550x500")
            tab_index = self.notebook.index(tab)
            tab_frame = self.get_tab_frame(tab)
            if tab_index not in self.fields:
                self.fields[tab_index] = []

            if self.tab_list[tab_index]:
                value_field = tk.Entry(tab_frame)
                if value is not None:
                    value_field.insert(0, value)
                row_index = len(self.fields[tab_index]) + 1
                value_field.grid(row=len(self.fields[tab_index]) + 5, column=0, columnspan=2)
                remove_button = tk.Button(tab_frame, text="Delete",
                                          command=lambda index=row_index: self.remove_selected_row(index - 1,
                                                                                                   tab_index, self.tab_list[tab_index]))
                remove_button.grid(row=len(self.fields[tab_index]) + 5, column=2)
                self.fields[tab_index].append((value_field, remove_button))

            else:
                key_field = tk.Entry(tab_frame)
                value_field = tk.Entry(tab_frame)
                if key is not None and value is not None:
                    key_field.insert(0, key)
                    value_field.insert(0, value)

                row_index = len(self.fields[tab_index]) + 1
                key_field.grid(row=len(self.fields[tab_index]) + 5, column=0)
                value_field.grid(row=len(self.fields[tab_index]) + 5, column=1)
                remove_button = tk.Button(tab_frame, text="Delete",
                                          command=lambda index=row_index: self.remove_selected_row(index - 1,
                                                                                                   tab_index, self.tab_list[tab_index]))
                remove_button.grid(row=len(self.fields[tab_index]) + 5, column=2)
                self.fields[tab_index].append((key_field, value_field, remove_button))

    def remove_selected_row(self, index, tab_index, isList):
        if len(self.fields) == 0:
            self.show_error("No tabs Present")
        else:
            if isList:
                if 0 <= index < len(self.fields[tab_index]):
                    value_field, remove_button = self.fields[tab_index].pop(index)
                    value_field.destroy()
                    remove_button.destroy()
                    for i, (value_field, remove_button) in enumerate(self.fields[tab_index]):
                        value_field.grid(row=i + 5, column=0, columnspan=2)
                        remove_button.grid(row=i + 5, column=2)
                        remove_button.config(command=lambda curr_index=i: self.remove_selected_row(curr_index, tab_index, isList))
            else:
                if 0 <= index < len(self.fields[tab_index]):
                    key_field, value_field, remove_button = self.fields[tab_index].pop(index)
                    key_field.destroy()
                    value_field.destroy()
                    remove_button.destroy()
                    for i, (key_field, value_field, remove_button) in enumerate(self.fields[tab_index]):
                        key_field.grid(row=i + 5, column=0)
                        value_field.grid(row=i + 5, column=1)
                        remove_button.grid(row=i + 5, column=2)
                        remove_button.config(command=lambda curr_index=i: self.remove_selected_row(curr_index, tab_index, isList))

    def remove_text_fields(self):
        try:
            tab = self.notebook.select()
            tab_index = self.notebook.index(tab)
            if self.fields[tab_index]:
                if self.tab_list[tab_index]:
                    value_field, remove_button = self.fields[tab_index].pop()
                    value_field.destroy()
                    remove_button.destroy()
                else:
                    key_field, value_field, remove_button = self.fields[tab_index].pop()
                    key_field.destroy()
                    value_field.destroy()
                    remove_button.destroy()
        except Exception as e:
            self.show_error("No Field to Delete")

    def new_json_file(self):
        self.clear_text_fields()
        self.filename_label.config(text="Create a New File")
        self.fields = {}
        self.filename = None
        self.geometry("370x500")

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def populate_dict_from_json(self, json_data, tab_index):
        for key, value in json_data.items():
            self.add_text_fields(key=key, value=value, tab=self.notebook.tabs()[tab_index])

    def populate_list_from_json(self, json_data, tab_index):
        for value in json_data:
            self.add_text_fields(value=value, tab=self.notebook.tabs()[tab_index])

    def save_as_data(self):
        curr_filename = tkinter.filedialog.asksaveasfilename(defaultextension=".json",
                                                             filetypes=[("JSON files", "*.json")],
                                                             initialfile=self.save_name)
        if curr_filename:
            self.filename = curr_filename
            self.save_data()

    def save_data(self):
        if not self.filename:
            self.filename = self.save_name
        print(self.filename)
        data = {}
        for tab, fields in self.fields.items():
            if self.tab_list[tab]:
                section_data = []
                for value_entry, _ in fields:
                    section_data.append(value_entry.get())
                data[self.get_tab_name_from_index(tab)] = section_data
            else:
                section_data = {}
                for key_entry, value_entry, _ in fields:
                    section_data[key_entry.get()] = value_entry.get()
                data[self.get_tab_name_from_index(tab)] = section_data
        with open(self.filename, 'w') as file:
            json.dump(data, file)
        self.filename_label.config(text=os.path.basename(self.filename))
        tk.messagebox.showinfo("File Saved", f"{os.path.basename(self.filename)} Date Saved!")


    def open_json_file(self, filename=None):
        try:
            if filename is None:
                filename = tkinter.filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
                if filename:
                    self.filename = filename
                    with open(filename, 'r') as file:
                        json_data = json.load(file)
                    self.clear_text_fields()
                    self.fields = {}
                    for json_item in json_data:
                        if isinstance(json_data.get(json_item), list):
                            curr_tab = self.add_tab(json_item, True)
                            self.populate_list_from_json(json_data.get(json_item), curr_tab)
                        else:
                            curr_tab = self.add_tab(json_item, False)
                            self.populate_dict_from_json(json_data.get(json_item), curr_tab)

                    self.filename_label.config(text=os.path.basename(self.filename))
            else:
                self.filename = filename
                with open(filename, 'r') as file:
                    json_data = json.load(file)
                self.clear_text_fields()
                self.fields = {}
                for json_item in json_data:
                    if isinstance(json_data.get(json_item), list):
                        curr_tab = self.add_tab(json_item, True)
                        self.populate_list_from_json(json_data.get(json_item), curr_tab)
                    else:
                        print(f"{json_item} : dict")
                        curr_tab = self.add_tab(json_item, False)
                        self.populate_dict_from_json(json_data.get(json_item), curr_tab)
                self.filename_label.config(text=os.path.basename(self.filename))
        except Exception as e:
            print(str(e))
            self.show_error(f"Error in Opening File.")

    def clear_text_fields(self):
        for tab_index, fields in list(self.fields.items()):
            tab_frame = self.notebook.tabs()[0]
            self.notebook.forget(tab_frame)

    def clear_tab(self,tab_index):

        if self.tab_list[tab_index]:
            for value_field, remove_button in self.fields[tab_index]:
                value_field.destroy()
                remove_button.destroy()
                self.fields[tab_index] = []
        else:
            for key_field, value_field,remove_button in self.fields[tab_index]:
                key_field.destroy()
                value_field.destroy()
                remove_button.destroy()
                self.fields[tab_index] = []


if __name__ == "__main__":
    app = GUI()
    app.mainloop()
