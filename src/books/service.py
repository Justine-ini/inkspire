
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
# from src.books.routes import get_books
from src.books.schemas import Book, BookCreateModel, BookUpdateModel
from sqlmodel import select, desc

# To be deleted
from src.books.models import Book

class BookService:
    async def get_books(self, session:AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        books = result.all()

        if not books:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Books not found"
            )

        return books


    async def get_book(self, book_uid:str, session:AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        if not book:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with UID {book_uid} not found"
            )

        return book

  

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        # Convert Pydantic model to dictionary
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        session.add(new_book)
        
        try:
            await session.commit()
            await session.refresh(new_book)
        except Exception as e:
            # Rollback on error
            await session.rollback()
            raise e  
        
        return new_book
    

    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        # Fetch the existing book from the database
        book = await self.get_book(book_uid, session)
        
        if not book:
            return None 
        
        update_data_dict = update_data.model_dump(exclude_unset=True)
        
        for key, value in update_data_dict.items():
            setattr(book, key, value)
        
        try:
            await session.commit()
            await session.refresh(book)
        except Exception as e:
            # Rollback on error
            await session.rollback()
            raise e 
        
        return book
        

    async def delete_book(self, book_uid:str, session:AsyncSession):
        book = await self.get_book(book_uid, session)

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with UID {book_uid} not found"
            )
        
        try:
            await session.delete(book)
            await session.commit()
        except Exception as e:
        # Rollback on error
            await session.rollback()
            raise e  # Propagate the error
    
        return book 