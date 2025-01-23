from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class BookData(db.Model):
    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    review: Mapped[str] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()

# # id is auto-generated
# with app.app_context():
#     new_book = BookData(id=1, title="Harry Potter", author="J. K. Rowling", review=9.3)

# # read all the records
# with app.app_context():
#     result = db.session.execute(db.select(BookData).order_by(BookData.title))
#     all_books = result.scalars()

# # read a particular record by query
# # to get a single data - use scalar()
# # to get multiple data - use scalars()
# with app.app_context():
#     book = db.session.execute(db.select(BookData).where(BookData.title == "Harry Potter")).scalar()

# # update a record by primary key
# book_id = 1
# with app.app_context():
#     book_to_update = db.session.execute(db.select(BookData).where(BookData.id == book_id)).scalar()
#     book_to_update.title = "Harry Potter and the Goblet of Fire"
#     db.session.commit()

# # will raise a 404 if the row with the given id doesn’t exist, otherwise it will return the instance.
# with app.app_context():
#     book_details = db.get_or_404(BookData, id=book_id)

# # delete a particular record by primary key
# with app.app_context():
#     book_to_delete = db.session.execute(db.select(BookData).where(BookData.id == book_id)).scalar()
#     db.session.delete(book_to_delete)
#     db.session.commit()

@app.route('/', methods=['GET','POST'])
def home():
    with app.app_context():
        result = db.session.execute(db.select(BookData).order_by(BookData.id))
        all_books = result.scalars().all()
    return render_template('index.html', books=all_books)

@app.route('/delete')
def delete():
    book_id = request.args.get('book_id')
    # DELETE A RECORD BY ID
    book_to_delete = db.get_or_404(BookData, book_id)
    # Alternative way to select the book to delete.
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == 'POST':

        with app.app_context():
            # Check if the title already exists
            existing_book = db.session.execute(
                db.select(BookData).where(BookData.title == request.form['title'])
            ).scalar()

            if existing_book:
                return "A book with this title already exists.", 400
            else:
                # getting id of the last data in the database
                last_book = db.session.execute(db.select(BookData).order_by(BookData.id.desc())).scalar()
                last_id = last_book.id if last_book else 0

                new_book = BookData(
                    id=last_id + 1, 
                    title=request.form['title'],
                    author=request.form['author'], 
                    review=request.form['rating']
                )

                
                db.session.add(new_book)
                db.session.commit()
                return redirect(url_for('home'))
    
    return render_template('add.html')

@app.route('/edit/<book_id>', methods=['GET','POST'])
def edit(book_id):
    with app.app_context():
        book = db.session.execute(db.select(BookData).where(BookData.id == book_id)).scalar()
        if request.method == 'POST':
            book.review = request.form['rating']
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('edit.html', book=book)


if __name__ == "__main__":
    app.run(debug=True)

