# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from datetime import datetime
from mysql.connector import IntegrityError

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import pyodbc

class HouseScraperPipeline:
    def process_item(self, item, spider):
        

        adapter = ItemAdapter(item)

        # Strip the $ sign from the price
        price = adapter.get("price")
        price = price.replace("$", "")
        price = price.replace(",", "")
        adapter["price"] = price

        # get the location together
        try:
            location = adapter.get("location")

            location_split = location.split(", ")
            adapter["apartment_no"] = location_split[0].split(" ")[0]
            adapter["street"] = " ".join(location_split[0].split(" ")[1:])
            adapter["city"] = location_split[1]
            adapter["state"] = location_split[2].split(" ")[0]
            adapter["zip_code"] = " ".join(location_split[2].split(" ")[1:])
        except:
            adapter["apartment_no"] = None
            adapter["street"] = None
            adapter["city"] = None
            adapter["state"] = None
            adapter["zip_code"] = None

        # get the location tag together
        location_tag = adapter.get("location_tag")

        adapter["location_tag"] = location_tag.strip('<span> (').strip(')</span>')

        # get latitude and longitude from google maps url
        try:
            google_maps_url = adapter.get("google_maps_url")
            split_url = google_maps_url.split("/")[-1].split(",")
            adapter["latitude"] = split_url[0]
            adapter["longitude"] = split_url[1]
        except:
            adapter["latitude"] = None
            adapter["longitude"] = None

        # get the number of bedrooms and bathrooms
        try: 
            br_ba = adapter.get("br_ba")
            split_br_ba = br_ba.split(" / ")
            adapter["bed_rooms"] = split_br_ba[0].replace("BR", "")
            adapter["bath_rooms"] = split_br_ba[1].replace("Ba", "")
        except:
            adapter["bed_rooms"] = None
            adapter["bath_rooms"] = None

        # take the ft out of the square footage
        try:
            ft = adapter.get("ft")
            if "ft" in ft:
                adapter["ft"] = ft.replace("ft", "")
            else:
                adapter["ft"] = None
        except:
            adapter["ft"] = None
        
        # get the posting date
        
        posting_date = adapter.get("posting_date")
        adapter["posting_date"] = datetime.strptime(posting_date, "%Y-%m-%dT%H:%M:%S%z")

        return item

# class SaveToMySQLPipeline:

