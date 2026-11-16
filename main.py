# This is a sample Python script.
import pymongo
from pip._internal.utils import deprecation
from pymongo import MongoClient, AsyncMongoClient, server_api
import json
import asyncio
from typing import TypedDict


class Movie(TypedDict):
    name: str
    year: int

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

async def main():
    db_username = 'mtemkin'
    db_password = 'vHBZclh2TWRL7ixK'
    uri = f"mongodb+srv://{db_username}:{db_password}@cluster0.hqts3.mongodb.net/?authSource=admin"


    isLocal = False
    database = "sample_mflix"
    collection = "movies"
    if isLocal:
        uri = "mongodb://localhost:27017/"
        database = "MoviesDatabase"
        collection = "Movies"


    client: AsyncMongoClient[Movie] = AsyncMongoClient(uri,server_api=pymongo.server_api.ServerApi(version="1", strict=True, deprecation_errors=True))

    print(uri)
    async with AsyncMongoClient(uri) as client:
        await client.admin.command("ping")
        print("Connected Successfully")





        try:
            database = client.get_database(database)
            movies = database.get_collection(collection)


            query = {"title": "Back to the Future"}
            project = {'_id':1, 'year':1, 'director': { '$slice': ['$directors', 1] }}
            movie = await movies.find_one(query, project)
            #print(movie)

            print(json.dumps(movie, indent=4, default=str))

            # await client.close()
        except Exception as e:
            raise Exception("Unable to find the document due to the following error:",e)

asyncio.run(main())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
