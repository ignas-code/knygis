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
    st.sidebar.title("Navigacija")
    page = st.sidebar.radio("Pasirinkite:", ["Pagrindinis", "Peržiūrėti knygas", "Atsijungti"])

    if page == "Pagrindinis":
        show_home()
    elif page == "Peržiūrėti knygas":
        show_all_books()
    elif page == "Atsijungti":
        show_log_out()

def librarian_navigation(lib):
    st.sidebar.title("Navigacija")
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
        st.write("Skaitytoju nėra")

def show_late_books():
    st.subheader("Vėluojančios knygos")
    all_overdue, late_readers = lib.get_all_overdue()
    st.write("Vėluojančios knygos:")
    for book in all_overdue:
        st.write(book)
    st.write("Vėluojantys grąžinti skaitytojai:")
    for reader in late_readers:
        st.write(reader)


if __name__ == "__main__":
    lib = initial_load()
    main(lib)