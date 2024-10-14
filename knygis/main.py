import streamlit as st
from load_save import initial_load,save

def main(lib):
    st.title("Biblioteka")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.lib = None
        st.session_state.user = None 

    if not st.session_state.logged_in:
        page_option = st.sidebar.radio("Pasirinkite", ["Skaitytojo puslapis", "Bibliotekininko puslapis"])
        if page_option == "Skaitytojo puslapis":
            lib_card = st.text_input("Įveskite savo skaitytojo kortelės numerį:")
            if st.button("Prisijungti"):
                if lib_card in lib.readers:
                    reader = lib.readers[lib_card]
                    username = reader.username
                    st.session_state.logged_in = True
                    st.session_state.lib_card = lib_card
                    st.session_state.user = 'reader' 
                    st.session_state.username = username
                    st.success(f"Sveiki prisijungę, {username} !")
                    print(f'Sveiki prisijungę, {username} !')
                    st.rerun()
                else:
                    st.error("Klaidinga įvestis. Prašome įvesti skaitytojo kortelės numerį.")
        
        elif page_option == "Bibliotekininko puslapis":
            librarian_username = st.text_input("Įveskite vartotojo vardą:")
            librarian_password = st.text_input("Įveskite vartotojo slaptažodį:", type='password') 
            if st.button("Prisijungti"):
                if librarian_username == lib.librarian.username and librarian_password == lib.librarian.password: 
                    st.session_state.logged_in = True
                    st.session_state.lib_card = None
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
    page = st.sidebar.radio("Pasirinkite:", ["Pagrindinis", "Pridėti knygą", "Pašalinti knygas", "Peržiūrėti knygas", "Pridėti skaitytoją", "Peržiūrėti skaitytojus", "Vėluojančios knygos", "Atsijungti"])

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

    elif page == "Atsijungti":
        show_log_out()

def show_home():
    st.subheader("Pagrindinis")
    username = st.session_state.username
    st.write(f"Sveiki prisijungę, {username} !")
    st.write("Čia yra pradinis mūsų puslapis.")
    st.write("Pasirinkite norimą puslapį šoninėje juostoje.")
    st.write("Ateityje čia taip pat matysite populiariausias knygas.")

def show_add_book():
    st.subheader("Pridėti knygą")
    
    with st.form(key='add_book_form'):
        name = st.text_input("Įveskite knygos pavadinimą:")
        author = st.text_input("Įveskite autorių:")
        year = st.number_input("Įveskite metus:", min_value=0000, max_value=2100, step=1, value=2000)
        genre = st.text_input("Įveskite žanrą:")
        quantity = st.number_input("Įveskite kiekį:", min_value=1, max_value=200, step=1)
    
        submit_button = st.form_submit_button("Pridėti")

        if submit_button:
            if name and author and genre:
                lib.add_book(name,author,year,genre,quantity)
                save(lib)
                st.success(f"Knyga '{name}' pridėta sėkmingai!")
                #st.session_state['last_added_book'] = name 
            else:
                st.error("Įvesti ne visi laukai")

def show_contact_us():
    st.subheader("Kontaktai")

def show_log_out():
    st.subheader("Atsijungti")
    submit_button = st.button("Atsijungti")
    if submit_button:
        st.session_state.logged_in = False
        st.rerun()

def show_all_books():
    st.subheader("Mūsų knygos:")
    books = lib.all_books()
    for book in books:
        st.write(book)

def show_remove_books():
    st.subheader("Pašalinti knygas")
    st.write("Knygos, kurių leidimo data senesnė nei nurodyta, bus pašalintos.")
    criteria = st.number_input("Įveskite metus:", min_value=0000, max_value=2100, step=1, value=1800)

    if 'obsolete_books' not in st.session_state:
        st.session_state.obsolete_books = None
    if 'remove_confirmed' not in st.session_state:
        st.session_state.remove_confirmed = False

    if st.button("Pašalinti"):
        obsolete = lib.view_obsolete_books(criteria)
        st.session_state.obsolete_books = obsolete
        st.session_state.remove_confirmed = False
        print(obsolete)
    
    if st.session_state.obsolete_books:
        st.write("Ar tikrai norite pašalinti šias knygas?")
        for book in st.session_state.obsolete_books:
            st.write(book)

        if st.button("Taip, pašalinti") and not st.session_state.remove_confirmed:
            st.write("Ištrinta")
            lib.remove_obsolete_books(criteria)
            save(lib)
            st.session_state.remove_confirmed = True
    elif st.session_state.obsolete_books is False:
        st.write(f"Knygų, kurių leidimo data senesnė nei nurodyta ({criteria}m.) nerasta")

def show_add_reader():
    st.subheader("Pridėti skaitytoją")
    input_username = st.text_input("Įveskite vartotojo vardą:")
    if st.button("Pridėti"):
        id = lib.add_reader(input_username)
        save(lib)
        st.write(f'Skaitytojas **{input_username}** sukurtas. Skaitytojo kortelės numeris: **{id}**')

def show_all_readers():
    st.subheader("Peržiūrėti skaitytojus")
    all_readers = lib.all_readers()
    if all_readers:
        for reader in all_readers:
            st.write(reader)
    else:
        st.write("Skaitytojų nėra")

def show_late_books():
    st.subheader("Vėluojančios knygos")
    all_overdue, late_readers = lib.get_all_overdue()
    st.write("Vėluojančios knygos:")
    for book in all_overdue:
        st.write(book)
    st.write("Vėluojantys grąžinti skaitytojai:")
    for reader in late_readers:
        st.write(reader)

def show_borrow_book():
    st.subheader("Pasiimti knygą")
    book_id = st.number_input("Įveskite norimos knygos ID:",min_value=0,step=1)
    try:
        book_name = lib.books[book_id].name
        book_author = lib.books[book_id].author
        st.write(f'Knyga: {book_name}, Autorius: {book_author}')
        if st.button("Pasiimti"):
            result = lib.borrow_book(book_id, st.session_state.lib_card)
            st.write(result)
            save(lib)
    except KeyError:
        st.write("Knyga neegzistuoja")
        
def show_borrowed_by_user():
    st.subheader("Paimtos knygos")
    borrowed_books = lib.get_borrowed_by_user(st.session_state.lib_card)
    for item in borrowed_books:
        st.write(item)

def show_return_book():
    st.subheader("Grąžinti knygą")
    
    borrowed_books_dict = lib.get_currently_borrowed_by_user(st.session_state.lib_card) # Returns a list of tuples (book_title, book_id)

    if borrowed_books_dict:
        book_options = [(title, book_id) for book_id, title in borrowed_books_dict.items()]
        selected_book_title, selected_book_id = st.selectbox("Pasirinkite norimą grąžinti knygą:", book_options, format_func=lambda x: x[0])  # Lambda to only display the title
        if st.button("Grąžinti"):
                response = lib.return_book(selected_book_id,st.session_state.lib_card)
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
            for book in results:
                st.write(f'{book}')
            
    elif search_option == "Ieškoti pagal autorių":
        author_name = st.text_input("Įveskite autoriaus vardą:")
        if author_name:
            results = lib.find_books_by_author(author_name)
            for book in results:
                st.write(f'{book}')
            
if __name__ == "__main__":
    lib = initial_load()
    main(lib)