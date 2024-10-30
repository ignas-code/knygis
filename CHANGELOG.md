# Changelog

## Version 0.1.0
- **User Login System**: Introduced separate login pages for readers and librarians.
  - **Reader Login**: Allows login with a reader card number.
  - **Librarian Login**: Allows login using a username and password.

- **Reader Features**:
  - **View Books**: Readers can browse a list of available books and sort by various criteria.
  - **Borrow Book**: Allows book borrowing if no overdue books are pending.
  - **Return Book**: Enables users to select and return borrowed books.
  - **Search Books**: Supports searching by title or author.
  - **View Borrowed Books**: View a list of currently borrowed books and the borrowing history.
  - **Logout**: End session for the reader.

- **Librarian Features**:
  - **Add Book**: Allows librarians to add new books or update quantities of existing books.
  - **Remove Books**: Remove books based on publication date or book ID.
  - **View Library Books**: Complete list of library books.
  - **Add Reader**: Add new readers, automatically generating their reader card codes.
  - **View Readers**: Display all readers and their respective card codes.
  - **Overdue Books**: Display overdue books and associated readers.
  - **Data Initialization**: Load predefined data if not previously done.
  - **Logout**: End session for the librarian.

---

## Version 0.2.0
- **Database Migration**: Migrated data storage to SQLite for improved stability, scalability, and enhanced data querying capabilities.
- **Reader Login**: Allows login using first name, last name, and reader card number.
- **Borrow Book**: The maximum number of books a reader can borrow has been limited to 3.
- **Soft Delete and Restore Functionality**: Implemented soft delete for books, allowing deleted items to be marked as inactive rather than permanently removed. This feature also enables the restoration of deleted books, providing greater flexibility in book management.

---

## Version 0.2.1
- **Main Page**: Added statistics to main page - total books, total readers, currently taken books, 5 most popular books