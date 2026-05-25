import json
import os
import tkinter as tk
from tkinter import messagebox

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
        pass
        

class NutritionTrackerApp:
    def __init__(self, window):
        self.food_db = FoodDatabase("food_database.json")

        self.window = window
        self.window.title("Nutrition Tracker")
        self.window.geometry("800x500")
        self.create_widgets()

    def create_widgets(self):
        nav = tk.Frame(self.window)
        nav.pack(fill='x', pady=8)
        tk.Button(nav, text="Today's Log", width=16)
        tk.Button(nav, text='Food Database', width=16 )
        tk.Button(nav, text='Summary', width=16 )
        tk.Button(nav, text='Exit', width=16)

    def food_log_screen(self):
        tk.Label(self.window, text="Today's Food Log").pack(pady=6)
        
    
    def run(self):
        self.window.mainloop()

class Foodlog:
    def __init__(self, filename):
        self.filename = filename
        self.entries = []
        pass
        

if __name__ == "__main__":
    main_window = NutritionTrackerApp(tk.Tk())
    main_window.run()

    