#     def __init__(self):
#         self.conn =  pyodbc.connect(
#             'DRIVER={ODBC Driver 17 for SQL Server};'
#             'SERVER=house-server.database.windows.net;'
#             'DATABASE=house_db;'
#             'UID=sekanti02;'
#             'PWD=fatih_24584040'
#         )
#         ## Create cursor, used to execute commands
#         self.cursor = self.conn.cursor()
        
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS houses (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 url VARCHAR(255) UNIQUE NOT NULL,
#                 title VARCHAR(255) NOT NULL,
#                 price DECIMAL(10, 2) NOT NULL,
#                 apartment_no VARCHAR(255),
#                 street VARCHAR(255),
#                 city VARCHAR(255),
#                 state VARCHAR(255),
#                 zip_code VARCHAR(255),
#                 location_tag VARCHAR(255),
#                 google_maps_url VARCHAR(255),
#                 latitude DECIMAL(10, 8),
#                 longitude DECIMAL(11, 8),
#                 br_ba VARCHAR(255),
#                 bed_rooms INT,
#                 bath_rooms INT,
#                 ft INT,
#                 available_till VARCHAR(255),
#                 cover_img VARCHAR(255),
#                 posting_id VARCHAR(255),
#                 posting_date DATETIME,
#                 is_available_now BOOLEAN,
#                 has_cats_ok BOOLEAN,
#                 has_dogs_ok BOOLEAN,
#                 has_wd_in_unit BOOLEAN,
#                 is_furnished BOOLEAN,
#                 has_attached_garage BOOLEAN,
#                 no_smoking BOOLEAN,
#                 is_wheelchair_accessible BOOLEAN,
#                 has_air_conditioning BOOLEAN,
#                 has_ev_charging BOOLEAN
#             )
#         """)
#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#         try:
#             self.cursor.execute(
#                 """
#                 INSERT INTO houses (url, title, price, apartment_no, street, city, state, zip_code, location_tag, google_maps_url, latitude, longitude, br_ba, bed_rooms, bath_rooms, ft, available_till, cover_img, posting_id, posting_date, is_available_now, has_cats_ok, has_dogs_ok, has_wd_in_unit, is_furnished, has_attached_garage, no_smoking, is_wheelchair_accessible, has_air_conditioning, has_ev_charging)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """,
#                 (
#                     adapter.get("url"),
#                     adapter.get("title"),
#                     adapter.get("price"),
#                     adapter.get("apartment_no"),
#                     adapter.get("street"),
#                     adapter.get("city"),
#                     adapter.get("state"),
#                     adapter.get("zip_code"),
#                     adapter.get("location_tag"),
#                     adapter.get("google_maps_url"),
#                     adapter.get("latitude"),
#                     adapter.get("longitude"),
#                     adapter.get("br_ba"),
#                     adapter.get("bed_rooms"),
#                     adapter.get("bath_rooms"),
#                     adapter.get("ft"),
#                     adapter.get("available_till"),
#                     adapter.get("cover_img"),
#                     adapter.get("posting_id"),
#                     adapter.get("posting_date"),
#                     adapter.get("is_available_now"),
#                     adapter.get("has_cats_ok"),
#                     adapter.get("has_dogs_ok"),
#                     adapter.get("has_wd_in_unit"),
#                     adapter.get("is_furnished"),
#                     adapter.get("has_attached_garage"),
#                     adapter.get("no_smoking"),
#                     adapter.get("is_wheelchair_accessible"),
#                     adapter.get("has_air_conditioning"),
#                     adapter.get("has_ev_charging")
#                 )
#             )
#             self.conn.commit()
#         except IntegrityError as e:
#             # Duplicate entry, skip this item
#             raise DropItem(f"Duplicate item found: {e}")
        
#         return item # So that if we further pipeline, our operation will continue

#     def close_spider(self, spider):
#         self.cursor.close()
#         self.conn.close()

import pyodbc
import logging
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
import os

class SaveToSQLServerPipeline:
    def __init__(self):
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=house-server.database.windows.net;'
            'DATABASE=house_db;'
            f'UID={os.environ.get('DATABASE_USERNAME')};' 
            F'PWD={os.environ.get('DATABASE_PASSWORD')}'
        )
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
            IF OBJECT_ID('houses', 'U') IS NULL
            BEGIN
                CREATE TABLE houses2 (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    url VARCHAR(255) UNIQUE NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    apartment_no VARCHAR(255),
                    street VARCHAR(255),
                    city VARCHAR(255),
                    state VARCHAR(255),
                    zip_code VARCHAR(255),
                    location_tag VARCHAR(255),
                    google_maps_url VARCHAR(255),
                    latitude DECIMAL(10, 8),
                    longitude DECIMAL(11, 8),
                    br_ba VARCHAR(255),
                    bed_room FLOAT,
                    bath_rooms  FLOAT,
                    ft INT,
                    available_till VARCHAR(255),
                    cover_img VARCHAR(255),
                    posting_id VARCHAR(255),
                    posting_date DATETIME,
                    is_available_now BIT,
                    has_cats_ok BIT,
                    has_dogs_ok BIT,
                    has_wd_in_unit BIT,
                    is_furnished BIT,
                    has_attached_garage BIT,
                    no_smoking BIT,
                    is_wheelchair_accessible BIT,
                    has_air_conditioning BIT,
                    has_ev_charging BIT
                )
            END
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        try:
            self.cursor.execute(
                """
                INSERT INTO houses (url, title, price, apartment_no, street, city, state, zip_code, location_tag, google_maps_url, latitude, longitude, br_ba, bed_rooms, bath_rooms, ft, available_till, cover_img, posting_id, posting_date, is_available_now, has_cats_ok, has_dogs_ok, has_wd_in_unit, is_furnished, has_attached_garage, no_smoking, is_wheelchair_accessible, has_air_conditioning, has_ev_charging)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    adapter.get("url"),
                    adapter.get("title"),
                    adapter.get("price"),
                    adapter.get("apartment_no"),
                    adapter.get("street"),
                    adapter.get("city"),
                    adapter.get("state"),
                    adapter.get("zip_code"),
                    adapter.get("location_tag"),
                    adapter.get("google_maps_url"),
                    adapter.get("latitude"),
                    adapter.get("longitude"),
                    adapter.get("br_ba"),
                    adapter.get("bed_rooms"),
                    adapter.get("bath_rooms"),
                    adapter.get("ft"),
                    adapter.get("available_till"),
                    adapter.get("cover_img"),
                    adapter.get("posting_id"),
                    adapter.get("posting_date"),
                    adapter.get("is_available_now"),
                    adapter.get("has_cats_ok"),
                    adapter.get("has_dogs_ok"),
                    adapter.get("has_wd_in_unit"),
                    adapter.get("is_furnished"),
                    adapter.get("has_attached_garage"),
                    adapter.get("no_smoking"),
                    adapter.get("is_wheelchair_accessible"),
                    adapter.get("has_air_conditioning"),
                    adapter.get("has_ev_charging")
                )
            )
            self.conn.commit()
        except pyodbc.IntegrityError as e:
            logging.error(f"Duplicate item found: {e}")
            raise DropItem(f"Duplicate item found: {e}")
        except pyodbc.Error as e:
            logging.error(f"Error inserting item: {e}")
            self.conn.rollback()
        
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()