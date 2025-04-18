from typing import List
from src.books.schemas import Book, BookUpdateModel, BookCreateModel

from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.book_data import books
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status, Depends
from src.db.main import get_session
from src.books.service import BookService

book_router = APIRouter()
book_service = BookService()

@book_router.get("/", response_model = List[Book])
async def get_books(session:AsyncSession = Depends(get_session)):
    retrieved_books = await book_service.get_books(session)
    return retrieved_books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model = BookCreateModel)  # Use status code 201 for created resource
async def create_book(book_data: BookCreateModel, session:AsyncSession = Depends(get_session)) -> dict: # Use Pydantic model for request body
    created_book = await book_service.create_book(book_data, session)
    return created_book


@book_router.get("/{book_uid}", response_model=Book)
async def get_book(book_uid: str, session:AsyncSession = Depends(get_session)) -> dict:
    retrieved_book = await book_service.get_book(book_uid, session)
    if retrieved_book:
        return retrieved_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found") # Add proper HTTP status code


@book_router.patch("/{book_uid}", response_model=BookUpdateModel)
async def update_book(book_uid:str, book_update: BookUpdateModel, session:AsyncSession = Depends(get_session))-> dict:
    updated_book = await book_service.update_book(book_uid, book_update, session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(
        status_code=status.HTTP_304_NOT_MODIFIED,
        detail="Book not found"
    )


@book_router.delete("/{book_uid}", status_code=status.HTTP_200_OK)
async def delete_book(book_uid: str, session:AsyncSession = Depends(get_session)):
    deleted_book = await book_service.delete_book(book_uid, session)
    if deleted_book:
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )
