import streamlit as st
import pandas as pd
from load_save import initial_load,save
from initial_data import initial_readers, initial_books
import settings
from library import Library

def main(lib):
    st.title("Biblioteka")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.lib = None
        st.session_state.user = None 

    if not st.session_state.logged_in:
        page_option = st.sidebar.radio("Pasirinkite", ["Skaitytojo puslapis", "Bibliotekininko puslapis"])
        if page_option == "Skaitytojo puslapis":
            reader_first_name = st.text_input("Įveskite skaitytojo vardą:")
            reader_last_name = st.text_input("Įveskite skaitytojo pavardę:")
            reader_card_number = st.text_input("Įveskite skaitytojo kortelės numerį:")
            if st.button("Prisijungti") or reader_card_number:
                reader_id = lib.get_reader(reader_first_name,reader_last_name,reader_card_number)
                if reader_id:
                    st.session_state.logged_in = True
                    st.session_state.reader_card_number = reader_card_number
                    st.session_state.reader_id = reader_id
                    st.session_state.user = 'reader' 
                    st.session_state.first_name = reader_first_name
                    st.session_state.last_name = reader_last_name
                    st.success(f"Sveiki prisijungę, {reader_first_name} {reader_last_name} !")
                    print(f'Sveiki prisijungę, {reader_first_name} {reader_last_name} !')
                    st.rerun()
                else:
                    st.error("Klaidinga įvestis. Prašome įvesti skaitytojo kortelės numerį.")
        
        elif page_option == "Bibliotekininko puslapis":
            librarian_username = st.text_input("Įveskite vartotojo vardą:")
            librarian_password = st.text_input("Įveskite vartotojo slaptažodį:", type='password') 
            if st.button("Prisijungti") or librarian_password:
                if librarian_username == lib.librarian.username and librarian_password == lib.librarian.password: 
                    st.session_state.logged_in = True
                    st.session_state.reader_card_number = None
                    st.session_state.user = 'librarian'
                    st.session_state.username = librarian_username
                    st.success(f"Sveiki prisijungę, {librarian_username} !")
                    print(f'Sveiki prisijungę, {librarian_username} !')
                    st.rerun()
                else:
                    st.error("Klaidinga įvestis. Prašome įvesti teisingą vartotojo vardą ir slaptažodį.")

    else:
        if st.session_state.user == 'reader':
            reader_navigation(lib)
        elif st.session_state.user == 'librarian':
            librarian_navigation(lib)

def reader_navigation(lib):
    st.sidebar.title("Skaitytojo navigacija")
    page = st.sidebar.radio("Pasirinkite:", ["Pagrindinis", "Peržiūrėti knygas", "Pasiimti knygą", "Grąžinti knygą", "Ieškoti knygų", "Paimtos knygos", "Atsijungti"])

    if page == "Pagrindinis":
        show_home()
    elif page == "Peržiūrėti knygas":
        show_all_books()
    elif page == "Pasiimti knygą":
        show_borrow_book()
    elif page == "Grąžinti knygą":
        show_return_book()
    elif page == "Ieškoti knygų":
        show_find_books()
    elif page == "Paimtos knygos":
        show_borrowed_by_user()
    elif page == "Atsijungti":
        show_log_out()

def librarian_navigation(lib):
    st.sidebar.title("Bibliotekininko navigacija")
    page = st.sidebar.radio("Pasirinkite:", ["Pagrindinis", "Pridėti knygą", "Pašalinti knygas", "Peržiūrėti knygas", "Pridėti skaitytoją", "Peržiūrėti skaitytojus",
                                             "Vėluojančios knygos", "Inicializuoti duomenis","Atsijungti"])

    if page == "Pagrindinis":
        show_home()

    elif page == "Pridėti knygą":
        show_add_book()

    elif page == "Pašalinti knygas":
        show_remove_books()

    elif page == "Peržiūrėti knygas":
        show_all_books()

    elif page == "Pridėti skaitytoją":
        show_add_reader()

    elif page == "Peržiūrėti skaitytojus":
        show_all_readers()

    elif page == "Vėluojančios knygos":
        show_late_books()

    elif page == "Inicializuoti duomenis":
        show_initialize_data()

    elif page == "Atsijungti":
        show_log_out()

def show_home():
    if st.session_state.user == 'reader':
        st.subheader("Pagrindinis")
        first_name = st.session_state.first_name
        last_name = st.session_state.last_name
        st.write(f"Sveiki prisijungę, **{first_name} {last_name}** !")
        st.write("Čia yra pradinis mūsų puslapis.")
        st.write("Pasirinkite norimą puslapį šoninėje juostoje.")
        st.write("Ateityje čia taip pat matysite populiariausias knygas.")
    if st.session_state.user == 'librarian':
        st.subheader("Pagrindinis")
        username = st.session_state.username
        st.write(f"Sveiki prisijungę, **{username}** !")
        st.write("Čia yra pradinis mūsų puslapis.")
        st.write("Pasirinkite norimą puslapį šoninėje juostoje.")
        st.write("Ateityje čia taip pat matysite populiariausias knygas.")

def show_add_book():
    st.subheader("Pridėti knygą")
    char_limit = settings.max_chars
    isbn_char_limit = 13
    st.write("Užpildykite laukelius ir pridėkite norimą knygą. " \
             "Jei tokia knyga jau egzistuoja, **bus papildytas jos kiekis**. "\
             f"Laukelio įvesties ilgis iki {char_limit} simbolių, ISBN iki {isbn_char_limit} simbolių.")


    with st.form(key='add_book_form',clear_on_submit=True):
        title = st.text_input("Įveskite knygos pavadinimą:", max_chars=char_limit)
        author = st.text_input("Įveskite autorių:",max_chars=char_limit)
        published_year = st.number_input("Įveskite metus:", min_value=0000, max_value=2100, step=1, value=2000)
        genre = st.text_input("Įveskite žanrą:",max_chars=char_limit)
        isbn = st.text_input("Įveskite ISBN:",max_chars=isbn_char_limit,help='10 arba 13 simbolių ISBN kodas')
        total_copies = st.number_input("Įveskite kiekį:",min_value = 1, max_value=200, step=1,help='Nurodžius 0 arba neigiamą kiekį, bus pridėta 1 kynga')
        #quantity = st.slider("Pasirinkite kiekį:", min_value=1, max_value=200, value=10, step=1)
    
        submit_button = st.form_submit_button("Pridėti")


        if submit_button:

            if title and author and genre and isbn:
                result = lib.add_book(title,author,published_year,genre,isbn,total_copies)
                if result == 'Book added successfully':
                    st.success(f"Knyga **{title}** pridėta sėkmingai!")
                elif result == 'Book already exists. Added additional copies.':
                    st.success(f"Knyga **{title}** jau yra bibliotekoje! Papildomai pridėta vienetų: **{total_copies}**.")
                elif result == 'Book already exists. Adding additioanl copies failed.':
                    st.error(f"Knyga **{title}** jau yra bibliotekoje! Pridėti papildomų vienetų nepavyko.")

                #st.session_state['last_added_book'] = name 
            else:
                st.error("Įvesti ne visi laukai")

def show_contact_us():
    st.subheader("Kontaktai")

def show_log_out():
    st.subheader("Atsijungti")
    st.write("Ar tikrai norite atsijungti?")
    submit_button = st.button("Atsijungti")
    if submit_button:
        st.session_state.logged_in = False
        st.rerun()

def show_all_books():
    st.write("Čia galite peržiūrėti visas mūsų bibliotekoje esančias knygas")
    st.subheader("Mūsų knygos:")
    books_data = lib.all_books()
    st.dataframe(books_data, width=800, height=1000, hide_index=True)
    

