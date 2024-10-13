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
    lib_card = input("Įveskite skaitytojo kortelės numerį: ")
    if lib_card in lib.readers:
        reader = lib.readers[lib_card]
        username = reader.username
        print(f'Sveiki prisijungę, {username} !')
    else:
        print("Klaidinga įvestis")
        return

    while True:
        choice = input("""
1 - Peržiūrėti knygas
2 - Pasiimti knygą
3 - Grąžinti knygą
4 - Ieškoti knygų
5 - Paimtos knygos
q - Grįžti\n""")

        match choice:
            case '1': # 1 - Peržiūrėti knygas
                lib.all_books()

            case '2': # 2 - Pasiimti knygą
                try:
                    book_id = int(input("Įveskite norimos knygos ID: "))
                    try:
                        lib.borrow_book(book_id, lib_card)
                    except:
                        print("Nepavyko paimti knygos")
                    
                except:
                    print("Klaidinga įvestis")
                    return
                save(lib)

            case '3': # 3 - Grąžinti knygą
                print("Paimtos knygos: ")
                reader.view_borrowed()
                try:
                    book_id = int(input("Įveskite norimos knygos ID: "))
                    lib.return_book(book_id,lib_card)
                except:
                    print("Klaidinga įvestis")
                    return
                save(lib)
            
            case '4': # 4 - Ieškoti knygų
                find_by = input("Pasirinkite:\n1. Ieškoti pagal pavadinimą\n2. Ieškoti pagal autorių\nĮveskite: ")
                match find_by:
                    case '1': # 1 - Ieškoti pagal pavadinimą
                        keyword = input("Įveskite ieškomą pavadinimą: ")
                        lib.find_books_by_name(keyword)
                    case '2': # 2 - Ieškoti pagal autorių
                        keyword = input("Įveskite ieškomą autorių: ")
                        lib.find_books_by_author(keyword)
                    case _:
                        print("Klaidinga įvestis. Bandykite dar kartą.")


            case '5': # 4 - Paimtos knygos
                print(reader.view_borrowed())

            case 'q':
                print("Grįžti")
                break

            case _:
                print("Klaidinga įvestis. Bandykite dar kartą.")

def librarian_menu(lib):
    librarian = input("Įveskite bibliotekininko vartotojo vardą: ")
    
    if librarian == lib.librarian.username:
        librarian_pw = input("Įveskite slaptažodį: ")
        if librarian_pw == lib.librarian.password:
            print(f"Sveiki prisijungę, {librarian}!")
        else:
            print("Neteisingai!")
            return
    else:
        print("Neteisingai!")
        return
    
    

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
                lib.all_readers()

            case 'q':
                print("Grįžti")
                break

            case _:
                print("Klaidinga įvestis. Bandykite dar kartą.")

def initial_menu(lib):
    while True:
        print("\nPasirinkite vartotoją: ")

        choice = input("""
1 - Skaitytojas
2 - Bibliotekininkas
q - Išeiti
Pasirinkite: """)

        match choice:
            case '1': # 1 - Skaitytojas
                reader_menu(lib)
            case '2': # 2 - Bibliotekininkas
                librarian_menu(lib)
            case 'q':
                break
            case _:
                print("\nKlaidinga įvestis. Bandykite dar kartą.")