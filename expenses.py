# εισαγωγή των απαιτούμενων μονάδων 
from tkinter import *                   # εισαγωγή όλων των ενοτήτων και των κλάσεων από το tkinter  
from tkinter import ttk as ttk          # εισαγωγή της μονάδας ttk από το tkinter  
from tkinter import messagebox as mb    # εισαγωγή της μονάδας μηνυμάτων από το tkinter  
import datetime                         # εισαγωγή της ενότητας ημερομηνίας  
import sqlite3                          # εισαγωγή της ενότητας sqlite3  
from tkcalendar import DateEntry        # εισαγωγή της κλάσης DateEntry από τη λειτουργική μονάδα tkcalendar

# To Pandas DataFrame είναι μια δισδιάστατη δομή δεδομένων με στήλες
import pandas as pd


# 1η Μέθοδος για να εμφανίσω όλα τα έξοδα
def listAllExpenses():  
    ''' Αυτή η Μέθοδος θα ανακτήσει τα δεδομένα
    από τη βάση δεδομένων και θα τα εισαγάγει στον πίνακα δεδομένων tkinter '''
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές  
    global dbconnector, data_table  
    # καθαρίζοντας τον πίνακα
    data_table.delete(*data_table.get_children())  
    # εκτέλεση της εντολής SQL SELECT για την ανάκτηση των δεδομένων από τον πίνακα της βάσης δεδομένων  
    all_data = dbconnector.execute('SELECT * FROM Expense')
  
    # πέρνω τα δεδομένα από τον query
    data = all_data.fetchall()  
      
    # εισάγω τις τιμές στον πίνακα δεδομένων data_table
    for val in data:  
        data_table.insert('', END, values = val)  
  
# 2η Μέθοδος για την προβολή εξόδου
def viewExpenseInfo():  
    '''Αυτή η Μέθοδος θα εμφανίσει τις πληροφορίες του εξόδου στα πεδία εισαγωγής'''
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές   
    global data_table  
    global dateField, payee, description, amount, modeOfPayment  
  
    # επιστρέψτε ένα πλαίσιο μηνύματος που εμφανίζει σφάλμα εάν δεν έχει επιλεγεί καμία σειρά από τον πίνακα  
    if not data_table.selection():  
        mb.showerror('Δεν επιλέχθηκε καμία δαπάνη', 'Επιλέξτε μια δαπάνη από τον πίνακα για να δείτε τα στοιχεία της')  
  
    # συλλογή των δεδομένων από την επιλεγμένη σειρά σε μορφή λεξικού  
    currentSelectedExpense = data_table.item(data_table.focus())  
  
    # ορίζοντας μια μεταβλητή για την αποθήκευση των τιμών από τα δεδομένα που συλλέγονται στη λίστα  
    val = currentSelectedExpense['values']  
  
    # ανάκτηση της ημερομηνίας των δαπανών από τον κατάλογο 
    expenditureDate = datetime.date(int(val[1][:4]), int(val[1][5:7]), int(val[1][8:]))  
  
    # ορίζοντας τα αναφερόμενα δεδομένα στα αντίστοιχα πεδία εισαγωγής τους 
    dateField.set_date(expenditureDate) ; payee.set(val[2]) ; description.set(val[3]) ; amount.set(val[4]) ; modeOfPayment.set(val[5])  
  
# 3η Μέθοδος για να διαγράψω τις καταχωρήσεις από τα πεδία εισαγωγής
def clearFields():  
    ''' Αυτή η Μέθοδος θα διαγράψει όλες τις καταχωρήσεις από τα πεδία εισαγωγής'''
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές  
    global description, payee, amount, modeOfPayment, dateField, data_table  
  
    # ορίζοντας μια μεταβλητή για την αποθήκευση της σημερινής ημερομηνίας  
    todayDate = datetime.datetime.now().date()  
  
    # επαναφέροντας τις τιμές στα πεδία εισαγωγής στο αρχικό  
    description.set('') ; payee.set('') ; amount.set(0.0) , dateField.set_date(todayDate)
    # αφαιρώντας το καθορισμένο στοιχείο από την επιλογή  
    data_table.selection_remove(*data_table.selection())  
  
