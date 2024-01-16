"""The purpose of this project is a mock library management system where users are able to check out and return books"""
import json


def load_books():
    """Load the books inventory from a separate file"""
    with open('books_inventory.json', 'r') as book_file:
        return json.load(book_file)


def load_users_info():
    """Load the userIDs from a separate file"""
    with open('users_info.json', 'r') as user_file:
        return json.load(user_file)


def save_users_info(users_info):
    """Update the Users Info after opening an account, checking out a book or returning a book"""
    with open('users_info.json', 'w') as user_file:
        json.dump(users_info, user_file, indent=4)


def save_book_info(books_inventory):
    """Update the Books Inventory after a book has been checked out or returned"""
    with open('books_inventory.json', 'w') as book_file:
        json.dump(books_inventory, book_file, indent=4)


def add_user(users_info):
    """Give the option to create a new account if the UserID isn't recognised"""
    user_id = input("Welcome to the Library. What is your UserID?\n").upper()

    if user_id not in users_info:
        print("UserID doesn't exist")
        new_customer = input("Would you like to add a new account? Y/N\n")
        if new_customer.upper() not in ['Y', 'N']:
            print("Please enter Y or N")
        elif new_customer.upper() == "Y":
            new_user_key = f'LIB{len(users_info) + 1}'
            users_info[new_user_key] = {'borrowed_books': []}
            print(f"Your new UserID is {new_user_key}.")
            save_users_info(users_info)
            return new_user_key  # Return the new user_id

    else:
        print(f"User {user_id} exists.")

    return user_id  # Return the existing user_id


def checkout_book(book, user, users_info, books_inventory):
    """Checkout a book from the library"""
    if book in books_inventory:
        if books_inventory[book]['copies'] > 0:
            books_inventory[book]['copies'] -= 1
            books_inventory[book]['current_borrowers'].append(user)
            users_info[user]['borrowed_books'].append(book)
            save_book_info(books_inventory)
            save_users_info(users_info)
            print(f"{book} checked out successfully")
        else:
            print(
                "Error: The book that you have requested is not currently available.")
    else:
        print("Error: That book is not stocked in this library")


def return_book(book, user, users_info, books_inventory):
    """Return a book to the library"""
    if book in users_info[user]['borrowed_books']:
        books_inventory[book]['copies'] += 1
        books_inventory[book]['current_borrowers'].remove(user)
        users_info[user]['borrowed_books'].remove(book)
        save_book_info(books_inventory)
        save_users_info(users_info)
        print(f"{book} returned successfully")
    else:
        print("You have not borrowed this book.")


def customer_options(user):
    """Provide customers with the options to either check out a book, return a book, or exit the system"""
    while True:
        try:
            choice = int(input("\nWhat would you like to do?\nEnter 1 to checkout a book\nEnter 2 to return a book\n"
                               "Enter 3 to exit\n"))
            if choice == 1:
                if len(users_info[user]['borrowed_books']) < 3:
                    checked_book = input("What book would you like to checkout?\n").capitalize()
                    checkout_book(checked_book, user_id, users_info, books_inventory)
                else:
                    print("Error: You have reached your maximum borrow limit")
            elif choice == 2:
                if len(users_info[user]['borrowed_books']) > 0:
                    print(f"The books that you have on loan are {users_info[user_id]['borrowed_books']}")
                    returned_book = input("What book would you like to return?\n").capitalize()
                    return_book(returned_book, user_id, users_info, books_inventory)
                else:
                    print("Error: You have no books to return.")
            elif choice == 3:
                break
        except ValueError:
            print("Please enter 1, 2, or 3")


users_info = load_users_info()
books_inventory = load_books()
user_id = add_user(users_info)
customer_options(user_id)
