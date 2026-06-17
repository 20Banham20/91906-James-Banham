import json
from logging import root
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List,Tuple

class FoodItem:
    def __init__(self, name:str, calories_per_100g:float, carbs_per_100g:float, protein_per_100g:float, fat_per_100g:float):
        self.name = name
        self.calories_per_100g = calories_per_100g
        self.carbs_per_100g = carbs_per_100g
        self.protein_per_100g = protein_per_100g
        self.fat_per_100g = fat_per_100g

    def get_nutrition(self, grams:float):
        factor = grams / 100
        return {
            'calories': self.calories_per_100g * factor,
            'carbs': self.carbs_per_100g * factor,
            'protein': self.protein_per_100g * factor,
            'fat': self.fat_per_100g * factor
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'name': self.name,
            'calories_per_100g': self.calories_per_100g,
            'carbs_per_100g': self.carbs_per_100g,
            'protein_per_100g': self.protein_per_100g,
            'fat_per_100g': self.fat_per_100g
        }
    
class FoodDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.food_items = [FoodItem("Chicken Breast", 165, 0, 31, 3.6), FoodItem("White Rice", 130, 28, 2.7, 0.3)]
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.food_items = [FoodItem(**item) for item in data]
            

    def add_food_item(self, food_item:FoodItem):
        self.food_items.append(food_item)  

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump([food.to_dict() for food in self.food_items], f, indent=2)    

    def remove_food_item(self, database: int):
        if 0 <= database < len(self.food_items):
            del self.food_items[database]
            self.save()
        else:
            raise IndexError("Food item index out of range.")  

