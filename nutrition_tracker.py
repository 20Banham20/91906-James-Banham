import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Tuple


class FoodItem:
    """Represents a food item with its
    nutritional information per 100 grams.
    Each food item contains calories, carbs,
    protein, and fat values that are used
    to calculate nutrition information
    for any quantity."""
    def __init__(
        self,
        name: str,
        calories_per_100g: float,
        carbs_per_100g: float,
        protein_per_100g: float,
        fat_per_100g: float,
    ):
        """
        Initialize a FoodItem with nutritional
        values per 100 grams. Validates that
        all inputs are valid and raises
        appropriate errors.
        """
        # Validate that the food name is a non-empty string
        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                "Food name must be a non-empty string."
            )

        # Validate that all nutritional values
        # are numbers and non-negative
        for value, label in [
            (calories_per_100g, "calories"),
            (carbs_per_100g, "carbs"),
            (protein_per_100g, "protein"),
            (fat_per_100g, "fat"),
        ]:
            if not isinstance(value, (int, float)):
                raise TypeError(f"{label} must be a number.")
            # Ensure no nutritional values are negative
            if value < 0:
                raise ValueError(
                    f"{label} must not be negative."
                )

        # Store the cleaned name and nutritional values as floats
        self.name = name.strip()
        self.calories_per_100g = float(calories_per_100g)
        self.carbs_per_100g = float(carbs_per_100g)
        self.protein_per_100g = float(protein_per_100g)
        self.fat_per_100g = float(fat_per_100g)

    @classmethod
    def from_dict(cls, data):
        """
        Create a FoodItem instance from a
        dictionary of nutritional data. Used
        when loading food items from JSON
        files.
        """
        # Validate that the input data is in dictionary format
        if not isinstance(data, dict):
            raise TypeError(
                "Food item data must be a dictionary."
            )

        return cls(
            name=data.get('name', ''),
            calories_per_100g=data.get('calories_per_100g', 0),
            carbs_per_100g=data.get('carbs_per_100g', 0),
            protein_per_100g=data.get('protein_per_100g', 0),
            fat_per_100g=data.get('fat_per_100g', 0),
        )

    def get_nutrition(self, grams: float):
        """
        Calculate the nutritional information
        for a given quantity in grams.
        Returns a dictionary with calories,
        carbs, protein, and fat for the
        specified amount.
        """
        # Calculate the scaling factor based on
        # the grams provided (divided by 100g base)
        factor = grams / 100
        # Scale all nutritional values by the factor
        # and return as a dictionary
        return {
            'calories': self.calories_per_100g * factor,
            'carbs': self.carbs_per_100g * factor,
            'protein': self.protein_per_100g * factor,
            'fat': self.fat_per_100g * factor
        }
    
    def to_json(self):
        """
        Convert the FoodItem to a JSON string representation.
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Convert the FoodItem to a dictionary
        representation. Used for saving to
        JSON files or other serialization
        needs.
        """
        return {
            'name': self.name,
            'calories_per_100g': self.calories_per_100g,
            'carbs_per_100g': self.carbs_per_100g,
            'protein_per_100g': self.protein_per_100g,
            'fat_per_100g': self.fat_per_100g
        }
    
