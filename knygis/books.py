# knyga, privalo turėti bent, autorių pavadinimą išleidimo metus ir žanrą
class Book:
    def __init__(self,name,author,year,genre,quantity): #metai str, nes kartais buna metu ruozas
        self.name = name
        self.author = author
        self.year = year
        self.genre = genre
        self.quantity = quantity # total quantity of the book
        self.borrowed_cur = 0 # number of books currently borrowed

    def __str__(self):
        return f'{self.name}, {self.author}, {self.year}m., {self.genre}, viso: {self.quantity}vnt., paimta: {self.borrowed_cur}'
    
    def __eq__(self, other): # __eq__ defines how class instances can be compared
        if isinstance(other, Book): # is it an instance of Book class
            return (self.name == other.name and
                    self.author == other.author and
                    self.year == other.year and
                    self.genre == other.genre)
                    #self.quantity == other.quantity) # do not check for quantity
        return False # if other is not a Book

if __name__ == "__main__":
    knyga1 = Book("Svetimas","Alberas Kamiu",1942,"romanas",12)
    print(knyga1)
    print(knyga1.quantity)
    knyga1.quantity = 55
    print(knyga1.quantity)
    # print(knyga1)