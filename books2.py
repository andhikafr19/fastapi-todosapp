from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    # constructor class Book
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

# validation from library pydantic
class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is optional/ not needed')              # Optional -> id tidak harus diinputkan
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=-1, lt=6)   # gt(greater than), lt(less than)
    published_date: int
    
    # swagger documentation API config
    class Config:
      schema_extra = {
        'example': {
          'title': 'A new title of book',
          'author': 'The Author of book',
          'description': 'A new description of book',
          'rating': 5,
          'published_date': 2023
        } 
      }


BOOKS = [
    Book(1, 'Learning Python', 'Eric', 'How to Learn Python', 5, 2020),         #object
    Book(2, 'Learning FastAPI', 'Eric', 'How to Learn FastAPI', 5, 2020),
    Book(3, 'Title 1', 'Anonim', 'Anonim Description', 3, 2020),
    Book(4, 'Title 2', 'Anonim', 'Anonim Description', 3, 2020),
    Book(5, 'Title 3', 'Anonim2', 'Anonim Description', 4, 2020),
    Book(6, 'Title 4', 'Anonim2', 'Anonim Description', 5, 2021),
]

# Book - GET
@app.get("/books", status_code=status.HTTP_200_OK) #status_code menggunakan library starlette
async def read_all_books():
    return BOOKS
  
# GET Book by ID
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):         # Path(gt=0) adalah path parameter validation
  for book in BOOKS:
    if book.id == book_id:
      return book
  raise HTTPException(status_code=404, detail='Item Not Found')

# GET Book by Rating
@app.get("/books/rating/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
  books_to_return = []
  for book in BOOKS:
    if book.rating == book_rating:
      books_to_return.append(book)
  return books_to_return

# Assignment - GET Book by Published Date
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(publish_date: int = Query(gt=1999, lt=2040)):
  books_to_return = []
  for book in BOOKS:
    if book.published_date == publish_date:
      books_to_return.append(book)
  return books_to_return

# Book - POST
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))

# function untuk ID autogenerate
def find_book_id(book: Book):
  # if len(BOOKS) > 0:
  #   book.id = BOOKS[-1].id + 1
  # else:
  #   book.id = 1
  book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
  return book

# Book - PUT
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def updated_book(book: BookRequest):
  book_changed = False
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book.id:
      BOOKS[i] = book
      book_changed = True
  if not book_changed:
    raise HTTPException(status_code=404, detail='Item not Found')
      
# Book - DELETE
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):         # Path(gt=0) adalah path parameter validation
  book_changed = False
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book_id:
      BOOKS.pop(i)
      book_changed = True
      break
  if not book_changed:
    raise HTTPException(status_code=404, detail='ID Not Found')