class FoodDatabase:
    """
    Manages the collection of food items stored in a JSON database.
    Handles loading, saving, adding, and removing food items.
    """
    
    def __init__(self, filename):
        """
        Initialize the FoodDatabase with a
        default set of food items and load
        from file.
        """
        self.filename = filename
        # Initialize with default food items:
        # Chicken Breast and White Rice
        self.food_items = [
            FoodItem("Chicken Breast", 165, 0, 31, 3.6),
            FoodItem("White Rice", 130, 28, 2.7, 0.3),
        ]
        self.load()

    def load(self):
        """Load food items from the
        database file if it exists."""
        # Check if the database file exists
        # and read its contents
        if os.path.exists(self.filename):
            with (
                open(
                    self.filename,
                    "r",
                    encoding="utf-8",
                )
                as f
            ):
                data = json.load(f)
            # Convert each dictionary entry
            # into a FoodItem object
            self.food_items = [
                FoodItem(**item) for item in data
            ]

    def add_food_item(self, food_item: FoodItem):
        """Add a new food item to the in-memory database."""
        # Append the new food item to the list
        self.food_items.append(food_item)

    def save(self):
        """
        Save all food items to the database file
        in JSON format.
        """
        # Write all food items as dictionaries
        # to JSON file with nice formatting
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(
                [food.to_dict() for food in self.food_items],
                f,
                indent=2,
            )

    def remove_food_item(self, database: int):
        """
        Remove a food item from the database
        by its index.
        """
        # Check if the index is valid
        # before removing
        if 0 <= database < len(self.food_items):
            del self.food_items[database]
            # Save changes immediately
            # after deletion
            self.save()
        else:
            raise IndexError(
                "Food item index out of range."
            )

