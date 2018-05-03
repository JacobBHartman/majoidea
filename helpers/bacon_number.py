#!/usr/bin/python3
"""
    Find the Bacon number between two actors    
"""
import requests
import json
from datetime import datetime
from helpers import parse_actor, parse_movie
from models import storage, Actor, Movie, Search


def find_bacon(source, target):
    """
        Finds the path from source to target actors

        Parameters:
            source: source actor
            target: target actor

        Returns:
            List of dictonaries indicating the path
        [
            {
                id: "movie id",
                movie_poster: "link to movie poster for front end",
                source_actor: "source actor from the initial search",
                source_actor_pic: "picture of actor",
                target_actor: "actor that connects to",
                target_actor_pic: "picture fo target actor"
            },
            {
                id: "movie id",
                movie_poster: "link to movie poster for front end",
                source_actor: "actor that connects from",
                source_actor_pic: "picture of actor",
                target_actor: "actor that connects to",
                target_actor_pic: "picture fo target actor"
            },
            { 
                id: "movie id",
                movie_poster: "link to movie poster for front end",
                source_actor: "actor that connects from",
                source_actor_pic: "picture of actor",
                target_actor: "this will be the final actor, the one in the search",
                target_actor_pic: "picture fo target actor"
            }
        ]
    """
    source_dict = get_movies(source)
    source_movies = source_dict['filmography']
    target_dict = get_movies(target)
    target_movies = target_dict['filmography']
    intersection = [movie for movie in source_movies
                    if movie in target_movies]
    #while len(intersection) == 0:
        # check for actors to find link
    movie = get_movie_info(intersection[0]['id'])
    path = [{"title": movie['title'],
             "movie_poster": movie['poster'],
             "source_actor": source,
             "source_actor_pic": source_dict['image'],
             "target_actor": target,
             "target_actor_pic": target_dict['image']}]
    #if len(intersection) != 0:
        # FOUND MOVIE
    search = Search() 
    setattr(search, "source_actor_name", source)
    setattr(search, "target_actor_name", target)
    setattr(search, "stringJson", json.dumps(path))
    setattr(search, "time_stamp", datetime.utcnow())
    storage.new(search)
    storage.save()
    return path


def get_movies(actor):
    """
        Returns the movies the actor has been in

        Return format:
        [
            "name": "actor name",
            "id": "person_id",
            "image": "link to image",
            "filmography":
            [{
                "type": "Film",
                "imdb_id": "id",
                "title": "movie title",
                "poster": "link to movie poster"
            }
            ...
            ]

    """
    actor = actor.lower()
    movies = storage.query_actor(actor_name=actor)
    if movies is None:
        url = "http://www.theimdbapi.org/api/find/person?name={}".format(actor.replace(' ', '+'))
        result = requests.get(url).json()
        movies = parse_actor(result)
        new_actor = Actor()
        setattr(new_actor, "actor_id", movies["id"])
        setattr(new_actor, "actor_name", movies["name"])
        setattr(new_actor, "stringJson", json.dumps(movies))
        setattr(new_actor, "time_stamp", datetime.utcnow())
        storage.new(new_actor)
        storage.save()
    return movies


def get_movie_info(movie_id):
    """
        Returns the movie information for given movie

        Return format:
        {
            "cast" : [list of actors],
            "title":  "name of movie",
            "id": "movie_id",
            "poster": "link to movie poster"
        }
    """
    movie = storage.query_movie(movie_id)
    if movie is None:
        url = "http://www.theimdbapi.org/api/movie?movie_id={}".format(movie_id)
        result = requests.get(url).json()
        movie = parse_movie(result)
        # TODO: add to database
        new_movie = Movie()
        setattr(new_movie, "movie_id", movie["id"])
        setattr(new_movie, "stringJson", json.dumps(movie))
        setattr(new_movie, "time_stamp", datetime.utcnow())
        storage.new(new_movie)
        storage.save()
    return movie



if __name__ == "__main__":
    print(find_bacon("will smith", "margot robbie"))