# 4η Μέθοδος για να διαγράψω την επιλεγμένη εγγραφή
def removeExpense():  
    '''Αυτή η Μέθοδος θα διαγράψει την επιλεγμένη εγγραφή από την βάση δεδομένων'''
  
    # επιστρέφοντας το πλαίσιο μηνύματος που εμφανίζει σφάλμα εάν δεν έχει επιλεγεί καμία σειρά  
    if not data_table.selection():  
        mb.showerror('Δεν έχει επιλεγεί εγγραφή!', 'Παρακαλώ επιλέξτε μια εγγραφή για διαγραφή!')  
        return  
  
    # συλλογή των δεδομένων από την επιλεγμένη σειρά σε μορφή λεξικού  
    currentSelectedExpense = data_table.item(data_table.focus())  
  
    # ορίζοντας μια μεταβλητή για την αποθήκευση των τιμών από τα δεδομένα που συλλέγονται στη λίστα  
    valuesSelected = currentSelectedExpense['values']  
  
    # εμφανίζοντας ένα πλαίσιο μηνύματος που ζητά επιβεβαίωση  
    confirmation = mb.askyesno('Είστε σίγουροι;', f'Είστε βέβαιοι ότι θέλετε να διαγράψετε την εγγραφή του {valuesSelected[2]}')  
  
    # εάν ο χρήστης πει ΝΑΙ, εκτελώντας την εντολή SQL DELETE FROM
    if confirmation:  
        dbconnector.execute('DELETE FROM Expense WHERE ID=%d' % valuesSelected[0])
        dbconnector.commit()  
  
        # καλώντας τη συνάρτηση listAllExpenses().  
        listAllExpenses()  
  
        # επιστρέφοντας το πλαίσιο μηνύματος που εμφανίζει τις πληροφορίες  
        mb.showinfo('Η εγγραφή διαγράφηκε με επιτυχία!', 'Η εγγραφή που θέλατε να διαγράψετε έχει διαγραφεί με επιτυχία')  
  
# 5η Μέθοδος για να διαγράψω όλες τις καταχωρήσεις
def removeAllExpenses():  
    '''Αυτή η Μέθοδος θα διαγράψει όλες τις καταχωρήσεις από την βάση δεδομένων'''
      
    # εμφανίζοντας ένα πλαίσιο μηνύματος που ζητά επιβεβαίωση  
    confirmation = mb.askyesno('Είστε σίγουροι;', 'Είστε βέβαιοι ότι θέλετε να διαγράψετε όλα τα στοιχεία εξόδων από τη βάση δεδομένων;', icon='warning')  
  
    # εάν ο χρήστης πει ΝΑΙ, διαγράφοντας τις εγγραφές από τον πίνακα και εκτελώντας την εντολή SQL DELETE FROM για να διαγράψετε όλες τις καταχωρήσεις  
    if confirmation:  
        data_table.delete(*data_table.get_children())  
  
        dbconnector.execute('DELETE FROM Expense')
        dbconnector.commit()  
  
        # καλώντας τη συνάρτηση clearFields().   
        clearFields()  
  
        # καλώντας τη συνάρτηση listAllExpenses().  
        listAllExpenses()  
  
        # επιστρέφοντας το πλαίσιο μηνύματος που εμφανίζει τις πληροφορίες  
        mb.showinfo('Όλα τα έξοδα διαγράφηκαν», «Όλα τα έξοδα διαγράφηκαν επιτυχώς')  
    else:  
        # επιστρέφοντας το πλαίσιο μηνύματος, εάν η λειτουργία ματαιωθεί  
        mb.showinfo('Εντάξει τότε», «Η εργασία ματαιώθηκε και καμία δαπάνη δεν διαγράφηκε!')  
  