class NutritionTrackerApp:
    """
    Main GUI application for the nutrition tracker.
    Manages the user interface with three tabs: food log, database, 
    and summary.
    """

    def __init__(self):
        """
        Initialize the application with database
        and log instances, then build the GUI.
        """
        # Initialize the food database
        # and food log instances
        self.food_db = FoodDatabase("food_database.json")
        self.food_log = Foodlog("food_log.json")
        
        # Create the main window
        # and set its properties
        root = tk.Tk()
        root.geometry('800x580')
        root.title('Nutrition Tracker')

        # Create a notebook widget
        # (tabbed interface) for multiple views
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        # Create three frames
        # for the three main tabs
        frame1 = ttk.Frame(notebook, width=800, height=580)
        frame2 = ttk.Frame(notebook, width=800, height=580)
        frame3 = ttk.Frame(notebook, width=800, height=580)

        # Pack the frames
        # to make them visible
        frame1.pack(fill='both', expand=True)
        frame2.pack(fill='both', expand=True)
        frame3.pack(fill='both', expand=True)

        # Add the frames to the notebook as tabs
        notebook.add(frame1, text="Today's Food Log")
        notebook.add(frame2, text="Food Database")
        notebook.add(frame3, text="Nutrition Summary")

        # Store references to each frame
        # for later use
        self.log_frame = frame1
        self.database_frame = frame2
        self.summary_frame = frame3
        
        # Build each tab's content
        self.load_food_log()
        self.load_food_database()
        self.load_nutrition_summary()
        # Start the GUI event loop
        root.mainloop()

    def load_food_log(self):
        """Build the food log tab and populate it with current 
        entries."""
        # Add a title label to the food log tab
        tk.Label(self.log_frame, text="Today's Food Log").pack(pady=6)
        # Create a frame to hold the listbox
        log_frame = tk.Frame(self.log_frame)
        log_frame.pack(fill='both', expand=True, padx=8)
        # Create a listbox to display food entries
        self.log_list = tk.Listbox(log_frame, width=100, height=16)
        self.log_list.pack(side='left', fill='both', expand=True)

        # Populate the listbox with current
        # food log entries
        for food, grams in (
            self.food_log.food_entries
        ):
            # Get nutrition info and display
            # formatted entry
            nutrition = food.get_nutrition(grams)
            entry_text = (
                f"{food.name} — {grams}g - "
                f"{nutrition['calories']:.1f} kcal - "
                f"{nutrition['carbs']:.1f}g carbs - "
                f"{nutrition['protein']:.1f}g protein - "
                f"{nutrition['fat']:.1f}g fat"
            )
            self.log_list.insert(tk.END, entry_text)
        
        # Add buttons for food log management
        btn_add = tk.Button(
            self.log_frame,
            text="Add Food",
            command=self.add_food_log,
        )
        btn_add.pack(side='left', padx=4, pady=4)
        btn_save = tk.Button(
            self.log_frame,
            text="Save Log",
            command=self.save_food_log,
        )
        btn_save.pack(side='left', padx=4, pady=4)
        btn_delete = tk.Button(
            self.log_frame,
            text="Delete Food Item",
            command=self.delete_log_entry,
        )
        btn_delete.pack(side='left', padx=4, pady=4)
        btn_edit = tk.Button(
            self.log_frame,
            text="Edit Food Item",
            command=self.edit_food_log,
        )
        btn_edit.pack(side='left', padx=4, pady=4)

    def load_food_database(self):
        """Build the food database tab and display
        stored food items."""
        # Add a title label to the database tab
        tk.Label(
            self.database_frame,
            text="Food Database",
        ).pack(pady=6)
        # Create a frame to hold the listbox
        database_frame = tk.Frame(self.database_frame)
        database_frame.pack(fill='both', expand=True, padx=8)
        # Create a listbox to display
        # all available food items
        self.database_list = tk.Listbox(
            database_frame,
            width=120,
            height=16,
        )
        self.database_list.pack(
            side='left',
            fill='both',
            expand=True,
        )

        # Populate the listbox with all food
        # items from the database
        for food in self.food_db.food_items:
            # Display food item with its
            # nutritional information
            nutrition_str = (
                f"{food.name} — {food.calories_per_100g} kcal | "
                f"{food.carbs_per_100g}g carbs | "
                f"{food.protein_per_100g}g protein | "
                f"{food.fat_per_100g}g fat"
            )
            self.database_list.insert(tk.END, nutrition_str)

        # Add buttons for database management
        btn_add = tk.Button(
            self.database_frame,
            text="Add Food",
            command=self.add_food_entry,
        )
        btn_add.pack(side='left', padx=4, pady=4)
        btn_save = tk.Button(
            self.database_frame,
            text="Save Database",
            command=self.save_food_database,
        )
        btn_save.pack(side='left', padx=4, pady=4)
        btn_delete = tk.Button(
            self.database_frame,
            text="Delete Food Item",
            command=self.delete_food_item,
        )
        btn_delete.pack(side='left', padx=4, pady=4)
        btn_edit = tk.Button(
            self.database_frame,
            text="Edit Food Item",
            command=self.edit_food_entry,
        )
        btn_edit.pack(side='left', padx=4, pady=4)

    def load_nutrition_summary(self):
        """Build the nutrition summary tab and
        show totals from the food log."""
        # Add a title label to the summary tab
        tk.Label(
            self.summary_frame,
            text="Nutrition Summary",
        ).pack(pady=6)
        # Create a label to display
        # nutrition totals
        self.summary = tk.Label(
            self.summary_frame,
            text=(
                "Total Calories: 0\nTotal Carbs: 0g\n"
                "Total Protein: 0g\nTotal Fat: 0g"
            ),
            justify='left',
        )
        self.summary.pack(pady=4)
        # Calculate and display nutrition totals
        # if there are entries
        if self.food_log.food_entries:
            # Sum up all nutritional values
            # from food entries
            total_calories = sum(
                food.get_nutrition(grams)['calories']
                for food, grams in self.food_log.food_entries
            )
            total_carbs = sum(
                food.get_nutrition(grams)['carbs']
                for food, grams in self.food_log.food_entries
            )
            total_protein = sum(
                food.get_nutrition(grams)['protein']
                for food, grams in self.food_log.food_entries
            )
            total_fat = sum(
                food.get_nutrition(grams)['fat']
                for food, grams in self.food_log.food_entries
            )
            # Update the label
            # with calculated totals
            self.summary.config(
                text=(
                    f"Total Calories: {total_calories:.1f}\n"
                    f"Total Carbs: {total_carbs:.1f}g\n"
                    f"Total Protein: {total_protein:.1f}g\n"
                    f"Total Fat: {total_fat:.1f}g"
                )
            )
        
        # Add a button to refresh the summary
        tk.Button(
            self.summary_frame,
            text="Refresh Summary",
            command=self.refresh_nutrition_summary,
        ).pack(pady=4)

    def add_food_entry(self):
        """
        Prompt the user to create and add a new
        food item to the database. Collects
        nutritional information from the user.
        """
        # Ask user for confirmation before
        # proceeding with new entry
        if not messagebox.askyesno(
            "Add Food",
            "Create a custom entry for the database?",
        ):
            return

        # Prompt user for food name
        name = self.ask_non_empty_string(
            "Food Name",
            "Enter the name of the food item:",
        )
        if name is None:
            return

        # Prompt user for calorie content
        calories = self.ask_positive_float(
            "Calories per 100g",
            f"Enter calories per 100g for {name}:",
        )
        if calories is None:
            return

        # Prompt user for carb content
        carbs = self.ask_positive_float(
            "Carbs per 100g",
            f"Enter carbs per 100g for {name}:",
        )
        if carbs is None:
            return

        # Prompt user for protein content
        protein = self.ask_positive_float(
            "Protein per 100g",
            f"Enter protein per 100g for {name}:",
        )
        if protein is None:
            return

        # Prompt user for fat content
        fat = self.ask_positive_float(
            "Fat per 100g",
            f"Enter fat per 100g for {name}:",
        )
        if fat is None:
            return

        # Try to create a new FoodItem
        # with the provided data
        try:
            new_food = FoodItem(
                name,
                calories,
                carbs,
                protein,
                fat,
            )
        except (TypeError, ValueError) as exc:
            messagebox.showerror("Error", str(exc))
            return

        # Add the new food item to database
        self.food_db.add_food_item(new_food)
        # Add the new food item to
        # the display listbox
        nutrition_str = (
            f"{new_food.name} — "
            f"{new_food.calories_per_100g} kcal | "
            f"{new_food.carbs_per_100g}g carbs | "
            f"{new_food.protein_per_100g}g protein | "
            f"{new_food.fat_per_100g}g fat"
        )
        self.database_list.insert(tk.END, nutrition_str)

    def save_food_database(self):
        """
        Save the current food database to file.
        """
        # Save the database and show
        # confirmation message
        if self.food_db.save():
            messagebox.showinfo(
                "Save Database",
                "Food database saved successfully.",
            )

    def delete_food_item(self):
        """Remove the currently selected food
        item from the database."""
        # Try to get the selected item
        # and delete it
        try:
            selected_index = (
                self.database_list.curselection()[0]
            )
            # Remove from display and database
            self.database_list.delete(selected_index)
            self.food_db.remove_food_item(
                selected_index
            )

        except IndexError:
            messagebox.showerror(
                "Error",
                "Please select a food item to delete.",
            )

    def edit_food_entry(self):
        """Edit the currently selected food
        item in the database."""
        # Try to get the selected food item
        # for editing
        try:
            selected = (
                self.database_list.curselection()[0]
            )
        except IndexError:
            messagebox.showerror(
                "Error",
                "Please select a food item to edit.",
            )
            return

        # Get the food item to edit
        food_item = self.food_db.food_items[selected]
        # Prompt user for updated food name
        name = self.ask_non_empty_string(
            "Food Name",
            "Enter the name of the food item:",
        )
        if name is None:
            return

        # Prompt user for updated calorie content
        calories = self.ask_positive_float(
            "Calories per 100g",
            f"Enter calories per 100g for {name}:",
        )
        if calories is None:
            return

        # Prompt user for updated carb content
        carbs = self.ask_positive_float(
            "Carbs per 100g",
            f"Enter carbs per 100g for {name}:",
        )
        if carbs is None:
            return

        # Prompt user for updated protein content
        protein = self.ask_positive_float(
            "Protein per 100g",
            f"Enter protein per 100g for {name}:",
        )
        if protein is None:
            return

        # Prompt user for updated fat content
        fat = self.ask_positive_float(
            "Fat per 100g",
            f"Enter fat per 100g for {name}:",
        )
        if fat is None:
            return

        # Try to create updated FoodItem
        # with new values
        try:
            updated_food = FoodItem(
                name,
                calories,
                carbs,
                protein,
                fat,
            )
        except (TypeError, ValueError) as exc:
            messagebox.showerror("Error", str(exc))
            return

        # Replace the old food item
        # with the updated one
        self.food_db.food_items[selected] = updated_food
        # Update the display to reflect changes
        self.database_list.delete(selected)
        nutrition_str = (
            f"{updated_food.name} — "
            f"{updated_food.calories_per_100g} kcal | "
            f"{updated_food.carbs_per_100g}g carbs | "
            f"{updated_food.protein_per_100g}g protein | "
            f"{updated_food.fat_per_100g}g fat"
        )
        self.database_list.insert(selected, nutrition_str)

    def add_food_log(
        self,
        food_item: FoodItem = None,
        grams: float = None,
    ):
        """Add a food entry to the daily log.
        Either from the database or by direct data."""
        # If food item and grams are not provided,
        # prompt user to select from database
        if food_item is None or grams is None:
            # Check if database has any
            # items available
            if not self.food_db.food_items:
                messagebox.showerror(
                    "Error",
                    "No food items are available",
                )
                return

            # Confirm user wants to add from database
            if not messagebox.askyesno(
                "Add Food",
                (
                    "Would you like to add a food item "
                    "from the database to the food log?"
                ),
            ):
                return

            # Display list of available food items
            # for user selection
            items = '\n'.join(
                [
                    f"{i}. {food.name}"
                    for i, food in enumerate(
                        self.food_db.food_items,
                        start=1,
                    )
                ]
            )
            selection = self.ask_positive_int(
                "Food Item",
                f"Select a food item:\n{items}",
            )
            if selection is None:
                return

            # Validate the selected item number
            if (
                selection < 1 or
                selection > len(self.food_db.food_items)
            ):
                messagebox.showerror(
                    "Error",
                    "Please select a valid food item.",
                )
                return

            # Get the selected food item
            # and ask for quantity
            selected_index = selection - 1
            food_item = (
                self.food_db.food_items[selected_index]
            )
            grams = self.ask_positive_float(
                "Grams",
                (
                    f"How many grams of "
                    f"{food_item.name} did you eat?"
                ),
            )
            if grams is None:
                return

            # Display the entry and add to log
            nutrition = food_item.get_nutrition(grams)
            nutrition_str = (
                f"{food_item.name} — {grams}g - "
                f"{nutrition['calories']:.1f} kcal - "
                f"{nutrition['carbs']:.1f}g carbs - "
                f"{nutrition['protein']:.1f}g protein - "
                f"{nutrition['fat']:.1f}g fat"
            )
            self.log_list.insert(tk.END, nutrition_str)
            self.food_log.add_entry(food_item, grams)
            # Update nutrition summary
            # after adding entry
            self.refresh_nutrition_summary()
            return

        # Add entry directly if food item
        # and grams are provided
        self.food_log.add_entry(food_item, grams)
        self.food_log.save()

    def save_food_log(self):
        """
        Save the current food log entries to file.
        """
        # Save the log and show
        # confirmation message
        if self.food_log.save():
            messagebox.showinfo(
                "Save Log",
                "Food log saved successfully.",
            )

    def delete_log_entry(self):
        """Delete the selected entry from the
        food log and update totals."""
        # Try to delete the selected entry
        # and update summary
        try:
            selected_index = (
                self.log_list.curselection()[0]
            )
            # Remove from display and food log
            self.log_list.delete(selected_index)
            self.food_log.remove_entry(selected_index)
            # Recalculate and display
            # updated totals
            self.refresh_nutrition_summary()
        except IndexError:
            messagebox.showerror(
                "Error",
                "Please select a food entry to delete.",
            )

    def edit_food_log(self):
        """Allow the user to update the grams
        for a selected food log entry."""
        # Try to get selected entry for editing
        try:
            selected_index = (
                self.log_list.curselection()[0]
            )
        except IndexError:
            messagebox.showerror(
                "Error",
                "Please select a food entry to edit.",
            )
            return

        # Get the food item and current grams
        food_item, grams = (
            self.food_log.food_entries[selected_index]
        )
        # Ask user for new quantity
        new_grams = self.ask_positive_float(
            "Edit Grams",
            (
                f"Enter new grams for {food_item.name} "
                f"(current: {grams}g):"
            ),
        )
        if new_grams is None:
            return

        # Update the entry with
        # new grams value
        self.food_log.food_entries[
            selected_index
        ] = (food_item, new_grams)
        # Calculate new nutrition values
        nutrition = (
            food_item.get_nutrition(new_grams)
        )
        # Update the display
        self.log_list.delete(selected_index)
        nutrition_str = (
            f"{food_item.name} — {new_grams}g - "
            f"{nutrition['calories']:.1f} kcal - "
            f"{nutrition['carbs']:.1f}g carbs - "
            f"{nutrition['protein']:.1f}g protein - "
            f"{nutrition['fat']:.1f}g fat"
        )
        self.log_list.insert(selected_index, nutrition_str)
        # Save changes and update summary
        self.food_log.save()
        self.refresh_nutrition_summary()

    def refresh_nutrition_summary(self):
        """Recalculate and display the total
        nutrition summary for the food log."""
        # Check if there are any entries
        # to calculate
        if self.food_log.food_entries:
            # Sum all nutritional values
            # from current entries
            total_calories = sum(
                food.get_nutrition(grams)
                ["calories"]
                for food, grams in (
                    self.food_log.food_entries
                )
            )
            total_carbs = sum(
                food.get_nutrition(grams)["carbs"]
                for food, grams in (
                    self.food_log.food_entries
                )
            )
            total_protein = sum(
                food.get_nutrition(grams)
                ["protein"]
                for food, grams in (
                    self.food_log.food_entries
                )
            )
            total_fat = sum(
                food.get_nutrition(grams)["fat"]
                for food, grams in (
                    self.food_log.food_entries
                )
            )
            # Update the summary label with
            # calculated totals
            summary_text = (
                f"Total Calories: "
                f"{total_calories:.1f}\n"
                f"Total Carbs: {total_carbs:.1f}g\n"
                f"Total Protein: "
                f"{total_protein:.1f}g\n"
                f"Total Fat: {total_fat:.1f}g"
            )
            self.summary.config(text=summary_text)
        else:
            # Display zeros if no entries exist
            self.summary.config(
                text=(
                    "Total Calories: 0\n"
                    "Total Carbs: 0g\n"
                    "Total Protein: 0g\n"
                    "Total Fat: 0g"
                )
            )

    def float_validation(self, value):
        """Validate that a string can be
        converted to a positive float."""
        # Return False if value is None
        if value is None:
            return False

        try:
            # Try to convert the value to a float
            value = float(value)

            # Check that the value is positive
            # and within acceptable range
            if value <= 0:  # Reject zero and
                # negative values
                return False
            if value > 10000:  # Reject
                # unreasonably large values
                return False

            return True
        except ValueError:
            # Return False if conversion
            # to float fails
            return False

    def int_validation(self, value):
        """Validate that a string can be
        converted to a positive integer."""
        # Return False if value is None
        if value is None:
            return False

        try:
            # Try to convert the value to
            # an integer
            value = int(value)

            # Check that the value is positive
            # and within acceptable range
            if value <= 0:  # Reject zero and
                # negative values
                return False
            if value > 10000:  # Reject
                # unreasonably large values
                return False

            return True

        except ValueError:
            # Return False if conversion
            # to integer fails
            return False
        
    def non_empty_validation(
        self, value_if_allowed
    ):
        """Validate that a string entry
        is not empty."""
        try:
            # Check if the string is empty
            # after stripping whitespace
            if value_if_allowed.strip() == "":
                return False
            return True
        except ValueError:
            # Return False if any error
            # occurs during validation
            return False

    def ask_non_empty_string(self, title, prompt):
        """Prompt the user until they enter
        a non-empty string or cancel."""
        # Loop until valid input is
        # received or user cancels
        while True:
            value = simpledialog.askstring(
                title, prompt
            )
            # Return None if user clicks Cancel
            if value is None:
                return None
            # Check if the input is valid
            # (non-empty)
            if (
                self.non_empty_validation(value)
            ):
                return value.strip()
            # Show error message if
            # input is empty
            messagebox.showerror(
                "Error",
                "This field cannot be empty.",
            )

    def ask_positive_float(
        self, title, prompt, max_value=100000.0
    ):
        """Prompt the user until a positive
        float within range is provided."""
        # Loop until valid input is received
        while True:
            value = simpledialog.askstring(
                title, prompt
            )
            # Return None if user clicks Cancel
            if value is None:
                return None
            try:
                # Try to convert the input
                # to a float
                number = float(value)
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Please enter a valid number.",
                )
                continue
            # Validate that the number is
            # within the acceptable range
            if number <= 0 or number > max_value:
                messagebox.showerror(
                    "Error",
                    (
                        f"Enter a value between 0 "
                        f"and {max_value}."
                    ),
                )
                continue
            return number

    def ask_positive_int(
        self, title, prompt, max_value=10000
    ):
        """Prompt the user until a positive
        integer within range is provided."""
        # Loop until valid input is received
        while True:
            value = simpledialog.askstring(
                title, prompt
            )
            # Return None if user clicks Cancel
            if value is None:
                return None
            try:
                # Try to convert the input
                # to an integer
                number = int(value)
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Please enter a valid whole number.",
                )
                continue
            # Validate that the number is
            # within the acceptable range
            if number <= 0 or number > max_value:
                messagebox.showerror(
                    "Error",
                    (
                        f"Enter a value between 1 "
                        f"and {max_value}."
                    ),
                )
                continue
            return number
        

