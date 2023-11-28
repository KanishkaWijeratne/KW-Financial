import ast
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

# Create the main application window
root = tk.Tk()
root.title("KW Financial")
file_path = 'information_file.txt'
#FILE FUNCTIONS
def file_lines_to_lists(file_path):
    result = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    # Use ast.literal_eval to parse each line as a Python list
                    line_list = ast.literal_eval(line.strip())
                    if isinstance(line_list, list):
                        result.append(line_list)
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing line: {str(e)}")
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    print(result)
    return result

#FILE FUNCTIONS
#FILE FUNCTIONS
#FILE FUNCTIONS
#FILE FUNCTIONS


def file_reader(file_path):
    try:
        with open(file_path, 'r') as file:
            
            file_contents = file.read()
            print(file_contents)
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except IOError:
        print(f"An error occurred while trying to read the file '{file_path}'.")


def file_adder(file, new_data):
    try:
        with open(file, 'a') as file:
            file.write(new_data + '\n')
    except FileNotFoundError:
        print(f"The file '{file}' does not exist.")
    except IOError:
        print(f"An error occurred while trying to append to the file '{file}'.")




# Create variables to store transaction details
full_transaction = []
date = ""
# Create a variable to track if an expense is being added
adding_expense = False
def expense_page(event):
    def expense_checker():
        nonlocal full_transaction  # Use 'nonlocal' to modify the outer 'full_transaction' list
        

        # Validate and append transaction amount
        try:
            transaction_amount = float(entry_amount.get())
            full_transaction.append(transaction_amount)
        except ValueError:
            print("Invalid amount input")
            return

        # Append selected option (transaction type)
        full_transaction.append(option_var.get())

    
        

        # Print the full_transaction list to check
        print("Full Transaction:", full_transaction)
        #add the full transaction to the file
        file_adder(file_path,str(full_transaction))
        file_reader(file_path)
        # Reset the variables for the next transaction
        full_transaction = []  # Reset to an empty list
        entry_amount.delete(0, 'end')  # Clear the entry widget
        option_var.set("")  # Clear the option menu selection
        date_label.config(text="Selected Date: ")  # Clear the selected date label

    global adding_expense  # Use global to modify the outer adding_expense variable
    full_transaction = []
    # Check if an expense is already being added
    if adding_expense:
        print("Cannot add another expense until the previous one is finished.")
        return

    # This is a checker to make sure that it can be submitted
    # A function to check if whatever amount is submitted is valid
    NO_label_check = False

    def get_selected_date():
        def calendar_view():
            def print_sel():
                nonlocal date  # Use 'nonlocal' to modify the outer 'date' variable
                selected_date = cal.get_date()
                date = str(selected_date)
                date_label.config(text=f"Selected Date: {selected_date}")
                print(date)
                full_transaction.append(str(selected_date))
                top.destroy()
            
            top = tk.Toplevel(root)
            cal = Calendar(top, font="Arial 14", selectmode='day', cursor="hand1", year=2023, month=2, day=5)
            cal.pack(fill="both", expand=True)
            tk.Button(top, text="OK", command=print_sel).pack()
        date = ""
        calendar_view()
        

    def validate_float_input():
        nonlocal NO_label_check, transaction_amount
       
        NO_label = tk.Label(root, text="MUST INPUT VALID AMOUNT", font=("Arial", 11))
        try:
            transaction_amount = float(entry_amount.get())
            if transaction_amount > 0:
                print(transaction_amount)
                print("YES")
                date = get_selected_date()
                NO_label_check = False
                expense_button.config(state=tk.NORMAL)  # Enable the "Add Expense" button
            
        except ValueError:
            print("NO")
            if not NO_label_check:
                NO_label.pack()
                NO_label_check = True

    # What transaction type
    transaction_button = tk.Button(root, text="Verify and Submit Transaction", command=expense_checker)
    def option_selected(*args):
        nonlocal transaction_type
        selected_option = option_var.get()
        transaction_type = selected_option
        print(transaction_type)
        
        transaction_button.pack()

        result_label.config(text=f"You selected: {selected_option}")

    # Create variables to store the transaction amount and transaction type
    transaction_amount = ""
    transaction_type = ""

    # Create an Entry widget for float input
    entry_amount = tk.Entry(root)
    entry_amount.pack()

    # Create an OptionMenu widget with the list of options
    option_var = tk.StringVar(root)
    option_var.trace_add("write", option_selected)

    option_menu = tk.OptionMenu(root, option_var, *options)
    option_menu.config(font=("Arial", 12))
    option_menu.pack(pady=10)

    # Create a button to validate the input
    validate_button = tk.Button(root, text="Validate transaction amount and pick date", command=validate_float_input)
    validate_button.pack()

    # Create a label to display the validation result
    result_label = tk.Label(root, text="")

    # Create a label to display the selected date
    date_label = tk.Label(root, text="Selected Date: ")
    date_label.pack() 

    adding_expense = True  # Mark that an expense is being added
    expense_button.config(state=tk.DISABLED)  # Disable the "Add Expense" button


