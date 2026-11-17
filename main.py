# This is a sample Python script.
import pymongo
from pip._internal.utils import deprecation
from pymongo import MongoClient, AsyncMongoClient, server_api
import json
import asyncio
import configparser
from typing import TypedDict


class Movie(TypedDict):
    title: str
    director: str
    year: int





# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def getUri(isLocal:bool, pickCredentials="credentials_student") -> str:

    config = configparser.RawConfigParser()
    config.read('config.ini', encoding='utf-8')

    # Access credentials
    db_username = config.get(pickCredentials, 'username')
    db_password = config.get(pickCredentials, 'password')

    uri = f"mongodb+srv://{db_username}:{db_password}@cluster0.hqts3.mongodb.net/?authSource=admin"
    if isLocal:
        uri = "mongodb://localhost:27017/"
    return uri


async def TestConnectionAndInitialQuery(isLocal:bool, uri: str):

    database, collection = getDatabaseCollection(isLocal)

    client: AsyncMongoClient[Movie] = AsyncMongoClient(uri,server_api=pymongo.server_api.ServerApi(version="1", strict=True, deprecation_errors=True))

    print(uri)
    async with AsyncMongoClient(uri) as client:
        await client.admin.command("ping")
        print("Connected Successfully")


        try:
            database = client[database]
            movies = database[collection]


            query = {"title": "Back to the Future"}
            project = {'_id':1, 'year':1, 'director': { '$slice': ['$directors', 1] }}
            movie = await movies.find_one(query, project)
            #print(movie)

            print(json.dumps(movie, indent=4, default=str))

            # await client.close()
        except Exception as e:
            raise Exception("Unable to find the document due to the following error:",e)

def getDatabaseCollection(isLocal:bool):
    database = "sample_mflix"
    collection = "movies"
    if isLocal:
        database = "MoviesDatabase"
        collection = "Movies"
    return database, collection

async def CRUD_Operations():
    '''
    Create the Reviewers Collection or add to it if already exists.
    Enter your name as a Reviewer and save the _id field.
    Use the _id as ReviewerID in a Reviews collection.
    Use the _id of a selected movie and give the movie a rating (int) 1..5

    Recap
    Reviewer collection:
    FirstName, LastName
    Save the object returned by the insertOne to a variable reviewerInfo
    Get the _id, title, and year of a movie and save that to a variable movieInfo
    Reviews collection:
    reviewerInfo, movieInfo, Rating
    Get a few more movies and add more reviews with the same reviewerInfo
    '''
    #await sample

    client: AsyncMongoClient[Movie] = AsyncMongoClient(uri, server_api=pymongo.server_api.ServerApi(version="1",
                                                                                                    strict=True,
                                                                                                    deprecation_errors=True))

    async with AsyncMongoClient(uri) as client:
        database, collection = getDatabaseCollection(isLocal)
        try:
            database = client[database]
            movies = database[collection]
            # Add a reviewer
            reviewerDoc = {"FirstName":"Marc", "LastName":"Temkin"}
            reviewer = await database.reviewer.insert_one(reviewerDoc)
            reviewerRec = await database.reviewer.find_one({"_id": reviewer.inserted_id})
            reviewerInfo ={
                "id": reviewerRec['_id'],
                "FirstName": reviewerRec['FirstName'],
                "LastName": reviewerRec['LastName'],
            }
            # Find some movies that have Star Wars within the title
            moviesToReview = movies.find({"title":{"$regex": "Star Wars", "$options": "i"}},{"_id":1, "title":1, "year":1, "director":{"$slice":["$directors", 1]}})
            async for movieToReview in moviesToReview:
                print(f"{movieToReview["title"]}, {movieToReview['year']}, {movieToReview['director']}")
                rating = input("Enter your rating (1-5):")
                print (rating)
                doc = { "Reviewer":reviewerInfo, "Movie": movieToReview, "Rating": rating }
                await database.reviews.insert_one(doc)

            print("Done")

        except Exception as e:
            raise Exception("Unspecified error:",e)


isLocal = False


uri = getUri(isLocal, pickCredentials="credentials_student")
asyncio.run(TestConnectionAndInitialQuery(isLocal, uri=uri))
asyncio.run(CRUD_Operations())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