# 6η Μέθοδος για να προσθέσω ένα έξοδο
def addAnotherExpense():  
    '''''Αυτή η Μέθοδος θα προσθέσει ένα έξοδο στην βάση δεδομένων'''
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές 
    global dateField, payee, description, amount, modeOfPayment  
    global dbconnector  
      
    # Εάν κάποιο από τα πεδία είναι κενό, επιστρέψτε το πλαίσιο μηνύματος που εμφανίζει σφάλμα  
    if not dateField.get() or not payee.get() or not description.get() or not amount.get() or not modeOfPayment.get():  
        mb.showerror('Τα πεδία είναι άδεια!', "Παρακαλώ συμπληρώστε όλα τα πεδία που λείπουν πριν πατήσετε το κουμπί προσθήκης!")  
    else:  
        # εκτέλεση της εντολής SQL INSERT INTO  
        dbconnector.execute(  
            'INSERT INTO Expense (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',
            (dateField.get_date(), payee.get(), description.get(), amount.get(), modeOfPayment.get())  
        )  
        dbconnector.commit()  
  
        # καλώντας τη συνάρτηση clearFields().  
        clearFields()  
  
        # καλώντας τη συνάρτηση listAllExpenses().  
        listAllExpenses()  
  
        # επιστρέφοντας το πλαίσιο μηνύματος που εμφανίζει πληροφορίες  
        mb.showinfo('Έξοδα προστέθηκαν», «Η δαπάνη της οποίας τα στοιχεία μόλις εισαγάγατε προστέθηκε στη βάση δεδομένων')  
  
# 7η Μέθοδος για την επεξεργασία σε ένα έξοδο
def editExpense():  
    '''''Αυτή η Μέθοδος θα επιτρέψει στον χρήστη να επεξεργαστεί ένα έξοδο'''
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές  
    global data_table  
  

    '''''Αυτή η συνάρτηση θα ενημερώσει τις λεπτομέρειες της επιλεγμένης δαπάνης στη βάση δεδομένων και στον πίνακα'''
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές
    global dateField, amount, description, payee, modeOfPayment
    global dbconnector, data_table
          
    # συλλογή των δεδομένων από την επιλεγμένη σειρά σε μορφή λεξικού
    currentSelectedExpense = data_table.item(data_table.focus())
          
    # ορίζοντας μια μεταβλητή για την αποθήκευση των τιμών από τα δεδομένα που συλλέγονται στη λίστα
    content = currentSelectedExpense['values']
          
    # εκτέλεση της εντολής SQL UPDATE για ενημέρωση της εγγραφής στον πίνακα της βάσης δεδομένων
    dbconnector.execute(
        'UPDATE Expense SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
        (dateField.get_date(), payee.get(), description.get(), amount.get(), modeOfPayment.get(), content[0])
    )
    dbconnector.commit()

    # καλώντας τη συνάρτηση clearFields().
    clearFields()
  
    # καλώντας τη συνάρτηση listAllExpenses().
    listAllExpenses()
          
    # επιστρέφοντας ένα πλαίσιο μηνύματος που εμφανίζει το μήνυμα
    mb.showinfo('Επεξεργάστηκαν δεδομένα', 'Ενημερώσαμε τα δεδομένα και αποθηκεύσαμε στη βάση δεδομένων όπως θέλετε')


# 8η Μέθοδος για να φέρνω τις κατηγορίες στο πρόγραμμα
def getCategory():
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές
    global dbconnector, category, modeField, my_list, modeOfPayment

    # εκτέλεση της εντολής SQL SELECT για την ανάκτηση των δεδομένων από τον πίνακα της βάσης δεδομένων
    all_data = dbconnector.execute('SELECT nameCat FROM ExpenseCategories')
    row = all_data.fetchone()
    dbconnector.commit()

    if row != None:
        all_data = dbconnector.execute('SELECT nameCat FROM ExpenseCategories')
        dbconnector.commit()

        # πέρνω τα δεδομένα από τον query
        my_list = [r for r, in all_data]  # Δημιουργεί μία λίστα
        modeOfPayment = StringVar(value=my_list[0])
        modeField = OptionMenu(
            frameL2,
            modeOfPayment,
            *my_list
        )
        modeField.config(
            width=15,
            font=("consolas", "10"),
            relief=GROOVE,
            bg="#FFFFFF"
        )

        # χρησιμοποιώντας τη μέθοδο grid() για να ορίσετε τη θέση των παραπάνω γραφικών στοιχείων στη μορφή πλέγματος
        modeField.grid(row=4, column=1, sticky=W, padx=10, pady=10)


