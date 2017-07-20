"""Helper functions for querying database and pulling favorite genres and counts of favorited genres of one user or all users."""

from model import Museum


def get_favorited_genres_all(trips_favorited_all):
    """Queries database for the count of genres favorited by users and a list of genres that can be favorited."""

    museum_ids_all = []
    for trip in trips_favorited_all:
        museum_ids_all.append(trip.museum_id)
    
    museums_all = []
    for id in museum_ids_all:
        museum = Museum.query.filter_by(museum_id=id).first()
        museums_all.append(museum)

    dict_genres_all = {'Impressionism': 0, 'Africa, Oceania, the Americas': 0, 
                    'California Art': 0, 'Jewish Art': 0, 'Expressionism': 0, 
                    'Chinese Ink Painting': 0, 'Mixed Media': 0, 'Asian Art': 0}
    for museum in museums_all:
        genre_name = museum.genre.genre_name
        dict_genres_all[genre_name] = dict_genres_all.get(genre_name, 0) + 1

    dict_genres_all = sorted(dict_genres_all.items())    
    genre_names_all = []
    counts_all = []
    for t in dict_genres_all:
        genre_names_all.append(t[0])
        counts_all.append(t[1]) 

    return [genre_names_all, counts_all]
    

def get_favorited_genres_user(trips_favorited_user):
    """Queries database for the count of genres favorited by a user and all users and a list of genres that can be favorited."""

    museum_ids_user = []
    for trip in trips_favorited_user:
        museum_ids_user = [trip.museum_id for trip in trips_favorited_user]

    museums_user = []
    for id in museum_ids_user:
        museum = Museum.query.filter_by(museum_id=id).first()
        museums_user.append(museum)

    dict_genres_user = {'Impressionism': 0, 'Africa, Oceania, the Americas': 0, 
                    'California Art': 0, 'Jewish Art': 0, 'Expressionism': 0, 
                    'Chinese Ink Painting': 0, 'Mixed Media': 0, 'Asian Art': 0}
    for museum in museums_user:
        genre_name = museum.genre.genre_name
        dict_genres_user[genre_name] = dict_genres_user.get(genre_name, 0) + 1

    dict_genres_user = sorted(dict_genres_user.items())    
    counts_user = []
    for t in dict_genres_user:
        counts_user.append(t[1])

    return counts_user




    

        

   
