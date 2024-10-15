from settings import borrow_duration_limit
from datetime import datetime as dt
class User:
    def __init__(self,username):
        self.username = username

    def __str__(self):
        return(self.username)

class Reader(User):
    def __init__(self,username,lib_card,books_borrowed):
        super().__init__(username)
        self.lib_card = lib_card
        self.books_borrowed = books_borrowed # {bookd_id: [borrow_date, return_date]}

    def __str__(self):
        if not self.books_borrowed:
            borrowed_books_str = "nėra"
        else:
            borrowed_books_str = ", ".join(f"{key}: {value}" for key, value in self.books_borrowed.items())
        return f"Vartotojas: {self.username}, Skaitytojo kortelė: {self.lib_card}, Paimtos knygos: {borrowed_books_str}" 
    
    def __repr__(self):
        return ({self.username},{self.lib_card}) #(self.books_borrowed)

    def view_borrowed(self):
        borrowed_books_str = ", ".join(f"{key}: {value}" for key, value in self.books_borrowed.items())
        print(borrowed_books_str)
        return self.books_borrowed

    def get_overdue(self):
        "Returns overdue books as a list, otherwise returns `False`"
        overdue_books = []
        current_date = dt.now().date()#.strftime("%Y-%m-%d")
        overdue_date = ...
        for book_id in self.books_borrowed:
            book = self.books_borrowed[book_id]
            date_taken = book[0]
            date_returned = book[1]
            if not date_returned: # if there is no `date_returned` - book is not returned
                date_taken = dt.strptime(date_taken, "%Y-%m-%d").date()
                difference = (current_date - date_taken).days
                if difference > borrow_duration_limit:
                    #print(f"Knyga negrąžinta laiku! Paėmimo data: {date_taken}, dabartinė data: {current_date}, skirtumas {difference} dienų")
                    overdue_books.append(book_id)
        if overdue_books:
            return overdue_books
        else:
            return False

class Librarian(User):
    def __init__(self,username,password):
        super().__init__(username)
        self.password = password

    def __str__(self):
        return f'{self.username}, {self.password}'

if __name__ == "__main__":
    # for testing purposes only
    reader1 = Reader("Skaitmantas",12333,{"raktas":"verte"})
    print(reader1)
    print(reader1.lib_card)
    print(reader1.books_borrowed)
    reader1.books_borrowed["key"] = "knyga"
    print(reader1.books_borrowed)