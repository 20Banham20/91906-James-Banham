import json
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

class NutritionTrackerApp:
    def __init__(self):
        self.food_db = FoodDatabase("food_database.json")
        
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
        
        tk.Button(text="Add Food", command=self.add_food_entry).pack(pady=4)

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
    
    def load_nutrition_summary(self):
        tk.Label(self.summary_frame, text="Nutrition Summary").pack(pady=6)
        self.summary = tk.Label(self.summary_frame, text="Total Calories: 0\nTotal Carbs: 0g\nTotal Protein: 0g\nTotal Fat: 0g", justify='left')
        self.summary.pack(pady=4)

    def add_food_entry(self):
        entry=messagebox.askquestion("Add Food", "Would you like to add a food item from the database or create a custom entry?")
        if entry == 'yes':
            try:
                selected_food=self.food_db.food_items[self.database_list.curselection()[0]]
                grams = float(simpledialog.askstring("Grams", f"How many grams of {selected_food.name} did you eat?"))
                self.food_log.add_entry(selected_food, grams)
            except IndexError:
                messagebox.showerror("Error", "Please select a food item from the database.")
        else:
            messagebox.showerror("Error", "Custom food entry not implemented yet.")

class Foodlog:
    def __init__(self, filename):
        self.filename = filename
        self.food_entries = []
    
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.food_entries = json.load(f)
        self.food_entries = []
        for entry in self.food_entries:
            name = entry['food']['name']
            calories_per_100g = entry['food']['calories_per_100g']
            if entry:
                self.food_entries.append({
                    'food': FoodItem(name, calories_per_100g, entry['food']['carbs_per_100g'], entry['food']['protein_per_100g'], entry['food']['fat_per_100g']),
                    'grams': entry['grams']
                })
    
    def add_entry(self, food_item:FoodItem, grams:float):
        self.food_entries.append({
            'food': food_item.to_dict(),
            'grams': grams
        })

        
        

if __name__ == "__main__":
    app = NutritionTrackerApp()

    