class NutritionTrackerApp:
    def __init__(self):
        self.food_db = FoodDatabase("food_database.json")
        self.food_log = Foodlog("food_log.json")
        
        root = tk.Tk()
        root.geometry('800x580')
        root.title('Nutrition Tracker')

        # create a notebook
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        # create frames
        frame1 = ttk.Frame(notebook, width=800, height=580)
        frame2 = ttk.Frame(notebook, width=800, height=580)
        frame3 = ttk.Frame(notebook, width=800, height=580)

        frame1.pack(fill='both', expand=True)
        frame2.pack(fill='both', expand=True)
        frame3.pack(fill='both', expand=True)

        # add frames to notebook

        notebook.add(frame1, text="Today's Food Log")
        notebook.add(frame2, text="Food Database")
        notebook.add(frame3, text="Nutrition Summary")

        self.log_frame = frame1
        self.database_frame = frame2
        self.summary_frame = frame3
        
        self.load_food_log()
        self.load_food_database()
        self.load_nutrition_summary()
        root.mainloop()

    def load_food_log(self):
        tk.Label(self.log_frame, text="Today's Food Log").pack(pady=6)
        log_frame = tk.Frame(self.log_frame)
        log_frame.pack(fill='both', expand=True, padx=8)
        self.log_list = tk.Listbox(log_frame, width=100, height=16)
        self.log_list.pack(side='left', fill='both', expand=True)

        for food, grams in self.food_log.food_entries:
            nutrition = food.get_nutrition(grams)
            self.log_list.insert(tk.END,
                f"{food.name} — {grams}g - {nutrition['calories']:.1f} kcal - {nutrition['carbs']:.1f}g carbs - {nutrition['protein']:.1f}g protein - {nutrition['fat']:.1f}g fat"
            )
        
        tk.Button(self.log_frame,text="Add Food", command=self.add_food_log).pack(side='left', padx=4,pady=4)
        tk.Button(self.log_frame,text="Save Log", command=self.save_food_log).pack(side='left', padx=4,pady=4)
        tk.Button(self.log_frame,text="Delete Food Item", command=self.delete_log_entry).pack(side='left', padx=4,pady=4)
        tk.Button(self.log_frame,text="Edit Food Item", command=self.edit_food_log).pack(side='left', padx=4,pady=4)


    def load_food_database(self):
        tk.Label(self.database_frame, text="Food Database").pack(pady=6)
        database_frame = tk.Frame(self.database_frame)
        database_frame.pack(fill='both', expand=True, padx=8)
        self.database_list = tk.Listbox(database_frame, width=120, height=16)
        self.database_list.pack(side='left', fill='both', expand=True)

        for food in self.food_db.food_items:
            self.database_list.insert(tk.END,
                f"{food.name} — {food.calories_per_100g} kcal | {food.carbs_per_100g}g carbs | {food.protein_per_100g}g protein | {food.fat_per_100g}g fat"
            )

        tk.Button(self.database_frame,text="Add Food", command=self.add_food_entry).pack(side='left', padx=4,pady=4)
        tk.Button(self.database_frame,text="Save Database", command=self.save_food_database).pack(side='left', padx=4,pady=4)
        tk.Button(self.database_frame,text="Delete Food Item", command=self.delete_food_item).pack(side='left', padx=4,pady=4)
        tk.Button(self.database_frame,text="Edit Food Item", command=self.edit_food_entry).pack(side='left', padx=4,pady=4)

    def load_nutrition_summary(self):
        tk.Label(self.summary_frame, text="Nutrition Summary").pack(pady=6)
        self.summary = tk.Label(self.summary_frame, text="Total Calories: 0\nTotal Carbs: 0g\nTotal Protein: 0g\nTotal Fat: 0g", justify='left')
        self.summary.pack(pady=4)
        if self.food_log.food_entries:
            total_calories = sum(food.get_nutrition(grams)['calories'] for food, grams in self.food_log.food_entries)
            total_carbs = sum(food.get_nutrition(grams)['carbs'] for food, grams in self.food_log.food_entries)
            total_protein = sum(food.get_nutrition(grams)['protein'] for food, grams in self.food_log.food_entries)
            total_fat = sum(food.get_nutrition(grams)['fat'] for food, grams in self.food_log.food_entries)
            self.summary.config(text=f"Total Calories: {total_calories:.1f}\nTotal Carbs: {total_carbs:.1f}g\nTotal Protein: {total_protein:.1f}g\nTotal Fat: {total_fat:.1f}g")

    def add_food_entry(self):
        entry=messagebox.askquestion("Add Food", "Would you like to create a custom entry for the database?")
        if entry == 'yes':
            name = simpledialog.askstring("Food Name", "Enter the name of the food item:")
            calories = float(simpledialog.askstring("Calories per 100g", f"Enter calories per 100g for {name}:"))
            carbs = float(simpledialog.askstring("Carbs per 100g", f"Enter carbs per 100g for {name}:"))
            protein = float(simpledialog.askstring("Protein per 100g", f"Enter protein per 100g for {name}:"))
            fat = float(simpledialog.askstring("Fat per 100g", f"Enter fat per 100g for {name}:"))
            new_food = FoodItem(name, calories, carbs, protein, fat)
            self.food_db.add_food_item(new_food)
            self.database_list.insert(tk.END,
                f"{new_food.name} — {new_food.calories_per_100g} kcal | {new_food.carbs_per_100g}g carbs | {new_food.protein_per_100g}g protein | {new_food.fat_per_100g}g fat"
            )
            

    def save_food_database(self):
        self.food_db.save()
        messagebox.showinfo("Save Database", "Food database saved successfully.")

    def delete_food_item(self):
        try:
            selected_index = self.database_list.curselection()[0]
            self.database_list.delete(selected_index)
            self.food_db.remove_food_item(selected_index)

        except IndexError:
            messagebox.showerror("Error", "Please select a food item to delete.")

    def edit_food_entry(self):
        try:
            selected = self.database_list.curselection()[0]
            food_item = self.food_db.food_items[selected]
            name = simpledialog.askstring("Food Name", "Enter the name of the food item:")
            if name is None:
                messagebox.showerror("Error", "Food name cannot be empty.")
                return
            else:
                calories = float(simpledialog.askstring("Calories per 100g", f"Enter calories per 100g for {name}:"))
                carbs = float(simpledialog.askstring("Carbs per 100g", f"Enter carbs per 100g for {name}:"))
                protein = float(simpledialog.askstring("Protein per 100g", f"Enter protein per 100g for {name}:"))
                fat = float(simpledialog.askstring("Fat per 100g", f"Enter fat per 100g for {name}:"))
                food_item.name = name
                food_item.calories_per_100g = calories
                food_item.carbs_per_100g = carbs
                food_item.protein_per_100g = protein
                food_item.fat_per_100g = fat
                self.database_list.delete(selected)
                self.database_list.insert(selected,
                    f"{food_item.name} — {food_item.calories_per_100g} kcal | {food_item.carbs_per_100g}g carbs | {food_item.protein_per_100g}g protein | {food_item.fat_per_100g}g fat"
                )
        except IndexError:
            messagebox.showerror("Error", "Please select a food item to edit.")


    def add_food_log(self, food_item:FoodItem=None, grams:float=None):
        if food_item is None or grams is None:
            entry=messagebox.askquestion("Add Food", "Would you like to add a custom food item to the foodlog?")
            if entry == 'yes':
                items='\n'.join([f"{i}. {food.name}" for i, food in enumerate(self.food_db.food_items)])
                food_entry_name=simpledialog.askstring("Food Item", f"Select a food item from the database:\n{items}")
                try:
                    selected_index = int(food_entry_name.split('.')[0])
                    food_entry_name = self.food_db.food_items[selected_index].name
                    grams = float(simpledialog.askstring("Grams", f"How many grams of {food_entry_name} did you eat?"))
                    if grams <= 0:
                        messagebox.showerror("Error", "Grams must be a positive number.")
                        return
                    self.log_list.insert(tk.END, f"{food_entry_name} — {grams}g - {self.food_db.food_items[selected_index].get_nutrition(grams)['calories']} kcal - {self.food_db.food_items[selected_index].get_nutrition(grams)['carbs']}g carbs - {self.food_db.food_items[selected_index].get_nutrition(grams)['protein']}g protein - {self.food_db.food_items[selected_index].get_nutrition(grams)['fat']}g fat")
                    self.food_log.add_entry(self.food_db.food_items[selected_index], grams)
                except (IndexError, ValueError):
                    messagebox.showerror("Error", "Invalid food item selection or grams input.")
            else:
                messagebox.showerror("Error", "Custom food entry not implemented yet.")
        else:
            self.food_log.add_entry(food_item, grams)
            self.food_log.save()
        

    def save_food_log(self):
        self.food_log.save()
        messagebox.showinfo("Save Log", "Food log saved successfully.")

    def delete_log_entry(self):
        try:
            selected_index = self.log_list.curselection()[0]
            self.log_list.delete(selected_index)
            self.food_log.remove_entry(selected_index)

        except IndexError:
            messagebox.showerror("Error", "Please select a food entry to delete.")

    def edit_food_log(self):
        try:
            selected_index = self.log_list.curselection()[0]
            food_item, grams = self.food_log.food_entries[selected_index]
            new_grams = float(simpledialog.askstring("Edit Grams", f"Enter new grams for {food_item.name} (current: {grams}g):"))
            if new_grams <= 0:
                messagebox.showerror("Error", "Grams must be a positive number.")
                return
            self.food_log.food_entries[selected_index] = (food_item, new_grams)
            nutrition = food_item.get_nutrition(new_grams)
            self.log_list.delete(selected_index)
            self.log_list.insert(selected_index, f"{food_item.name} — {new_grams}g - {nutrition['calories']} kcal - {nutrition['carbs']}g carbs - {nutrition['protein']}g protein - {nutrition['fat']}g fat")
            self.food_log.save()
        except IndexError:
            messagebox.showerror("Error", "Please select a food entry to edit.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for grams.")

