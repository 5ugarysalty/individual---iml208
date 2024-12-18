import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime, timedelta

# CSV file name
csv_file = "ferry_tickets.csv"

# Initialize tickets list
tickets = []

# Load tickets from CSV
def load_tickets():
    global tickets
    try:
        with open(csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            tickets = [row for row in reader]
    except FileNotFoundError:
        tickets = []

# Save tickets to CSV
def save_tickets():
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "name", "email", "phone", "dob", "membership_type", "start_date", "expiration_date", "route"
        ])
        writer.writeheader()
        writer.writerows(tickets)

# Refresh ticket list display
def refresh_list():
    ticket_list.delete(0, tk.END)
    for i, ticket in enumerate(tickets):
        ticket_list.insert(tk.END, 
            f"{i+1}. {ticket['name']} | {ticket['route']} | {ticket['membership_type']} | Exp: {ticket['expiration_date']}")

# Add a new ticket
def add_ticket():
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    dob = entry_dob.get()
    membership_type = combo_membership.get()
    start_date = datetime.now().strftime("%Y-%m-%d")
    expiration_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    route = combo_route.get()
    
    if not name or not email or not phone or not dob or not membership_type or not route:
        messagebox.showwarning("Invalid Input", "Please fill all fields.")
        return

    tickets.append({
        "name": name,
        "email": email,
        "phone": phone,
        "dob": dob,
        "membership_type": membership_type,
        "start_date": start_date,
        "expiration_date": expiration_date,
        "route": route
    })
    save_tickets()
    refresh_list()
    clear_fields()
    messagebox.showinfo("Success", "Ticket added successfully.")

# Update selected ticket
def update_ticket():
    try:
        selected_index = ticket_list.curselection()[0]
        tickets[selected_index] = {
            "name": entry_name.get(),
            "email": entry_email.get(),
            "phone": entry_phone.get(),
            "dob": entry_dob.get(),
            "membership_type": combo_membership.get(),
            "start_date": tickets[selected_index]["start_date"],
            "expiration_date": tickets[selected_index]["expiration_date"],
            "route": combo_route.get()
        }
        save_tickets()
        refresh_list()
        clear_fields()
        messagebox.showinfo("Success", "Ticket updated successfully.")
    except IndexError:
        messagebox.showwarning("Error", "Please select a ticket to update.")

# Delete selected ticket
def delete_ticket():
    try:
        selected_index = ticket_list.curselection()[0]
        tickets.pop(selected_index)
        save_tickets()
        refresh_list()
        messagebox.showinfo("Success", "Ticket deleted successfully.")
    except IndexError:
        messagebox.showwarning("Error", "Please select a ticket to delete.")

# Clear input fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_dob.delete(0, tk.END)
    combo_membership.set("")
    combo_route.set("")

# GUI setup
root = tk.Tk()
root.title(" Shinee Ferry Ticket Booking System")
root.geometry("800x500")

# Input Form
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Email:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Date of Birth:").grid(row=3, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Membership Type:").grid(row=4, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Route:").grid(row=5, column=0, padx=5, pady=5)

entry_name = tk.Entry(frame_form)
entry_email = tk.Entry(frame_form)
entry_phone = tk.Entry(frame_form)
entry_dob = tk.Entry(frame_form)

entry_name.grid(row=0, column=1, padx=5, pady=5)
entry_email.grid(row=1, column=1, padx=5, pady=5)
entry_phone.grid(row=2, column=1, padx=5, pady=5)
entry_dob.grid(row=3, column=1, padx=5, pady=5)

combo_membership = ttk.Combobox(frame_form, values=["Regular (RM26.60)", "Student (RM16)", "VIP (RM40.60)"])
combo_membership.grid(row=4, column=1, padx=5, pady=5)

combo_route = ttk.Combobox(frame_form, values=[
    "Langkawi to Kuala Kedah", 
    "Langkawi to Kuala Perlis", 
    "Kuala Kedah to Langkawi", 
    "Kuala Perlis to Langkawi"
])
combo_route.grid(row=5, column=1, padx=5, pady=5)

# Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Add Ticket", command=add_ticket).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Update Ticket", command=update_ticket).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Delete Ticket", command=delete_ticket).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Clear Fields", command=clear_fields).grid(row=0, column=3, padx=5)

# Ticket List
frame_list = tk.Frame(root)
frame_list.pack(pady=10)

ticket_list = tk.Listbox(frame_list, width=100, height=15)
ticket_list.pack()

# Initialize system
load_tickets()
refresh_list()

# Run the application
root.mainloop()
