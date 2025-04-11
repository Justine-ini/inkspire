from typing import List
from src.books.schemas import Book, BookUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
# from src.books.book_data import books
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status, Depends
from src.db.main import get_session
from src.books.service import BookService

book_router = APIRouter()
book_service = BookService()

@book_router.get("/", response_model = List[Book])
async def get_books(session:AsyncSession = Depends(get_session)):
    books = book_service.get_books(session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model = Book)  # Use status code 201 for created resource
async def create_book(book_data: Book, session:AsyncSession = Depends(get_session)) -> dict: # Use Pydantic model for request body
    new_book = book_service.create_book(book_data, session)
    return new_book


@book_router.get("/{book_id}")
async def get_book(book_uid: int, session:AsyncSession = Depends(get_session)) -> dict:
    book = book_service.get_book(book_uid, session)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found") # Add proper HTTP status code


@book_router.patch("/{book_uid}", response_model=BookUpdateModel)
async def update_book(book_uid:int, book_update: BookUpdateModel, session:AsyncSession = Depends(get_session))-> dict:
    book = book_service.update_book(book_uid, book_update, session)
    raise HTTPException(
        status_code=status.HTTP_304_NOT_MODIFIED,
        detail="Book not found"
    )


@book_router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int, session:AsyncSession = Depends(get_session)):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully", "books": books}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )
