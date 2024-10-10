from load_save import save

def book_input():
    print("Įveskite knygos duomenis:")
    name = input("Pavadinimas: ")
    author = input("Autorius: ")
    year = input("Metai: ")
    genre = input("Žanras: ")
    quantity = input("Kiekis: ")
    return name,author,year,genre,quantity

def reader_menu(lib):
    while True:
        choice = input("""
1 - Peržiūrėti knygas
2 - Pasiimti knygą
q - Grįžti\n""")

        match choice:
            case '1': # 1 - Peržiūrėti knygas
                lib.all_books()

            case '2': # 2 - Pasiimti knygą
                print("funkcionalumas dar kuriamas")

            case 'q':
                print("Grįžti")
                break

            case _:
                print("Klaidinga įvestis. Bandykite dar kartą.")

def librarian_menu(lib):
    while True:
        choice = input("""
1 - Pridėti knygą
2 - Pašalinti knygą
3 - Peržiūrėti knygas
4 - Pridėti skaitytoją
5 - Peržiūrėti skaitytojus                       
q - Grįžti\n""")

        match choice:
            case '1': # 1 - Pridėti knygą
                try:
                    name,author,year,genre,quantity = book_input()
                    lib.add_book(name,author,year,genre,int(quantity))
                    save(lib)
                    print("Knyga pridėta")
                except ValueError:
                    print("Klaidinga įvestis")
                except:
                    print("Klaida 1")
                    continue

            case '2': # 2 - Pašalinti knygą
                print("funkcionalumas dar kuriamas")
                # additional checks required
                # book_id = input("Įveskite knygos ID: ")
                # book_id = int(book_id)
                # lib.remove_book(book_id)

            case '3': # 3 - Peržiūrėti knygas
                lib.all_books()

            case '4': # 4 - Pridėti skaitytoją
                username = input("Įveskite norimą skaitytojo vardą: ")
                try:
                    id = lib.add_reader(username)
                    save(lib)
                    print(f'Skaitytojas {username} sukurtas. Skaitytojo kortelės numeris: {id}')
                except:
                    print("Skaitytojo pridėti nepavyko")

            case '5': # 5 - Peržiūrėti skaitytojus
                for value in lib.readers.values():
                    print(value.lib_card, value.username) # value.books_borrowed

            case 'q':
                print("Grįžti")
                break

            case _:
                print("Klaidinga įvestis. Bandykite dar kartą.")


def initial_menu(lib):
    while True:

        choice = input("""
1 - Skaitytojas
2 - Bibliotekininkas
q - Išeiti
Pasirinkite: """)

        match choice:
            case '1': # 1 - Skaitytojas
                print("1")
                reader_menu(lib)
            case '2':
                print("2") # 2 - Bibliotekininkas
                librarian_menu(lib)
            case 'q':
                break
            case _:
                print("\nKlaidinga įvestis. Bandykite dar kartą.")