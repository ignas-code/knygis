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

if __name__ == "__main__":
    knyga1 = Book("Svetimas","Alberas Kamiu",1942,"romanas")
    print(knyga1)