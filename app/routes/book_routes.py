from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from .route_utilities import validate_model
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

    try:
        new_book = Book.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }

    return response, 201

@bp.get("")
def get_all_books():
    # create a basic select query without any filtering
    query = db.select(Book)

    # If we have a `title` query parameter, we can add on to the query object
    title_param = request.args.get("title")
    if title_param:     
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        # In case there are books with similar titles, we can also filter by description
        query = query.where(Book.description.ilike(f"%{description_param}%"))
    
    books = db.session.scalars(query.order_by(Book.id))

    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return books_response


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

    return f"Book #{book_id} successfully updated"

@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    return f"Book #{book_id} successfully deleted"