# knyga, privalo turėti bent, autorių pavadinimą išleidimo metus ir žanrą
class Book:
    def __init__(self,name,author,year,genre,quantity): #metai str, nes kartais buna metu ruozas
        self.name = name
        self.author = author
        self.year = year
        self.genre = genre
        self.quantity = quantity

    def __str__(self):
        return f'{self.name}, {self.author}, {self.year}m., {self.genre}, {self.quantity}vnt.'
    
    def __eq__(self, other): # __eq__ defines how class instances can be compared
        if isinstance(other, Book): # is it an instance of Book class
            return (self.name == other.name and
                    self.author == other.author and
                    self.year == other.year and
                    self.genre == other.genre)
                    #self.quantity == other.quantity) # do not check for quantity
        return False # if other is not a Book
    
    def get_quantity(self):
        return self.quantity
    
    def update_quantity(self,new_quantity):
        self.quantity = new_quantity

if __name__ == "__main__":
    knyga1 = Book("Svetimas","Alberas Kamiu",1942,"romanas",12)
    print(knyga1.get_quantity())
    knyga1.update_quantity(24)
    print(knyga1.get_quantity())
    # print(knyga1)