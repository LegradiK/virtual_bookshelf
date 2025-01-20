from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


app = Flask(__name__)

# absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# relative path to the database file
db_file_path = os.path.join(current_dir, 'python_day63_virtual_bookshelf','book_collection_database','new-books-collection.db')

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file_path}"

db.init_app(app)

class BookData(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    titles: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    rating: Mapped[int]

with app.app_context():
    db.create_all()

@app.route('/')
def home():   
    book_data = db.session.execute(db.select(BookData).order_by(BookData.titles)).scalars()
    return render_template('index.html', books=book_data)


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        # all_books.append(request.form.to_dict())
        new_book = BookData(
            title=request.form["title"],
            author=request.form['author'],
            rating=request.form['rating']
            db.session.add(new_book)
            db.session.commit()
        )
        return redirect(url_for('home'), id=new_book.id)

    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