class Foodlog:
    def __init__(self, filename):
        self.filename = filename
        self.food_entries = []
        self.load()

    def load(self):
        self.food_entries = []

        if os.path.exists(self.filename):
            print("Found file:", self.filename)

            with open(self.filename, 'r') as f:
                data = json.load(f)

            self.food_entries = [
                (FoodItem(**entry['food_item']), entry['grams'])
                for entry in data
            ]
        
    def display_log(self, log_list:tk.Listbox):
        log_list.delete(0, tk.END)
        for food_item, grams in self.food_entries:
            nutrition = food_item.get_nutrition(grams)
            log_list.insert(tk.END, f"{food_item.name} — {grams}g - {nutrition['calories']} kcal - {nutrition['carbs']}g carbs - {nutrition['protein']}g protein - {nutrition['fat']}g fat")

    def add_entry(self, food_item:FoodItem, grams:float):
        self.food_entries.append((food_item, grams))

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump([{'food_item': food.to_dict(), 'grams': grams} for food, grams in self.food_entries], f, indent=2)    

    def remove_entry(self, log_list_index: int):
        if 0 <= log_list_index < len(self.food_entries):
            del self.food_entries[log_list_index]
            self.save()
        else:
            raise IndexError("Food item index out of range.")  
        
          

if __name__ == "__main__":
    app = NutritionTrackerApp()

    