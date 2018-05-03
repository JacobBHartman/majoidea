
def parse_movie(movie):
    return {
        "cast": [o['name'] for o in movie['cast'] if o['name'] != ""],
        "title": movie['title'],
        "id": movie['imdb_id'],
        "poster": movie['poster']['large']
    }

def parse_actor(actorArr):
    actor = actorArr[0]
    if "actor" in actor['filmography']:
        act = "actor"
    else:
        act= "actress"
    return { 
        "name": actor['title'],
        "id": actor['person_id'],
        "image": actor['image']['poster'],
        "filmography": [{
            "id": o['imdb_id'],
            "title": o['title'],
            "year": o['year']
        } for o in actor['filmography'][act] if o['type'] == "Film"]
    }
