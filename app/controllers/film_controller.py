from ..models.film_model import Film

from flask import request

from decimal import Decimal

from ..models.exceptions import FilmNotFound, InvalidDataError

class FilmController:
    """Film controller class"""

    @classmethod
    def get(cls, film_id):
        """Get a film by id"""
        try:
            film = Film(film_id=film_id)
            result = Film.get(film)
            if result is not None:
                return result.serialize(), 200
            else:
                raise FilmNotFound(film_id)  # Lanzar la excepción si la película no se encuentra
        except FilmNotFound as e:
            return e.get_response() 
        
    @classmethod
    def get_all(cls):
        """Get all films"""
        film_objects = Film.get_all()
        films = []
        for film in film_objects:
            films.append(film.serialize())
        return films, 200
    
    @classmethod
    def create(cls):
        """Create a new film"""
        try:
            data = request.json

            # Validar los datos de entrada
            if len(data.get('title', '')) < 3:
                raise InvalidDataError("Title must have at least three characters")
            if not isinstance(data.get('language_id'), int):
                raise InvalidDataError("Language ID must be an integer")
            if not isinstance(data.get('rental_duration'), int):
                raise InvalidDataError("Rental duration must be an integer")
            if not isinstance(data.get('rental_rate'), int):
                raise InvalidDataError("Rental rate must be an integer")
            if not isinstance(data.get('replacement_cost'), int):
                raise InvalidDataError("Replacement cost must be an integer")
            if not isinstance(data.get('special_features'), list) or \
               not all(isinstance(feature, str) for feature in data.get('special_features')) or \
               not all(feature in ['Trailers', 'Commentaries', 'Deleted Scenes', 'Behind the Scenes'] for feature in data.get('special_features')):
                raise InvalidDataError("Special features must be a list of valid strings")

            # Convertir los campos 'rental_rate' y 'replacement_cost' a Decimal
            if data.get('rental_rate') is not None:
                data['rental_rate'] = Decimal(data.get('rental_rate')) / 100
            if data.get('replacement_cost') is not None:
                data['replacement_cost'] = Decimal(data.get('replacement_cost')) / 100

            # Crear la película
            film = Film(**data)
            Film.create(film)

            return {'message': 'Film created successfully'}, 201
        except InvalidDataError as e:
            return e.get_response()

    @classmethod
    def update(cls, film_id):
        """Update a film"""
        data = request.json

        # TODO: Validate data
        if data.get('rental_rate') is not None:
            if isinstance(data.get('rental_rate'), int):
                data['rental_rate'] = Decimal(data.get('rental_rate'))/100

        if data.get('replacement_cost') is not None:
            if isinstance(data.get('replacement_cost'), int):
                data['replacement_cost'] = Decimal(data.get('replacement_cost'))/100

        data['film_id'] = film_id

        # Verificar si la película existe
        film = Film(film_id=film_id)
        if not film.exists():
            raise FilmNotFound(film_id)

        # TODO: Validate film exists
        Film.update(film)
        return {'message': 'Film updated successfully'}, 200
        
    @classmethod
    def delete(cls, film_id):
        """Delete a film"""
        film = Film(film_id=film_id)

        # TODO: Validate film exists
        Film.delete(film)
        return {'message': 'Film deleted successfully'}, 204