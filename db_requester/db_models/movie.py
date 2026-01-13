from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from typing import Dict, Any

Base = declarative_base()


class GenreDBModel(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    movies = relationship("MovieDBModel", back_populates="genre")

    def __repr__(self):
        return f"<Genre(id='{self.id}', name='{self.name}')>"

class MovieDBModel(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    published = Column(Boolean)
    rating = Column(Float)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    created_at = Column(DateTime)

    genre = relationship("GenreDBModel", back_populates="movies")

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "imageUrl": self.image_url,
            "location": self.location,
            "published": self.published,
            "rating": self.rating,
            "genre_id": self.genre_id,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Movie(id={self.id}, name='{self.name}', price={self.price})>"


