import imdb
import imdb.helpers

moviesDB = imdb.IMDb()

movies = moviesDB.search_movie("good time")[0]

id = movies.getID()
movie = moviesDB.get_movie(id)

directors = " ".join(map(str, movie['directors']))
string = movie.summary()
li = list(string.split("\n"))
print(li)