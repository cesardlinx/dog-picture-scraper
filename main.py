#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_URL = 'https://www.freeimages.com/search/dogs'

engine = create_engine('sqlite:///dogs.db', echo=True)
Base = declarative_base()

class Dog(Base):
    """Database model for a Dog"""
    __tablename__ = 'dogs'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)


def create_database_tables():
    """Creates database tables and deletes previous ones if exist"""
    # Drop all tables associated with the declarative base
    Base.metadata.drop_all(engine)
    # Create the database tables
    Base.metadata.create_all(engine)

def get_dog_urls():
    """Scrapes the url in order to get the dogs urls"""
    dog_urls = []
    page_number = 0

    while (len(dog_urls) < 1000):
        print(f'Scrapping page number {page_number}...')
        page = requests.get(f'{BASE_URL}/{page_number}')
        soup = BeautifulSoup(page.content, 'html.parser')

        istock_top_container = soup.find(id='istock-block-top')
        images_container = istock_top_container.find_next_siblings()[0] 

        pictures = images_container.find_all(
            'img',
            {
                'src': lambda x: x and x.startswith('https://images') and 'banner' not in x
            }
        )

        prev_len = len(dog_urls)

        for picture in pictures:
            dog_urls.append(picture['src'])
        page_number += 1

        if (prev_len == len(dog_urls)):
            break

    return dog_urls


def main():
    """Application entry point"""
    # create database tables
    create_database_tables()

    # get dog urls
    urls = get_dog_urls()

    dogs = [Dog(url=data) for data in urls]

    # save data
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    session.add_all(dogs)
    session.commit()

if __name__ == "__main__":
    main()
