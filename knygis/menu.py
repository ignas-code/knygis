def book_input():
    print("Įveskite knygos duomenis:")
    name = input("Pavadinimas: ")
    author = input("Autorius: ")
    year = input("Metai: ")
    genre = input("Žanras: ")
    quantity = input("Kiekis: ")
    return name,author,year,genre,quantity

def menu(lib):
    while True:
        try:
            pasirinkimas = int(input("""
        1 - Pridėti knygą
        2 - Pašalinti knygą
        3 - Peržiūrėti knygas
        4 - Pasiimti knygą
        5 - Išeiti
        Pasirinkite: """))
        except:
            print("Netinkamas pasirinkimas. Įveskite skaičių 1-5.")
            continue
            
        if pasirinkimas == 1: # 1 - Pridėti knygą
            try:
                name,author,year,genre,quantity = book_input()
                lib.add_book(name,author,year,genre,quantity)
                print("knyga pridėta")

            except:
                print("Klaida 1")
                continue

        if pasirinkimas == 2: # 2 - Pašalinti knygą
            print("funkcionalumas dar kuriamas")
            # additional checks required
            # book_id = input("Įveskite knygos ID: ")
            # book_id = int(book_id)
            # lib.remove_book(book_id)

        if pasirinkimas == 3: # 3 - Peržiūrėti knygas
            lib.all_books()

        if pasirinkimas == 4: # 4 - Pasiimti knygą
            print("funkcionalumas dar kuriamas")

        if pasirinkimas == 5:
            print("Išeita")
            break

if __name__ == "__main__":
    print(book_input())