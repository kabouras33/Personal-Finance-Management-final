# Εισαγωγή βιβλιοθήκη Tkinter
from tkinter import *
import subprocess

def openExpenses():
   subprocess.run(["python", "expenses.py"])

def openIncome():
   subprocess.run(["python", "income.py"])


# Create the root window
root = Tk()

# Αλλάζω το όνομα του τίτλου
root.title("Διαχείριση προσωπικών οικονομικών οικογένειας V1.0")

# ορίζουμε το window size
root.geometry("800x400+0+0")

# διαμορφώνοντας το χρώμα φόντου σε #FFFAF0
root.config(bg="#FFDEAD")

# Create label - Aλλάζουμε το font και το style
Label(root, text="Διαχείριση προσωπικών οικονομικών οικογένειας",  bg = "#FFDEAD",
        fg = "#000000", font = ("Bahnschrift Condensed", "25")).place(x=120, y=100)
Label(root, text="Ομαδικό Προγραμματιστικό Project 2022-2023",bg = "#FFDEAD",
        fg = "#000000",  font = ("Bahnschrift Condensed", "25")).place(x=140, y=150)
Label(root, text="ΠΛΗΠΡΟ - ID Project: 06",bg = "#FFDEAD",
        fg = "#000000", font = ("Bahnschrift Condensed", "25")).place(x=250, y=200)

# Create the Menu
menubar= Menu(root)
filemenu= Menu(menubar, tearoff=0)

# Συνάρτηση που καλείται αν γίνει η επιλογή
filemenu.add_command(label="Έξοδα οικογένειας", font = ("Bahnschrift Condensed", "14"), command=openExpenses)
filemenu.add_command(label="Έσοδα οικογένειας", font = ("Bahnschrift Condensed", "14"), command=openIncome)
filemenu.add_separator()
filemenu.add_command(label="Έξοδος", font = ("Bahnschrift Condensed", "14"), command=root.quit)
menubar.add_cascade(label="Μενού", menu=filemenu)
root.config(menu=menubar)
#input("Press enter to continue...")
#root.iconbitmap(get_path('client.ico'))
#input("Press enter to continue...")
# Start the event loop
root.mainloop()