# 9η Μέθοδος για να διαγράφω κατηγορία
def deleteCategory():
    '''''Αυτή η συνάρτηση θα αφαιρέσει την Category'''
    global dbconnector, modeOfPayment, category

    # επιστρέφοντας το πλαίσιο μηνύματος που εμφανίζει σφάλμα εάν δεν έχει επιλεγεί καμία σειρά
    if not  category.get():
        mb.showerror('Δεν έχει επιλεγεί Κατηγορία!', 'Παρακαλώ επιλέξτε μια Κατηγορία για διαγραφή!')
        return

    value = category.get()

    # εμφανίζοντας ένα πλαίσιο μηνύματος που ζητά επιβεβαίωση
    confirmation = mb.askyesno('Είστε σίγουροι;',
                               f'Είστε βέβαιοι ότι θέλετε να διαγράψετε την εγγραφή του {value}')

    # εάν ο χρήστης πει ΝΑΙ, εκτελώντας την εντολή SQL DELETE FROM
    if confirmation:
        dbconnector.execute("DELETE FROM ExpenseCategories WHERE nameCat='%s'" % value)
        dbconnector.commit()

        # επιστρέφοντας το πλαίσιο μηνύματος που εμφανίζει τις πληροφορίες
        mb.showinfo('Διαγραφή Κατηγορίας',
                    'Η Κατηγορία έχει διαγραφεί με επιτυχία')

        # Εμφάνιση κατηγοριών
        getCategory()


# 10η Μέθοδος για επιλογή κατηγορίας
def selectCategory():
    '''Αυτή η Μέθοδος θα εμφανίσει τις πληροφορίες της κατηγορίας'''

    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές
    global dbconnector, modeOfPayment, category
    category.set("")

    # ορίζοντας μια μεταβλητή για την αποθήκευση των τιμών από τα δεδομένα που συλλέγονται στη λίστα
    val = modeOfPayment.get()

    # ορίζοντας τα αναφερόμενα δεδομένα στα αντίστοιχα πεδία εισαγωγής τους
    category.set(val)



# 11η Μέθοδος για προσθήκη κατηγορίας
def addCategory():
    ''' Αυτή η Μέθοδος θα προσθέσει κατηγορία '''

    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές
    global dbconnector, category, modeField, my_list, modeOfPayment

    all_data = dbconnector.execute("SELECT * FROM ExpenseCategories WHERE nameCat='%s'" % category.get())
    row = all_data.fetchone()

    # Εάν είναι κενή η κατηγορία, εμφανίζει το πλαίσιο μηνύματος σφάλμα
    if not category.get():
        mb.showerror('Τo πεδίο είναι άδειο!',
                     "Παρακαλώ συμπληρώστε μία κατηγορία")
        return
    # Έλεγχος εάν υπάρχει ήδη η κατηγορία
    elif row != None:
        mb.showerror('Προσοχή !!!',
                     "Η κατηγορία υπάρχει ήδη")
    else:
        # εκτέλεση της εντολής SQL INSERT INTO
        dbconnector.execute(
            'INSERT INTO ExpenseCategories (nameCat) VALUES (?)',
            (category.get(),)
        )

        # το πλαίσιο μηνύματος που εμφανίζει πληροφορίες
        mb.showinfo(
            'Επιτυχής Καταχώρηση', 'Η Κατηγορία '+ category.get() +' προστέθηκε στη βάση δεδομένων')

        # Εμφάνιση κατηγοριών
        getCategory()

# 12η Μέθοδος για την προβολή στατιστικών σε Excel
def viewStats():
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές
        global dbconnector, formdateField, todateField

        # εκτέλεση της εντολής SQL SELECT για την ανάκτηση των δεδομένων από τον πίνακα της βάσης δεδομένων
        all_data = dbconnector.execute("SELECT * FROM Expense where Date between ? and ?",(formdateField.get(), todateField.get()))

        # πέρνω τα δεδομένα από τον query
        records = all_data.fetchall()

        # Πέρνουμε τα ονόματα των στηλών του πίνακα
        names =  ['ID', 'Ημερομηνία', 'Αιτιολογία Εξόδου', 'Περιγραφή', 'Ποσό', 'Κατηγορία']

        # Δημιουργούμε ένα DataFrame
        df = pd.DataFrame(records)

        # Αλλάζουμε από το DataFrame τα ονόματα των στηλών
        df.columns = names

        # γράφω το αρχείο excel και βγάζω το index(index=False)
        with pd.ExcelWriter("stats.xlsx") as writer:
            df.to_excel(writer, index=False)

        # ανοίγω δυναμικά το νέο αρχείο excel
        import os
        os.startfile("stats.xlsx")


