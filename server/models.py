from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint


db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Every author must have a name.")

        author = Author.query.filter(Author.name == name).first()
        if author:
            raise ValueError(f"An author with the name '{name}' already exists.")

        return name

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number must have 10 digits.")
        else:
            return phone_number

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Post(db.Model):
    __tablename__ = "posts"
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("title")
    def validate_title(self, key, title):
        clickbaity_terms = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title:
            raise ValueError("Each post must have a title")
        if title not in clickbaity_terms:
            raise ValueError("Title is not clickbait-y enough")
        return title

    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be 250 characters long.")
        else:
            return content

    @validates("summary")
    def validates_summary(self, key, summary):
        if len(summary) >= 250:
            raise ValueError("Summary cannot be longer than 250 characters.")
        else:
            return summary

    @validates("category")
    def validates_category(self, key, category):
        categories = ["Fiction", "Non-Fiction"]
        if category not in categories:
            raise ValueError("Category must either be Fiction or Non-Fiction.")
        else:
            return category

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})"