def show_remove_books():
    st.subheader("Pašalinti knygas")
    st.write("Knygos, kurių leidimo data senesnė nei nurodyta, bus pašalintos.")
    st.write("Atkreipkite dėmesį, jog paimtos knygos nebus pašalintos.")
    criteria = st.number_input("Įveskite metus:", min_value=0000, max_value=2100, step=1, value=1800)

    if 'obsolete_books' not in st.session_state:
        st.session_state.obsolete_books = None
    if 'remove_confirmed' not in st.session_state:
        st.session_state.remove_confirmed = False

    if st.button("Pašalinti"):
        obsolete = lib.view_obsolete_books(criteria)
        st.session_state.obsolete_books = obsolete
        st.session_state.remove_confirmed = False
        print(f'{obsolete}')

    if st.session_state.obsolete_books:
        st.write("Ar tikrai norite pašalinti šias knygas?")
        for book in st.session_state.obsolete_books:
            st.write(f'{book}')

        if st.session_state.remove_confirmed is False:
            if st.button("Taip, pašalinti", type="primary") and not st.session_state.remove_confirmed:
                lib.remove_obsolete_books(criteria)
                save(lib)
                st.session_state.remove_confirmed = True
                st.success("Ištrinta")
    elif st.session_state.obsolete_books is False:
        st.error(f"Knygų, kurių leidimo data senesnė nei nurodyta (**{criteria}**m.) nerasta")

    if st.session_state.remove_confirmed:
        if st.button("Uždaryti"):
            st.session_state.obsolete_books = None
            st.session_state.remove_confirmed = False



    st.subheader("Pašalinti knygą pagal ID:")
    book_id = st.number_input("Įveskite norimos knygos ID:",min_value=0,step=1)
    if book_id is not None and book_id in lib.books:
        try:
            st.write(f"{lib.books[book_id]}")
            if st.button("Pašalinti pagal ID",type="primary", help = "Veiksmas neatšaukiamas"):
                removed_book = lib.remove_book(book_id)
                if removed_book.borrowed_cur >= 1:
                    st.error("Negalima ištrinti! Knyga paimta")
                else:
                    st.success("Knyga pašalinta!")
                    save(lib)
        except KeyError:
            st.error("Knyga neegzistuoja")
    else:
        st.error("Knyga neegzistuoja")


def show_add_reader():
    st.subheader("Pridėti skaitytoją")
    max_chars = settings.max_chars_username
    st.write(f"Sukūrus skaitytoją, skaitytojo kortelės numeris bus sugeneruotas automatiškai. Vartojo vardas neturi viršyti {max_chars} simbolių")
    input_first_name = st.text_input("Įveskite skaitytojo vardą:")
    input_last_name = st.text_input("Įveskite skaitytojo pavardę:")
    if len(input_first_name) >= max_chars:
        st.warning(f"Vardo įvestis apribota iki {max_chars} simbolių.")
        input_first_name = input_first_name[:max_chars]

    if len(input_last_name) >= max_chars:
        st.warning(f"Pavardės įvestis apribota iki {max_chars} simbolių.")
        input_last_name = input_last_name[:max_chars]

    if st.button("Pridėti"):
        id = lib.add_reader(input_first_name,input_last_name)
        st.write(f'Skaitytojas **{input_first_name} {input_last_name}** sukurtas. Skaitytojo kortelės numeris: **{id}**')

def show_all_readers():
    st.subheader("Peržiūrėti skaitytojus")
    st.write("Čia galite matyti visus skaitytojus ir jų skaitytojo kortelės ID")
    all_readers = lib.all_readers()
    df = pd.DataFrame(all_readers, columns=["ID","Skait. kortelė",'Vardas',"Pavardė",'Pridėjimo data'])
    if all_readers:
        st.table(df)
    else:
        st.write("Skaitytojų nėra")

def show_late_books():
    st.subheader("Vėluojančios knygos")

    all_overdue, late_readers = lib.get_all_overdue()
    st.write("**Vėluojančios knygos:**")
    if all_overdue:
        for book in all_overdue:
            try:
                st.write(f'{lib.books[book]}')
            except:
                st.write(f'Knyga ištrinta, bet vartotojo negrąžinta')
    st.write("**Vėluojantys grąžinti skaitytojai:**")
    if late_readers:
        for reader in late_readers:
            st.write(f'Skaitytojo kortelė {reader}, Vartotojo vardas: {lib.readers[reader].username}')

