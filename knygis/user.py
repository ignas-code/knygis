class User:
    def __init__(self,username):
        self.username = username

    def __str__(self):
        return(self.username)

class Reader(User):
    def __init__(self,username,lib_card,books_borrowed):
        super().__init__(username)
        self.lib_card = lib_card
        self.books_borrowed = books_borrowed

    def view_borrowed(self):
        borrowed_books_str = ", ".join(f"{key}: {value}" for key, value in self.books_borrowed.items())
        return borrowed_books_str

    def __str__(self):
        if not self.books_borrowed:
            borrowed_books_str = "nėra"
        else:
            borrowed_books_str = ", ".join(f"{key}: {value}" for key, value in self.books_borrowed.items())
        return f"Vartotojas: {self.username}, Skaitytojo kortelė: {self.lib_card}, Paimtos knygos: {borrowed_books_str}" 
    
    def __repr__(self):
        return ({self.username},{self.lib_card}) #,(self.books_borrowed)

class Librarian(User):
    def __init__(self,username,password):
        super().__init__(username)
        self.password = password

    def __str__(self):
        return f'{self.username}, {self.password}'

if __name__ == "__main__":
    reader1 = Reader("Skaitmantas",12333,{"raktas":"verte"})
    print(reader1)
    print(reader1.lib_card)
    print(reader1.books_borrowed)
    reader1.books_borrowed["key"] = "betkas"
    print(reader1.books_borrowed)