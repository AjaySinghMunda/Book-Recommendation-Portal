import pymongo
import streamlit as st

# MongoDB Connection
conn = pymongo.MongoClient(st.secrets["MONGO_URI"])

db = conn["BookRecommendationSystem"]

catalog_collection = db["Catalog"]

books = [
    {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J. K. Rowling",
        "genre": "Fantasy",
        "publication_year": 1997,
        "description": "A young wizard discovers his magical heritage and begins his magical education at Hogwarts while confronting dark forces."
    },
    {
        "title": "The Hobbit",
        "author": "J. R. R. Tolkien",
        "genre": "Fantasy",
        "publication_year": 1937,
        "description": "Bilbo Baggins joins a company of dwarves on an epic adventure to reclaim their homeland from a dragon."
    },
    {
        "title": "The Da Vinci Code",
        "author": "Dan Brown",
        "genre": "Mystery",
        "publication_year": 2003,
        "description": "A symbologist investigates a murder in Paris while uncovering hidden religious secrets and ancient conspiracies."
    },
    {
        "title": "A Study in Scarlet",
        "author": "Arthur Conan Doyle",
        "genre": "Mystery",
        "publication_year": 1887,
        "description": "Sherlock Holmes solves his very first case using brilliant observation, logic and deduction."
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "genre": "Science Fiction",
        "publication_year": 1965,
        "description": "A young nobleman fights for survival and power on the desert planet Arrakis."
    },
    {
        "title": "The Martian",
        "author": "Andy Weir",
        "genre": "Science Fiction",
        "publication_year": 2011,
        "description": "An astronaut stranded on Mars uses science and engineering to survive alone."
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "genre": "Romance",
        "publication_year": 1813,
        "description": "Elizabeth Bennet navigates love, family and society in nineteenth-century England."
    },
    {
        "title": "Me Before You",
        "author": "Jojo Moyes",
        "genre": "Romance",
        "publication_year": 2012,
        "description": "A young caregiver forms a life-changing relationship with a man whose life has been transformed by an accident."
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "genre": "Adventure",
        "publication_year": 1988,
        "description": "A shepherd searches for treasure while discovering his life's true purpose."
    },
    {
        "title": "Into the Wild",
        "author": "Jon Krakauer",
        "genre": "Adventure",
        "publication_year": 1996,
        "description": "The true story of Christopher McCandless and his journey into the Alaskan wilderness."
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": "Self Help",
        "publication_year": 2018,
        "description": "A practical guide to building good habits and breaking bad ones."
    },
    {
        "title": "Deep Work",
        "author": "Cal Newport",
        "genre": "Productivity",
        "publication_year": 2016,
        "description": "Strategies for improving focus and producing meaningful work."
    },
    {
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "genre": "History",
        "publication_year": 2011,
        "description": "An exploration of the history and evolution of humankind."
    },
    {
        "title": "Educated",
        "author": "Tara Westover",
        "genre": "Memoir",
        "publication_year": 2018,
        "description": "A memoir about overcoming an isolated upbringing through education."
    },
    {
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "genre": "Thriller",
        "publication_year": 2019,
        "description": "A psychotherapist investigates why a famous artist stopped speaking after a shocking crime."
    },
    {
        "title": "Gone Girl",
        "author": "Gillian Flynn",
        "genre": "Thriller",
        "publication_year": 2012,
        "description": "A missing wife case reveals deception, manipulation and shocking twists."
    },
    {
        "title": "The Fault in Our Stars",
        "author": "John Green",
        "genre": "Young Adult",
        "publication_year": 2012,
        "description": "Two teenagers with cancer fall in love while learning to appreciate life."
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "genre": "Dystopian",
        "publication_year": 1949,
        "description": "A man struggles against government surveillance and authoritarian control."
    },
    {
        "title": "Animal Farm",
        "author": "George Orwell",
        "genre": "Political Satire",
        "publication_year": 1945,
        "description": "Farm animals overthrow their owner only to witness corruption among themselves."
    },
    {
        "title": "The Girl with the Dragon Tattoo",
        "author": "Stieg Larsson",
        "genre": "Crime",
        "publication_year": 2005,
        "description": "A journalist and a brilliant hacker investigate a decades-old disappearance."
    }
]

catalog_collection.delete_many({})

catalog_collection.insert_many(books)

print("Catalog uploaded successfully!")