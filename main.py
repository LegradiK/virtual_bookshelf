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

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == 'POST':
        new_bood = BookData(
            title=request.form['title'],
            author=request.form['author'],
            rating=request.form['rating']
        )
        db.session.add(new_bood)
        db.session.commit()
        return redirect(url_for('home'), id=new_bood.id)
    
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

