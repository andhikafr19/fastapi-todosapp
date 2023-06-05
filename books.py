from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title" : "Title One", "author" : "Author One", "category" : "science" },
    {"title" : "Title Two", "author" : "Author Two", "category" : "history" },
    {"title" : "Title Three", "author" : "Author Three", "category" : "math" },
    {"title" : "Title Four", "author" : "Author Four", "category" : "history" },
    {"title" : "Title Five", "author" : "Author One", "category" : "math" },
]

# Book - GET
@app.get("/books")
async def read_all_books():
    return BOOKS

# books by author - assignment
@app.get("/books/byauthor/")
async def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return

# path parameter
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
            book.get('category').casefold() == category.casefold():
          books_to_return.append(book)

    return books_to_return

# Book - POST
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

# Book - UPDATE
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

# Book - DELETE
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
        
