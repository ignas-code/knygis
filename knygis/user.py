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
    def __str__(self):
        return f"Vartotojas: {self.username}, Skaitytojo kortelė: {self.lib_card}, Paimtos knygos: {self.books_borrowed}"
    def __repr__(self):
        return ({self.username},{self.lib_card},{self.books_borrowed})

class Librarian(User):
    def __init__(self,username,password):
        super().__init__(username)
        self.password = password

if __name__ == "__main__":
    reader1 = Reader("Skaitmantas",12333,[132,144])
    print(reader1)
    print(reader1.lib_card)
    print(reader1.books_borrowed)