def show_borrow_book():
    st.subheader("Pasiimti knygą")
    book_id = st.number_input("Įveskite norimos knygos ID:",min_value=1,step=1)
    # try:
    book_name,book_author = lib.get_title_author(str(book_id))
    if book_name != False and book_author != False:
        st.write(f'Knyga: **{book_name}**, Autorius: **{book_author}**')
        if st.button("Pasiimti"):
            result = lib.borrow_book(str(book_id), str(st.session_state.reader_id))
            if result == True:
                st.success(f"Knyga **{book_name}** sėkmingai paimta!")
            if result == "Reader has overdue books":
                st.error("Jūs turite vėluojančių knygų!")
            elif result == "No available copies":
                st.error("Nepakankamas knygų likutis!")
            elif result == "Reader already has this book borrowed":
                st.error("Jūs jau turite šią knygą!")
            elif result == "Reader already has maximum number of books borrowed":
                st.error("Jūs jau turite paėmę maksimalų leistiną kiekį knygų!")
    else:
        st.error("Knyga neegzistuoja")
    # except KeyError:
    #     st.error("Knyga neegzistuoja (KeyError)")
        
def show_borrowed_by_user():
    st.subheader("Paimtos knygos")
    st.write("Jūsų paimtos knygos:")
    borrowed_books = lib.get_borrowed_by_user(st.session_state.reader_card_number)
    if borrowed_books:
        for item in borrowed_books:
            st.write(item)
        #st.subheader("Anksčiau paimtos knygos")
        #st.write("Anksčiau jūsų paimtos knygos (grąžintos)")
        #separate currently and previously borrowed books

    else:
        st.error("Šiuo metu neturite paėmę knygų")

def show_return_book():
    st.subheader("Grąžinti knygą")
    
    borrowed_books_dict = lib.get_currently_borrowed_by_user(st.session_state.reader_card_number) # Returns a list of tuples (book_title, book_id)

    if borrowed_books_dict:
        book_options = [(title, book_id) for book_id, title in borrowed_books_dict.items()]
        selected_book_title, selected_book_id = st.selectbox("Pasirinkite norimą grąžinti knygą:", book_options, format_func=lambda x: x[0])  # Lambda to only display the title
        if st.button("Grąžinti"):
                response = lib.return_book(selected_book_id,st.session_state.reader_card_number)
                st.write(response)
                save(lib)
    else:
        st.write("Šiuo metu neturite paėmę knygų")

def show_find_books():
    st.subheader("Ieškoti knygų")
    search_option = st.radio("Pasirinkite paieškos tipą:", ("Ieškoti pagal pavadinimą", "Ieškoti pagal autorių"))

    if search_option == "Ieškoti pagal pavadinimą":
        book_name = st.text_input("Įveskite knygos pavadinimą:")
        if book_name:
            results = lib.find_books_by_name(book_name)
            if isinstance(results, dict):
                for book_id, book in results.items():
                    st.write(f'ID:{book_id}, Knyga: {book.name}, Autorius: {book.author}, Metai: {book.year}, Žanras: {book.genre}')
            else:
                st.write(results)
            
    elif search_option == "Ieškoti pagal autorių":
        author_name = st.text_input("Įveskite autoriaus vardą:")
        if author_name:
            results = lib.find_books_by_author(author_name)
            if isinstance(results, dict):
                for book_id, book in results.items():
                    st.write(f'ID:{book_id}, Knyga: {book.name}, Autorius: {book.author}, Metai: {book.year}, Žanras: {book.genre}')
            else:
                st.write(results)

def show_initialize_data():
    st.subheader("Inicializuoti duomenis")
    st.write("Sukelkite iš anksto numatytus duomenis (knygas ir vartotojus)")
    if lib.initialized_data == False:
        if st.button("Inicializuoti"):
            first_reader = lib.add_reader("Ignas Ti")
            for reader in initial_readers:
                lib.add_reader(reader)
            names = initial_books[0]   
            authors = initial_books[1]
            years = initial_books[2] 
            genres = initial_books[3]
            quantities = initial_books[4]
            for i in range(len(names)):
                lib.add_book(names[i], authors[i], years[i], genres[i], quantities[i])  
            lib.borrow_late_book(0,first_reader)
            st.write("Duomenys inicializuoti")
            lib.initialized_data = True
            save(lib)
    else:
        st.write("Duomenys jau inicializuoti")
            
if __name__ == "__main__":
    lib = Library()
    main(lib)
