#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from ttkthemes import ThemedStyle

class ProjectDirectoryCreator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("StuctDir Directory Creator")
        self.geometry("500x600")
        self.configure_style()
        
        # Attempt to set the window icon if the icon file exists
        icon_path = os.path.join(os.getcwd(), "./icon.ico")
        try:
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except tk.TclError as e:
            print(f"Error setting window icon: {e}")
        
        
        self.folder_structure = {}
        self.selected_template = ""

        self.create_widgets()

    def configure_style(self):
        self.style = ThemedStyle(self)
        self.style.set_theme("arc")# "adapta"
                                # "arc"
                                # "black"
                                # "blue"
                                # "breeze"
                                # "clearlooks"
                                # "equilux"
                                # "keramik"
                                # "plastik"
                                # "radiance"
                                # "smog"
                                # "ubuntu"
        
        ## Standard Theme
        #self.style = ttk.Style()
        #self.style.theme_use("clam")  # Use a modern ttk theme
        #self.style.configure("Treeview", font=("Helvetica", 12), rowheight=30, fieldbackground="#f0f0f0")
    
    def create_widgets(self):
        
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Add menu for save and load templates
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Templates", menu=self.file_menu)

        # Add buttons to menu
        self.file_menu.add_command(label="Save Template", command=self.save_template)
        self.file_menu.add_command(label="Load Template", command=self.load_template)
        
        self.label_frame = ttk.LabelFrame(self, text="Project Structure")
        self.label_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.treeview = ttk.Treeview(self.label_frame, selectmode='browse', show='tree') 
        self.treeview.pack(pady=10, padx=10, fill='both', expand=True)

        self.add_button = ttk.Button(self, text="Add Folder", command=self.add_folder)
        self.add_button.pack(pady=5)

        self.rename_button = ttk.Button(self, text="Rename", command=self.rename_item)
        self.rename_button.pack(pady=5)
        
        self.delete_button = ttk.Button(self, text="Delete", command=self.delete_item)
        self.delete_button.pack(pady=5)

        # Add a separator before the "Create Directories" button
        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill='x', pady=5)

        # Add a button to crate directories  
        self.create_dir_button = ttk.Button(self, text="Create Directories", command=self.create_directories)
        self.create_dir_button.pack(pady=10)

        # Bind the TreeviewSelect event to handle drag-and-drop
        self.treeview.bind("<B1-Motion>", self.handle_drag_and_drop)

    
    def add_folder(self):
        parent = self.treeview.focus()
        if not parent:
            parent = ''
        folder_name = tk.simpledialog.askstring("Add Folder", "Enter folder name:")
        if folder_name:
            self.treeview.insert(parent, 'end', text=folder_name)
            self.folder_structure[parent + '/' + folder_name] = []

    def delete_item(self):
        selected_item = self.treeview.selection()
        if selected_item:
            self.treeview.delete(selected_item)
            
    def rename_item(self):
        selected_item = self.treeview.selection()
        if selected_item:
            item_id = selected_item[0]
            folder_name = self.treeview.item(item_id, "text")
            new_name = simpledialog.askstring("Rename Folder", "Enter new folder name:", initialvalue=folder_name)
            if new_name:
                self.treeview.item(item_id, text=new_name)
                self.update_folder_structure()


    def save_template(self):
        templates_folder = os.path.join(os.getcwd(), "./templates")

        if not os.path.exists(templates_folder):
            try:
                os.makedirs(templates_folder)
            except OSError:
                tk.messagebox.showerror("Error", "Failed to create 'templates' folder.")
                return

        template_filename = filedialog.asksaveasfilename(
            title="Save Template",
            initialdir=templates_folder,  # Set the initial directory to the "templates" folder
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
        )

        if not template_filename:
            return

        template_name = os.path.splitext(os.path.basename(template_filename))[0]

        self.folder_structure[template_name] = self.get_structure_from_treeview()

        with open(template_filename, "w") as file:
            json.dump(self.folder_structure[template_name], file)

        tk.messagebox.showinfo("Template Saved", f"Template saved to {template_filename}.")


    def load_template(self):
        templates_folder = os.path.join(os.getcwd(), "./templates")

        if not os.path.exists(templates_folder):
            tk.messagebox.showerror("Error", "The 'templates' folder does not exist. Please create a templates folder in the application root directory")
            templates_folder=os.getcwd()
            
        
        
        file_path = filedialog.askopenfilename(
            title="Load Template",
            initialdir=templates_folder,  # Set the initial directory to the "templates" folder
            filetypes=[("JSON Files", "*.json")],
        )
        
        if file_path:
            with open(file_path, "r") as f:
                self.clear_treeview()
                structure = json.load(f)
                self.populate_treeview(structure)

    def create_directories(self):
        directory = filedialog.askdirectory(title="Select Directory to Create Folders")
        if directory:
            structure = self.get_structure_from_treeview()
            self.create_folders(directory, structure)

    def get_structure_from_treeview(self):
        structure = []
        for item in self.treeview.get_children():
            structure.append(self.get_item_structure(item))
        return structure

    def get_item_structure(self, item):
        item_structure = {
            'name': self.treeview.item(item, "text"),
            'subfolders': []
        }
        for child in self.treeview.get_children(item):
            item_structure['subfolders'].append(self.get_item_structure(child))
        return item_structure

    def populate_treeview(self, structure, parent=''):
        for item in structure:
            folder_name = item['name']
            subfolders = item['subfolders']
            item_id = self.treeview.insert(parent, 'end', text=folder_name)
            if subfolders:
                self.populate_treeview(subfolders, parent=item_id)

    def clear_treeview(self):
        self.treeview.delete(*self.treeview.get_children())

    def create_folders(self, parent_directory, structure):
        for item in structure:
            folder_name = item['name']
            folder_path = os.path.join(parent_directory, folder_name)
            os.makedirs(folder_path)
            subfolders = item['subfolders']
            if subfolders:
                self.create_folders(folder_path, subfolders)
    
    
    def handle_drag_and_drop(self, event):
        x, y = event.x, event.y
        item_id = self.treeview.identify_row(y)
        dragged_item = self.treeview.selection()[0]

        if not item_id or item_id == dragged_item or item_id in self.treeview.get_children(dragged_item):
            return

        if self.treeview.parent(item_id):
            parent_item = self.treeview.parent(item_id)
        else:
            parent_item = ""

        self.treeview.move(dragged_item, parent_item, self.treeview.index(item_id))
        self.update_folder_structure()

    def update_folder_structure(self, parent="", parent_structure=None):
        if parent_structure is None:
            parent_structure = self.folder_structure

        items = self.treeview.get_children(parent)
        subfolders = []
        for item in items:
            folder_name = self.treeview.item(item, "text")
            subfolder_structure = self.update_folder_structure(item)
            subfolders.append({'name': folder_name, 'subfolders': subfolder_structure})

        parent_structure[parent] = subfolders
        return subfolders

if __name__ == "__main__":
    app = ProjectDirectoryCreator()
    app.mainloop()


# In[ ]:





# In[ ]:




