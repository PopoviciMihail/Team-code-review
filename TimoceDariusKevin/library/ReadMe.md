Review the FastAPI tutorial (https://fastapi.tiangolo.com/tutorial/) carefully and use it to build a simple REST API for managing a collection of books in a library.

# Endpoints requirements:
- Create a book
    Endpoint: POST /books/
    Request body:
    {
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "year": 1999,
        "isbn": "978-0201616224"
    }
    Response: Return the created book with a unique ID.
- Read all books
    Endpoint: GET /books/
    Response: List all stored books.
- Read a single book by ID
    Endpoint: GET /books/{book_id}
    Response: Return the book with that ID or an error if not found.
- Update a book
    Endpoint: PUT /books/{book_id}
    Request body: Same as creation.
    Response: Return the updated book.
- Delete a book
    Endpoint: DELETE /books/{book_id}
    Response: Confirm deletion.

Moreover, find a way to integrate the requests and pandas libraries into your solution. Use your creativity.

## Additional Reqs(just for my personal bit of fun.):
- Create a second entity user
- Augment the Book entity with pseudonym
- Augment the Book entity with a quantity
- Users may come as Admins, Guests or Privileged
- Each Guest may see books and add to their own personal lists
- Books may be listed, or added only within the limit of their availability
- Each Privileged user may see the true name of the author
- Each Admin may see all users and their personal lists
- Each Admin may manage each user's personal collection
- Admins may not see the true name of author's
- Admins may remove a Privileged Users's account
- User accounts will be persisted within a database
- Augment Get call for books with get paginated
- Augment Get call for books with get sorted
- (Possibly add a sorted/filetered query object)?
- Add security token that is checked for roles
- Add CORS specialization
- Add custom errors and handling
- Users's passwords should be hashed before storing

