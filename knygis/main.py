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
        show_all_books(lib)
    elif page == "Atsijungti":
        show_log_out()

def librarian_navigation(lib):
    st.sidebar.title("Navigacija")
    page = st.sidebar.radio("Pasirinkite:", ["Pagrindinis", "Pridėti knygą", "Peržiūrėti knygas", "Atsijungti"])

    if page == "Pagrindinis":
        show_home()
    elif page == "Pridėti knygą":
        show_add_book()
    elif page == "Peržiūrėti knygas":
        show_all_books(lib)
    elif page == "Atsijungti":
        show_log_out()

def show_home():
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
        quantity = st.number_input("Įveskite kiekį:", min_value=1, step=1)
    
        submit_button = st.form_submit_button("Pridėti")

        if submit_button:
            if name and author and genre:
                lib.add_book(name,author,year,genre,quantity)
                save(lib)
                st.success(f"Book '{name}' by {author} added successfully!")
                st.session_state['last_added_book'] = name 
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

def show_all_books(lib):
    st.subheader("Mūsų knygos:")
    books = lib.all_books()
    for book in books:
        st.write(book)

if __name__ == "__main__":
    lib = initial_load()
    main(lib)