class Foodlog:
    """
    Manages the daily food log entries stored in a JSON file.
    Tracks food items and quantities consumed throughout the day.
    """
    
    def __init__(self, filename):
        """
        Initialize the Foodlog with a filename and load existing entries.
        """
        self.filename = filename
        # List to store tuples of (FoodItem, grams)
        self.food_entries = []
        self.load()

    def load(self):
        """
        Load food log entries from the JSON file.
        """
        # Clear existing entries
        self.food_entries = []

        # Check if the log file exists and read its contents
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Convert each entry dictionary into a tuple of (FoodItem, 
            # grams)
            self.food_entries = [
                (FoodItem(**entry['food_item']), entry['grams'])
                for entry in data
            ]

    def display_log(self, log_list: tk.Listbox):
        """Populate a Listbox widget with
        formatted food log entries."""
        # Clear the listbox first
        log_list.delete(0, tk.END)
        # Add each food entry to the listbox
        # with formatted nutrition information
        for food_item, grams in (
            self.food_entries
        ):
            nutrition = (
                food_item.get_nutrition(grams)
            )
            entry_text = (
                f"{food_item.name} — {grams}g - "
                f"{nutrition['calories']} kcal - "
                f"{nutrition['carbs']}g carbs - "
                f"{nutrition['protein']}g protein - "
                f"{nutrition['fat']}g fat"
            )
            log_list.insert(tk.END, entry_text)

    def add_entry(
        self, food_item: FoodItem, grams: float
    ):
        """Add a new food entry to the
        daily log."""
        # Append a tuple of (FoodItem, grams)
        # to the entries list
        self.food_entries.append(
            (food_item, grams)
        )

    def save(self):
        """Save all food log entries to a
        JSON file."""
        # Write all food entries as
        # dictionaries to JSON file
        with open(
            self.filename, "w", encoding="utf-8"
        ) as f:
            json.dump(
                [
                    {
                        "food_item": food.to_dict(),
                        "grams": grams,
                    }
                    for food, grams in (
                        self.food_entries
                    )
                ],
                f,
                indent=2,
            )

    def remove_entry(self, log_list_index: int):
        """Remove a food entry from the log
        by its index."""
        # Check if the index is valid
        # before removing
        if (
            0 <= log_list_index
            < len(self.food_entries)
        ):
            del self.food_entries[
                log_list_index
            ]
            # Save changes immediately
            # after deletion
            self.save()
        else:
            raise IndexError(
                "Food item index out of range."
            )


# Entry point: Run the application when this file is executed directly
if __name__ == "__main__":
    app = NutritionTrackerApp()