# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

"""
yield {
            "url": response.url,
            "title": response.xpath('//span[@id="titletextonly"]/text()').get(),
            "price": response.css("span.price::text").get(),
            "location": response.css("h2.street-address::text").get(),
            "location_tag": response.css("h1.postingtitle span")[-1].get(),
            "google_maps_url": response.css("p.mapaddress a").attrib.get("href"),
            "br_ba": br_ba,
            "ft": ft,
            "available_till": available_till,
            "cover_img" : response.xpath('//*[@class="slide first visible"]//img').attrib.get("src"),
            "posting_id" : response.css(".postinginfos p.postinginfo ::text")[0].get().split(": ")[-1],
            "posting_date" : response.css(".postinginfos .date")[0].attrib.get("datetime"),
            'is_available_now': is_available_now,
            'has_cats_ok': has_cats_ok,
            'has_dogs_ok': has_dogs_ok,
            'has_wd_in_unit': has_wd_in_unit,
            'is_furnished': is_furnished,
            'has_attached_garage': has_attached_garage,
            'no_smoking': no_smoking,
            'is_wheelchair_accessible': is_wheelchair_accessible,
            'has_air_conditioning': has_air_conditioning,
            'has_ev_charging': has_ev_charging,
        }
"""

class HouseItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    apartment_no = scrapy.Field()
    street = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    location_tag = scrapy.Field()
    google_maps_url = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    br_ba = scrapy.Field()
    bed_rooms = scrapy.Field()
    bath_rooms = scrapy.Field()
    ft = scrapy.Field()
    available_till = scrapy.Field()
    cover_img = scrapy.Field()
    posting_id = scrapy.Field()
    posting_date = scrapy.Field()
    is_available_now = scrapy.Field()
    has_cats_ok = scrapy.Field()
    has_dogs_ok = scrapy.Field()
    has_wd_in_unit = scrapy.Field()
    is_furnished = scrapy.Field()
    has_attached_garage = scrapy.Field()
    no_smoking = scrapy.Field()
    is_wheelchair_accessible = scrapy.Field()
    has_air_conditioning = scrapy.Field()
    has_ev_charging = scrapy.Field()