''' ΤΕΛΟΣ ΜΕΘΟΔΩΝ '''


# κύρια λειτουργία 
if __name__ == "__main__":  
  
    # σύνδεση με τη βάση δεδομένων  
    dbconnector = sqlite3.connect("Database.db")
    dbcursor = dbconnector.cursor()  
  
    # καθορίζοντας τη λειτουργία που θα εκτελείται κάθε φορά που εκτελείται η εφαρμογή  
    dbconnector.execute(  
        'CREATE TABLE IF NOT EXISTS Expense (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)'
    )  
    # εκτελώντας την παραπάνω εντολή  
    dbconnector.commit()

    dbconnector.execute(
        'CREATE TABLE IF NOT EXISTS ExpenseCategories (idCat INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nameCat TEXT)'
    )
    # εκτελώντας την παραπάνω εντολή
    dbconnector.commit()

    # δημιουργώντας το κύριο παράθυρο της εφαρμογής
    # δημιουργώντας ένα στιγμιότυπο της κλάσης Tk().  
    main_win = Tk()  
    # ορίζοντας τον τίτλο της αίτησης  
    main_win.title("Εφαρμογή για την καταγραφή και διαχείριση των προσωπικών οικονομικών μιας οικογένειας ")
    # ρύθμιση του μεγέθους και της θέσης του παραθύρου  
    main_win.geometry("1415x790+0+0")

    # διαμορφώνοντας το χρώμα φόντου σε #FFFAF0  
    main_win.config(bg = "#FFFAF0")  

  
    # προσθήκη πλαισίων στο παράθυρο για παροχή δομής στα άλλα γραφικά στοιχεία  
    frameLeft = Frame(main_win, bg = "#FFF8DC")  
    frameRight = Frame(main_win, bg = "#DEB887")  
    frameL1 = Frame(frameLeft, bg = "#FFF8DC")  
    frameL2 = Frame(frameLeft, bg = "#FFF8DC")  
    frameL3 = Frame(frameLeft, bg = "#FFF8DC")  
    frameR1 = Frame(frameRight, bg = "#DEB887")  
    frameR2 = Frame(frameRight, bg = "#DEB887")  
  
    # χρησιμοποιώντας τη μέθοδο pack() για να ορίσετε τη θέση των παραπάνω πλαισίων  
    frameLeft.pack(side=LEFT, fill = "both")  
    frameRight.pack(side = RIGHT, fill = "both", expand = True)  
    frameL1.pack(fill = "both")  
    frameL2.pack(fill = "both")  
    frameL3.pack(fill = "both")  
    frameR1.pack(fill = "both")  
    frameR2.pack(fill = "both", expand = True)  

  
    # προσθέτοντας την ετικέτα Στοιχεία Εξόδου
    subheadingLabel = Label(  
        frameL1,  
        text = "Στοιχεία Εξόδου",
        font = ("Bahnschrift Condensed", "15"),  
        width = 20,  
        bg = "#F5DEB3",  
        fg = "#000000"  
        )  
  
    # χρησιμοποιώντας τη μέθοδο pack() για να ορίσετε τη θέση των παραπάνω ετικετών
    subheadingLabel.pack(fill = "both")  
  
      
  
    # δημιουργώντας κάποιες ετικέτες για να ζητήσετε από τον χρήστη να εισαγάγει τα απαιτούμενα δεδομένα
    dateLabel = Label(  
        frameL2,  
        text = "Ημερομηνία:",  
        font = ("consolas", "11", "bold"),  
        bg = "#FFF8DC",  
        fg = "#000000"  
        )  
  
      
    descriptionLabel = Label(  
        frameL2,  
        text = "Περιγραφή:",
        font = ("consolas", "11", "bold"),  
        bg = "#FFF8DC",  
        fg = "#000000"  
        )  
  
      
    amountLabel = Label(  
        frameL2,  
        text = "Ποσό:",  
        font = ("consolas", "11", "bold"),  
        bg = "#FFF8DC",  
        fg = "#000000"  
        )  
  
      
    payeeLabel = Label(  
        frameL2,  
        text = "Αιτιολογία Εξόδου:",
        font = ("consolas", "11", "bold"),  
        bg = "#FFF8DC",  
        fg = "#000000"  
        )  
  
     
    modeLabel = Label(  
        frameL2,  
        text = "Κατηγορία:",
        font = ("consolas", "11", "bold"),  
        bg = "#FFF8DC",  
        fg = "#000000"  
        )  
  
    # χρησιμοποιώντας τη μέθοδο grid() για να ορίσετε τη θέση των παραπάνω ετικετών στη μορφή πλέγματος  
    dateLabel.grid(row = 0, column = 0, sticky = W, padx = 10, pady = 4)
    payeeLabel.grid(row=1, column=0, sticky=W, padx=10, pady=4)
    descriptionLabel.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 4)
    amountLabel.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 4)
    modeLabel.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 4)
  
    # δημιουργία της κλάσης StringVar() για την ανάκτηση των δεδομένων στη μορφή συμβολοσειράς από τον χρήστη  
    description = StringVar()  
    payee = StringVar()  

    # δημιουργία της κλάσης DoubleVar() για την ανάκτηση της λεπτομέρειας του ποσού σε διπλό τύπο δεδομένων
    amount = DoubleVar()  
  
    # δημιουργώντας ένα αναπτυσσόμενο ημερολόγιο για να εισάγει ο χρήστης την ημερομηνία  
    dateField = DateEntry(  
        frameL2,  
        date = datetime.datetime.now().date(),  
        font = ("consolas", "11"),  
        relief = GROOVE  , date_pattern="dd/mm/yy"
        )  
  
    # δημιουργία πεδίων εισαγωγής για την εισαγωγή των δεδομένων με ετικέτα
    descriptionField = Entry(  
        frameL2,  
        text = description,  
        width = 20,  
        font = ("consolas", "11"),  
        bg = "#FFFFFF",  
        fg = "#000000",  
        relief = GROOVE  
        )  
  
    # πεδίο για το ποσό
    amountField = Entry(  
        frameL2,  
        text = amount,  
        width = 20,  
        font = ("consolas", "11"),  
        bg = "#FFFFFF",  
        fg = "#000000",
        relief = GROOVE  
        )  
  
    # πεδίο για Αιτιολογία Εξόδου
    payeeField = Entry(  
        frameL2,  
        text = payee,  
        width = 20,  
        font = ("consolas", "11"),  
        bg = "#FFFFFF",  
        fg = "#000000",  
        relief = GROOVE  
        )


    # Εμφάνιση κατηγοριών
    getCategory()
  
    # Η μέθοδο grid() ορίζει τη θέση των παραπάνω γραφικών στοιχείων στη μορφή πλέγματος
    dateField.grid(row = 0, column = 1, sticky = W, padx = 10, pady = 4)
    payeeField.grid(row=1, column=1, sticky=W, padx=10, pady=4)
    descriptionField.grid(row = 2, column = 1, sticky = W, padx = 10, pady = 4)
    amountField.grid(row = 3, column = 1, sticky = W, padx = 10, pady = 4)


  
    # δημιουργία κουμπιών για τον χειρισμό δεδομένων στο αριστερό πάνελ
    insertButton = Button(  
        frameL3,  
        text = "Προσθήκη εξόδου",
        font = ("Bahnschrift Condensed", "13"),  
        width = 30,  
        bg = "#90EE90",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#008000",  
        activeforeground = "#98FB98",  
        command = addAnotherExpense  
        )

    resetButton = Button(  
        frameL3,  
        text = "Επαναφέρετε τα πεδία",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 30,  
        bg = "#90EE90",
        fg = "#000000",
        relief = GROOVE,  
        activebackground = "#008000",
        activeforeground = "#98FB98",
        command = clearFields  
        )

    # ετικέτα categoryLabel
    categoryLabel = Label(
        frameL3,
        text="Κατηγορίες εξόδων",
        font=("Bahnschrift Condensed", "15"),
        width=45,
        bg="#F5DEB3",
        fg="#000000"
    )

    newLabel = Label(
        frameL3,
        text="Νέα Κατηγορία:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )

    category = StringVar()
    newCategory = Entry(
        frameL3,
        text = category,
        width = 20,
        font = ("consolas", "11"),
        bg = "#FFFFFF",
        fg = "#000000",
        relief = GROOVE
        )



    categoryButton = Button(
        frameL3,
        text = "Προσθήκη Κατηγορίας",
        font = ("Bahnschrift Condensed", "13"),
        width = 20,
        bg = "#FF0000",
        fg = "#FFFFFF",
        relief = GROOVE,
        activebackground = "#8B0000",
        activeforeground = "#FFB4B4",
        command = addCategory
        )

    categorySelect = Button(
        frameL3,
        text="Επιλογή Κατηγορίας",
        font=("Bahnschrift Condensed", "13"),
        width=20,
        bg="#FF0000",
        fg="#FFFFFF",
        relief=GROOVE,
        activebackground="#8B0000",
        activeforeground="#FFB4B4",
        command=selectCategory
    )

    categoryDelete = Button(
        frameL3,
        text="Διαγραφή Κατηγορίας",
        font=("Bahnschrift Condensed", "13"),
        width=20,
        bg="#FF0000",
        fg="#FFFFFF",
        relief=GROOVE,
        activebackground="#8B0000",
        activeforeground="#FFB4B4",
        command=deleteCategory
    )


    ''' Στατιστικά εξόδων '''
    # ετικέτα Στατιστικά
    statsLabel = Label(
        frameL3,
        text="Στατιστικά εξόδων",
        font=("Bahnschrift Condensed", "15"),
        width=45,
        bg="#F5DEB3",
        fg="#000000"
    )

    fromLabel = Label(
        frameL3,
        text="Από Ημερομηνία:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )

    formdateField = DateEntry(
        frameL3,
        date=datetime.datetime.now().date(),
        font=("consolas", "11"),
        relief=GROOVE, date_pattern="yyyy-mm-dd"
    )

    toLabel = Label(
        frameL3,
        text="Έως Ημερομηνία:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )

    todateField = DateEntry(
        frameL3,
        date=datetime.datetime.now().date(),
        font=("consolas", "11"),
        relief=GROOVE, date_pattern="yyyy-mm-dd"
    )


    categoryStats = Button(
        frameL3,
        text="Προβολή Στατιστικών Excel",
        font=("Bahnschrift Condensed", "13"),
        width=30,
        bg="#8B4513",
        fg="#FFFAF0",
        relief=GROOVE,
        activebackground="#8B0000",
        activeforeground="#FFB4B4",
        command=viewStats
    )


    # Χρησιμοποιούμε την μέθοδο grid() για να ορίσουμε τη θέση των widgets της κατηγορίας
    insertButton.grid(row = 0, column = 0, sticky = W, padx = 60, pady = 4, columnspan=2)
    resetButton.grid(row = 1, column = 0, sticky = W, padx = 60, pady = 4, columnspan=2)
    categoryLabel.grid(row = 2, column = 0, sticky = W, pady=10, columnspan=2)
    newLabel.grid(row = 3, column = 0, sticky = W, padx = 15, pady = 4)
    newCategory.grid(row = 3, column = 1, sticky = W, padx = 15, pady = 4)
    categoryButton.grid(row = 4, column = 0, sticky = W, padx = 30, pady = 4, columnspan=2)
    categorySelect.grid(row = 4, column = 1, sticky=W, padx=30, pady=4, columnspan=2)
    categoryDelete.grid(row=5, column=0, sticky=W, padx=100, pady=4, columnspan=2)


    # Χρησιμοποιούμε την μέθοδο grid() για να ορίσουμε τη θέση των widgets των στατιστικών
    statsLabel.grid(row=7, column=0, sticky=W, padx=0, pady=10, columnspan=2)
    fromLabel.grid(row = 8, column = 0, sticky = W, padx = 15, pady = 4)
    formdateField.grid(row = 8, column = 1, sticky = W, padx = 15, pady = 4)
    toLabel.grid(row = 9, column = 0, sticky = W, padx = 15, pady = 4)
    todateField.grid(row = 9, column = 1, sticky = W, padx = 15, pady = 4)
    categoryStats.grid(row=10, column=0, sticky=W, padx=60, pady=20, columnspan=2)

    # δημιουργία κουμπιών για τον χειρισμό δεδομένων επάνω πάνελ
    viewButton = Button(
        frameR1,
        text = "Επιλογή Εξόδου",
        font = ("Bahnschrift Condensed", "13"),
        width = 35,
        bg = "#FFDEAD",
        fg = "#000000",
        relief = GROOVE,
        activebackground = "#A0522D",
        activeforeground = "#FFF8DC",
        command = viewExpenseInfo
        )

      
    editButton = Button(
        frameR1,
        text = "Αποθήκευση εξόδου",
        font = ("Bahnschrift Condensed", "13"),
        width = 35,
        bg = "#FFDEAD",
        fg = "#000000",
        relief = GROOVE,
        activebackground = "#A0522D",
        activeforeground = "#FFF8DC",
        command = editExpense
        )
      

    deleteButton = Button(  
        frameR1,  
        text = "Διαγραφή εξόδου",
        font = ("Bahnschrift Condensed", "13"),  
        width = 35,  
        bg = "#FFDEAD",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#A0522D",  
        activeforeground = "#FFF8DC",  
        command = removeExpense  
        )  
      
      
    deleteAllButton = Button(  
        frameR1,  
        text = "Διαγραφή όλων των εξόδων",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 35,  
        bg = "#FFDEAD",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#A0522D",  
        activeforeground = "#FFF8DC",  
        command = removeAllExpenses  
        )  
  
    # Χρησιμοποιούμε την μέθοδο grid() για να ορίσουμε τη θέση των widgets του επάνω πανελ
    viewButton.grid(row = 0, column = 0, sticky = W, padx = 10, pady = 10)
    editButton.grid(row = 0, column = 1, sticky = W, padx = 10, pady = 10)
    deleteButton.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)  
    deleteAllButton.grid(row = 1, column = 1, sticky = W, padx = 10, pady = 10)  
  

    # δημιουργία πίνακα για να εμφανιστούν όλες οι καταχωρήσεις
    data_table = ttk.Treeview(  
        frameR2,  
        selectmode = BROWSE,
        columns = ('ID', 'Ημερομηνία', 'Αιτιολογία Εξόδου', 'Περιγραφή', 'Ποσό', 'Κατηγορία')
        )



    # κάθετη γραμμή κύλισης στον πίνακα
    Yaxis_Scrollbar = Scrollbar(  
        data_table,  
        orient = VERTICAL,  
        command = data_table.yview  
        )  
  
    # Χρησιμοποιούμε την μέθοδο pack() για να ορίσουμε την θέση της γραμμής κύλισης
    Yaxis_Scrollbar.pack(side = RIGHT, fill = Y)  
  
    # διαμόρφωση της γραμμής κύλισης στον πίνακα
    data_table.config(yscrollcommand = Yaxis_Scrollbar.set)
  
    # προσθήκη επικεφαλίδων στον πίνακα
    data_table.heading('ID', text = 'ID', anchor = CENTER)
    data_table.heading('Ημερομηνία', text = 'Ημερομηνία', anchor = CENTER)  
    data_table.heading('Αιτιολογία Εξόδου', text = 'Αιτιολογία Εξόδου', anchor = CENTER)
    data_table.heading('Περιγραφή', text = 'Περιγραφή', anchor = CENTER)  
    data_table.heading('Ποσό', text = 'Ποσό', anchor = CENTER)  
    data_table.heading('Κατηγορία', text = 'Κατηγορία', anchor = CENTER)
  
    # Ορίζω το μήκος στις στήλες του πίνακα
    data_table.column('#0', width = 0, stretch = NO)  
    data_table.column('#1', width = 50, stretch = NO)  
    data_table.column('#2', width = 95, stretch = NO)  
    data_table.column('#3', width = 150, stretch = NO)  
    data_table.column('#4', width = 450, stretch = NO)
    data_table.column('#5', width = 135, stretch = NO)  
    data_table.column('#6', width = 140, stretch = NO)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Bahnschrift Condensed", 13))
    style.configure('Treeview', font=("Bahnschrift Condensed", 13))

    # Χρησιμοποιούμε την μέθοδο place() για να ορίσουμε την θέση του πίνακα
    data_table.place(relx = 0, y = 0, relheight = 1, relwidth = 1)

    #προβολή εξόδων
    listAllExpenses()

    # Χρησιμοποιούμε την μέθοδο mainloop() για την εκτέλεση της εφαρμογής
    main_win.mainloop()  