from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from .route_utilities import create_model, validate_model, get_models_with_filters
from ..db import db
# from app.models.book import books
# from app.models.book import validate_model



bp = Blueprint("bp", __name__, url_prefix="/books")

# @bp.get("")
# def get_all_books():
#     books_response = []
#     for book in books:
#         books_response.append(
#             {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             }
#         )
#     # print(books_response)    
#     return books_response


# @bp.get("/<book_id>")
# def get_one_book(book_id):
#     # book_id = int(book_id)
#     try:
#         book_id = int(book_id)
#     except:
#         return {"message": f"book {book_id} invalid"}, 400
    
#     for book in books:
#         if book.id == book_id:
#             return {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description,
#             }
        
#     return {"message": f"book {book_id} not found"}, 404

# @bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_model(Book, book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description,
#     }

@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)

@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args)


@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)
    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)
    return {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            }


@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body['title']
    book.description = request_body['description']
    db.session.commit()

    return {
            "message": f"Book #{book_id} successfully updated"
            }

@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    return {
            "message": f"Book #{book_id} successfully deleted"
            }