import tkinter as tk
from tkinter import messagebox
import json

class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __str__(self):
        return f"{self.name} | {self.phone} | {self.email} | {self.address}"

class AddressBook:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.filename, 'r') as f:
                return [Contact(**contact) for contact in json.load(f)]
        except FileNotFoundError:
            return []

    def save_contacts(self):
        with open(self.filename, 'w') as f:
            json.dump([contact.__dict__ for contact in self.contacts], f)

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def update_contact(self, old_name, new_contact):
        for i, contact in enumerate(self.contacts):
            if contact.name == old_name:
                self.contacts[i] = new_contact
                self.save_contacts()
                return True
        return False

    def delete_contact(self, name):
        for i, contact in enumerate(self.contacts):
            if contact.name == name:
                del self.contacts[i]
                self.save_contacts()
                return True
        return False

    def search_contact(self, name):
        return [contact for contact in self.contacts if name.lower() in contact.name.lower()]

class AddressBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Address Book")
        
        self.address_book = AddressBook()

        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        self.phone_label = tk.Label(self.root, text="Phone:")
        self.phone_label.grid(row=1, column=0)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(row=1, column=1)

        self.email_label = tk.Label(self.root, text="Email:")
        self.email_label.grid(row=2, column=0)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=2, column=1)

        self.address_label = tk.Label(self.root, text="Address:")
        self.address_label.grid(row=3, column=0)
        self.address_entry = tk.Entry(self.root)
        self.address_entry.grid(row=3, column=1)

        self.add_button = tk.Button(self.root, text="Add", command=self.add_contact)
        self.add_button.grid(row=4, column=0, columnspan=2)

        self.update_button = tk.Button(self.root, text="Update", command=self.update_contact)
        self.update_button.grid(row=4, column=2)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_contact)
        self.delete_button.grid(row=4, column=3)

        self.contacts_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.contacts_listbox.grid(row=5, column=0, columnspan=4)
        self.contacts_listbox.bind('<<ListboxSelect>>', self.on_select)

        self.load_contacts()

    def load_contacts(self):
        self.contacts_listbox.delete(0, tk.END)
        for contact in self.address_book.contacts:
            self.contacts_listbox.insert(tk.END, contact)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()
        
        if name and phone and email and address:
            contact = Contact(name, phone, email, address)
            self.address_book.add_contact(contact)
            self.load_contacts()
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    def on_select(self, event):
        selected_contact_index = self.contacts_listbox.curselection()
        if selected_contact_index:
            contact = self.address_book.contacts[selected_contact_index[0]]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, contact.name)
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, contact.phone)
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, contact.email)
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, contact.address)

    def update_contact(self):
        selected_contact = self.contacts_listbox.curselection()
        if selected_contact:
            old_name = self.address_book.contacts[selected_contact[0]].name
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            email = self.email_entry.get()
            address = self.address_entry.get()
            if name and phone and email and address:
                contact = Contact(name, phone, email, address)
                if self.address_book.update_contact(old_name, contact):
                    self.load_contacts()
                else:
                    messagebox.showerror("Error", "Contact not found.")
            else:
                messagebox.showerror("Error", "All fields must be filled!")
        else:
            messagebox.showerror("Error", "No contact selected for update.")

    def delete_contact(self):
        selected_contact = self.contacts_listbox.curselection()
        if selected_contact:
            name = self.address_book.contacts[selected_contact[0]].name
            if self.address_book.delete_contact(name):
                self.load_contacts()
        else:
            messagebox.showerror("Error", "No contact selected for deletion.")

    def search_contact(self):
        name = self.name_entry.get()
        results = self.address_book.search_contact(name)
        self.contacts_listbox.delete(0, tk.END)
        for contact in results:
            self.contacts_listbox.insert(tk.END, contact)

if __name__ == "__main__":
    root = tk.Tk()
    app = AddressBookApp(root)
    root.mainloop()