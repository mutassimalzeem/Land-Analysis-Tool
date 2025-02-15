import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sqlite3
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LandAnalysisTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Land Analysis Tool")
        self.root.geometry("900x700")
        
        # Initialize database
        self.init_database()
        
        # Load data from database
        self.load_data()
        
        # Create UI
        self.create_widgets()
    
    def init_database(self):
        # Create database if it doesn't exist
        self.conn = sqlite3.connect('Day 84/land_data.db')
        self.cursor = self.conn.cursor()
        
        # Create table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS land_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT NOT NULL,
                pollution_level REAL NOT NULL,
                soil_type TEXT NOT NULL
            )
        ''')
        self.conn.commit()
    
    def load_data(self):
        # Load data from database into pandas DataFrame
        query = "SELECT region, pollution_level, soil_type FROM land_data"
        self.data = pd.read_sql_query(query, self.conn)
        
        # If no data exists, create empty DataFrame with correct columns
        if self.data.empty:
            self.data = pd.DataFrame(columns=["Region", "Pollution Level", "Soil Type"])
    
    def save_data(self):
        # Save all data back to database (this is a simple approach - in production, you'd typically just insert new records)
        self.cursor.execute("DELETE FROM land_data")
        for _, row in self.data.iterrows():
            self.cursor.execute(
                "INSERT INTO land_data (region, pollution_level, soil_type) VALUES (?, ?, ?)",
                (row["Region"], row["Pollution Level"], row["Soil Type"])
            )
        self.conn.commit()
    
    def create_widgets(self):
        # Create notebook (tabbed interface)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        input_frame = ttk.Frame(notebook)
        visualization_frame = ttk.Frame(notebook)
        analysis_frame = ttk.Frame(notebook)
        
        notebook.add(input_frame, text="Data Input")
        notebook.add(visualization_frame, text="Visualization")
        notebook.add(analysis_frame, text="Analysis")
        
        # Setup input tab
        self.setup_input_tab(input_frame)
        
        # Setup visualization tab
        self.setup_visualization_tab(visualization_frame)
        
        # Setup analysis tab
        self.setup_analysis_tab(analysis_frame)
        
        # Add export button to input tab
        ttk.Button(input_frame, text="Export to CSV", command=self.export_to_csv).pack(pady=10)
    
    def setup_input_tab(self, parent):
        # Single entry frame
        single_entry_frame = ttk.LabelFrame(parent, text="Add Single Entry")
        single_entry_frame.pack(fill="x", padx=10, pady=10)
        
        # Region entry
        ttk.Label(single_entry_frame, text="Region:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.region_var = tk.StringVar()
        ttk.Entry(single_entry_frame, textvariable=self.region_var).grid(row=0, column=1, padx=5, pady=5)
        
        # Pollution level entry
        ttk.Label(single_entry_frame, text="Pollution Level:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.pollution_var = tk.DoubleVar()
        ttk.Entry(single_entry_frame, textvariable=self.pollution_var).grid(row=1, column=1, padx=5, pady=5)
        
        # Soil type dropdown
        ttk.Label(single_entry_frame, text="Soil Type:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.soil_var = tk.StringVar()
        soil_types = ["Fertile", "Rocky", "Neutral", "Sandy"]
        ttk.Combobox(single_entry_frame, textvariable=self.soil_var, values=soil_types).grid(row=2, column=1, padx=5, pady=5)
        
        # Add button
        ttk.Button(single_entry_frame, text="Add Entry", command=self.add_single_entry).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Batch import frame
        batch_frame = ttk.LabelFrame(parent, text="Batch Import")
        batch_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(batch_frame, text="Import from CSV", command=self.import_from_csv).pack(pady=10)
        ttk.Button(batch_frame, text="Import from Excel", command=self.import_from_excel).pack(pady=10)
        
        # Data view frame
        view_frame = ttk.LabelFrame(parent, text="Current Data")
        view_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview for data display
        self.tree = ttk.Treeview(view_frame, columns=("Region", "Pollution Level", "Soil Type"), show="headings")
        self.tree.heading("Region", text="Region")
        self.tree.heading("Pollution Level", text="Pollution Level")
        self.tree.heading("Soil Type", text="Soil Type")
        self.tree.pack(fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(view_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Populate treeview
        self.update_treeview()
    
    def setup_visualization_tab(self, parent):
        # Create frame for plot
        plot_frame = ttk.Frame(parent)
        plot_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add button to refresh plot
        ttk.Button(plot_frame, text="Refresh Plot", command=self.update_plot).pack(pady=10)
        
        # Create initial plot
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Initial plot
        self.update_plot()
    
    def setup_analysis_tab(self, parent):
        # Controls frame
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        # Add filter options
        ttk.Label(controls_frame, text="Max Pollution Level:").pack(side="left", padx=5)
        self.max_pollution_var = tk.DoubleVar(value=20)
        ttk.Entry(controls_frame, textvariable=self.max_pollution_var, width=5).pack(side="left", padx=5)
        
        ttk.Label(controls_frame, text="Suitable Soil Types:").pack(side="left", padx=5)
        
        # Checkboxes for soil types
        self.soil_selections = {}
        for soil in ["Fertile", "Rocky", "Neutral", "Sandy"]:
            var = tk.BooleanVar(value=(soil in ["Fertile", "Neutral"]))
            self.soil_selections[soil] = var
            ttk.Checkbutton(controls_frame, text=soil, variable=var).pack(side="left", padx=5)
        
        ttk.Button(controls_frame, text="Run Analysis", command=self.run_analysis).pack(side="left", padx=15)
        
        # Results frame
        results_frame = ttk.LabelFrame(parent, text="Analysis Results")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview for results
        self.results_tree = ttk.Treeview(results_frame, columns=("Region", "Pollution Level", "Soil Type"), show="headings")
        self.results_tree.heading("Region", text="Region")
        self.results_tree.heading("Pollution Level", text="Pollution Level")
        self.results_tree.heading("Soil Type", text="Soil Type")
        self.results_tree.pack(fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Run initial analysis
        self.run_analysis()
    
    def add_single_entry(self):
        try:
            region = self.region_var.get()
            pollution = self.pollution_var.get()
            soil = self.soil_var.get()
            
            if not region or not soil:
                messagebox.showerror("Error", "All fields are required")
                return
            
            # Add to DataFrame
            new_data = pd.DataFrame({
                "Region": [region],
                "Pollution Level": [pollution],
                "Soil Type": [soil]
            })
            
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            
            # Save to database
            self.save_data()
            
            # Update treeview
            self.update_treeview()
            
            # Clear entries
            self.region_var.set("")
            self.pollution_var.set(0.0)
            self.soil_var.set("")
            
            messagebox.showinfo("Success", "Entry added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def import_from_csv(self):
        try:
            filename = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV files", "*.csv")]
            )
            
            if not filename:
                return
            
            new_data = pd.read_csv(filename)
            required_columns = ["Region", "Pollution Level", "Soil Type"]
            
            # Check if all required columns exist
            if not all(col in new_data.columns for col in required_columns):
                missing = [col for col in required_columns if col not in new_data.columns]
                messagebox.showerror("Error", f"Missing columns: {', '.join(missing)}")
                return
            
            # Keep only required columns
            new_data = new_data[required_columns]
            
            # Concatenate with existing data
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            
            # Save to database
            self.save_data()
            
            # Update treeview
            self.update_treeview()
            
            messagebox.showinfo("Success", f"Imported {len(new_data)} entries from CSV")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def import_from_excel(self):
        try:
            filename = filedialog.askopenfilename(
                title="Select Excel File",
                filetypes=[("Excel files", "*.xlsx *.xls")]
            )
            
            if not filename:
                return
            
            new_data = pd.read_excel(filename)
            required_columns = ["Region", "Pollution Level", "Soil Type"]
            
            # Check if all required columns exist
            if not all(col in new_data.columns for col in required_columns):
                missing = [col for col in required_columns if col not in new_data.columns]
                messagebox.showerror("Error", f"Missing columns: {', '.join(missing)}")
                return
            
            # Keep only required columns
            new_data = new_data[required_columns]
            
            # Concatenate with existing data
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            
            # Save to database
            self.save_data()
            
            # Update treeview
            self.update_treeview()
            
            messagebox.showinfo("Success", f"Imported {len(new_data)} entries from Excel")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_treeview(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add data to treeview
        for _, row in self.data.iterrows():
            self.tree.insert("", "end", values=(
                row["Region"],
                row["Pollution Level"],
                row["Soil Type"]
            ))
    
    def update_plot(self):
        if self.data.empty:
            messagebox.showinfo("Info", "No data available for plotting")
            return
        
        # Clear previous plot
        self.ax.clear()
        
        # Define colors for soil types
        colors = {"Fertile": 'green', "Rocky": 'brown', "Neutral": 'blue', "Sandy": 'yellow'}
        
        # Get colors for each region based on soil type
        bar_colors = [colors.get(soil, 'gray') for soil in self.data['Soil Type']]
        
        # Create bar plot
        self.ax.bar(self.data["Region"], self.data['Pollution Level'], color=bar_colors)
        
        # Add legend
        handles = [plt.Rectangle((0,0),1,1,color=colors[soil]) for soil in colors if soil in self.data['Soil Type'].unique()]
        self.ax.legend(handles, [soil for soil in colors if soil in self.data['Soil Type'].unique()])
        
        # Add labels and title
        self.ax.set_xlabel("Region")
        self.ax.set_ylabel("Pollution Level")
        self.ax.set_title("Pollution Levels by Region with Soil Types")
        
        # Rotate region names for clarity
        plt.xticks(rotation=45, ha='right')
        
        # Adjust layout
        self.fig.tight_layout()
        
        # Redraw canvas
        self.canvas.draw()
    
    def run_analysis(self):
        if self.data.empty:
            messagebox.showinfo("Info", "No data available for analysis")
            return
        
        # Get selected soil types
        selected_soils = [soil for soil, var in self.soil_selections.items() if var.get()]
        
        # Get max pollution level
        max_pollution = self.max_pollution_var.get()
        
        # Filter data
        suitable_lands = self.data[
            (self.data['Pollution Level'] <max_pollution) & 
            (self.data['Soil Type'].isin(selected_soils))
        ]
        
        # Clear existing items in results tree
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add filtered data to results tree
        for _, row in suitable_lands.iterrows():
            self.results_tree.insert("", "end", values=(
                row["Region"],
                row["Pollution Level"],
                row["Soil Type"]
            ))
        
        # Show summary
        messagebox.showinfo("Analysis Summary", 
                           f"Found {len(suitable_lands)} suitable lands out of {len(self.data)} total regions.")
    
    def export_to_csv(self):
        try:
            filename = filedialog.asksaveasfilename(
                title="Save CSV File",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            
            if not filename:
                return
            
            self.data.to_csv(filename, index=False)
            messagebox.showinfo("Success", f"Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = LandAnalysisTool(root)
    root.mainloop()