def view_page(event):
    # Retrieve the list of transactions from the file
    list_of_transactions = file_lines_to_lists(file_path)

    # Create a new window to display the transactions
    view_window = tk.Toplevel(root)
    view_window.title("Transaction History")

    # Create a label for selecting the month
    month_label = tk.Label(view_window, text="Select Month:", font=("Arial", 12))
    month_label.pack(pady=10)

    # Create a dropdown menu for selecting the month
    month_var = tk.StringVar(view_window)
    months = ["All"] + [datetime(2000, i, 1).strftime("%B") for i in range(1, 13)]
    month_menu = tk.OptionMenu(view_window, month_var, *months)
    month_menu.config(font=("Arial", 12))
    month_menu.pack()

    # Create a label for selecting the year
    year_label = tk.Label(view_window, text="Select Year:", font=("Arial", 12))
    year_label.pack(pady=10)

    # Create a dropdown menu for selecting the year
    year_var = tk.StringVar(view_window)
    years = ["All"] + [str(year) for year in range(2000, 2031)]
    year_menu = tk.OptionMenu(view_window, year_var, *years)
    year_menu.config(font=("Arial", 12))
    year_menu.pack()

    # Create a label for selecting the transaction type
    transaction_type_label = tk.Label(view_window, text="Select Transaction Type:", font=("Arial", 12))
    transaction_type_label.pack(pady=10)

    # Create a dropdown menu for selecting the transaction type
    transaction_type_var = tk.StringVar(view_window)
    transaction_types = ["All"] + options  # Assuming 'options' contains your transaction types
    transaction_type_menu = tk.OptionMenu(view_window, transaction_type_var, *transaction_types)
    transaction_type_menu.config(font=("Arial", 12))
    transaction_type_menu.pack()

    # Create a label to display the total amount
    total_amount_label = tk.Label(view_window, text="Total Amount: 0", font=("Arial", 12))
    total_amount_label.pack(pady=10)

    # Function to filter transactions by month, year, and transaction type
    def filter_transactions():
        selected_month = month_var.get()
        selected_year = year_var.get()
        selected_transaction_type = transaction_type_var.get()
        text_widget.configure(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)  # Clear existing content

        total_amount = 0  # Variable to store the total amount

        for transaction in list_of_transactions:
            date_str = transaction[0]  # Assuming date is the first element in the transaction list
            date = datetime.strptime(date_str, "%m/%d/%y")
            month_str = date.strftime("%B")  # Get the full month name
            year_str = str(date.year)
            transaction_type = transaction[1]  # Assuming transaction type is the second element in the transaction list

            if (selected_month == "All" or selected_month == month_str) and \
                    (selected_year == "All" or selected_year == year_str) and \
                    (selected_transaction_type == "All" or selected_transaction_type == transaction_type):
                # Only display transactions for the selected month, year, and transaction type or all months, years, and transaction types
                text_widget.insert(tk.END, f"Transaction Amount: ${str(transaction[1])}     Date:{date}\n")
                total_amount += transaction[1]

        text_widget.configure(state=tk.DISABLED)

        # Update the total amount label with rounding to two decimals
        total_amount_label.config(text=f"Total Amount: {round(total_amount, 2)}")

    # Create a button to apply the month, year, and transaction type filter
    filter_button = tk.Button(view_window, text="Apply Filter", command=filter_transactions)
    filter_button.pack(pady=10)

    # Create a label to display a header
    header_label = tk.Label(view_window, text="Transaction History", font=("Arial", 16))
    header_label.pack(pady=10)

    # Create a text widget to display the transactions
    text_widget = tk.Text(view_window, wrap=tk.WORD, width=50, height=20)
    text_widget.pack()

    # Disable text editing in the text widget
    text_widget.configure(state=tk.DISABLED)

    # Bind the view_page function to the left mouse button click event
    view_button.bind("<Button-1>", view_page)





# Create a label for the title
title_label = tk.Label(root, text="KW Financial", font=("Arial", 20))
options = ["Housing", "Transportation", "Utilities", "Insurance", "Personal Spending", "Medical/Healthcare", "Savings", "Investments", "Recreation", "Miscellaneous"]




# Create buttons for different budgeting actions
income_button = tk.Button(root, text="Add Income")
expense_button = tk.Button(root, text="Add Expense")
view_button = tk.Button(root, text="View Transactions")
exit_button = tk.Button(root, text="Exit", command=root.destroy)

def button_pressed():
    print("Pressed")

# Bind the button_press function to the left mouse button click event
expense_button.bind("<Button-1>", expense_page)
view_button.bind("<Button-1>", view_page)
exit_button.bind("<Button-1>", button_pressed)

# Pack the widgets to arrange them in the window
title_label.pack(pady=20)
expense_button.pack(pady=10)
view_button.pack(pady=10)
exit_button.pack(pady=10)


# Start the tkinter main loop
root.mainloop()

# Now you cannot add another expense until the previous one is finished.
