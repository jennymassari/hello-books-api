from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db
# from app.models.book import books
# from app.models.book import validate_book



books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

# @books_bp.get("")
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


# @books_bp.get("/<book_id>")
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

# @books_bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_book(book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description,
#     }

@books_bp.post("")
def create_book():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]

    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }

    return response, 201

@books_bp.get("")
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


@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)
    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)
    return {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            }


@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body['title']
    book.description = request_body['description']
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_book(book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")



def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"message": f"book {book_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)
    
    if not book:
        response = {"message": f"book {book_id} not found"}
        abort(make_response(response, 404))

    return book
    





