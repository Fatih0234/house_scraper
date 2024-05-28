import scrapy
from house_scraper.items import HouseItem

class HouseSpiderSpider(scrapy.Spider):
    name = "house_spider"
    allowed_domains = ["losangeles.craigslist.org"]
    start_urls = ["https://losangeles.craigslist.org/search/apa#search=1~gallery~0~0"]

    def parse(self, response):
        
        all_houses = response.css("li.cl-static-search-result")

        for house in all_houses:
            house_url = house.css("a").attrib["href"]
            yield response.follow(house_url, self.parse_house)

    def parse_house(self, response):
        # Initialize all binary variables to False
        is_available_now = 0
        has_cats_ok = 0
        has_dogs_ok = 0
        has_wd_in_unit = 0
        is_furnished = 0
        has_attached_garage = 0
        no_smoking = 0
        is_wheelchair_accessible = 0
        has_air_conditioning = 0
        has_ev_charging = 0

        # Extract and update binary variables
        if response.xpath('//span[contains(@class, "available-now")]'):
            is_available_now = 1
        
        if response.xpath('//div[@class="attr pets_cat"]/span[@class="valu"]/a[contains(text(), "cats are OK")]'):
            has_cats_ok = 1
        
        if response.xpath('//div[@class="attr pets_dog"]/span[@class="valu"]/a[contains(text(), "dogs are OK")]'):
            has_dogs_ok = 1
        
        if response.xpath('//div[@class="attr"]/span[@class="valu"]/a[contains(text(), "w/d in unit")]'):
            has_wd_in_unit = 1
        
        if response.xpath('//div[@class="attr is_furnished"]/span[@class="valu"]/a[contains(text(), "furnished")]'):
            is_furnished = 1
        
        if response.xpath('//div[@class="attr"]/span[@class="valu"]/a[contains(text(), "attached garage")]'):
            has_attached_garage = 1
        
        if response.xpath('//div[@class="attr no_smoking"]/span[@class="valu"]/a[contains(text(), "no smoking")]'):
            no_smoking = 1
        
        if response.xpath('//div[@class="attr wheelchaccess"]/span[@class="valu"]/a[contains(text(), "wheelchair accessible")]'):
            is_wheelchair_accessible = 1
        
        if response.xpath('//div[@class="attr airconditioning"]/span[@class="valu"]/a[contains(text(), "air conditioning")]'):
            has_air_conditioning = 1
        
        if response.xpath('//div[@class="attr ev_charging"]/span[@class="valu"]/a[contains(text(), "EV charging")]'):
            has_ev_charging = 1

        # deal with the attr important tags
        if len(response.xpath('//span[@class="attr important"]')) == 0:
            br_ba = None
            ft = None
            available_till = None

        elif len(response.xpath('//span[@class="attr important"]')) == 1:
            br_ba = response.xpath('//span[@class="attr important"]/text()').get().strip()
            ft = None
            available_till = None
        
        elif len(response.xpath('//span[@class="attr important"]')) == 2:
            br_ba = response.xpath('//span[@class="attr important"]/text()').get().strip()
            ft = response.xpath('//span[@class="attr important"]/text()')[1].get().strip()
            available_till = None
        
        elif len(response.xpath('//span[@class="attr important"]')) == 3:
            br_ba = response.xpath('//span[@class="attr important"]/text()').get().strip()
            ft = response.xpath('//span[@class="attr important"]/text()')[1].get().strip()
            available_till = response.xpath('//span[@class="attr important"]/text()')[2].get().strip()

        house_item  = HouseItem()

        house_item["url"] = response.url
        house_item["title"] = response.xpath('//span[@id="titletextonly"]/text()').get()
        house_item["price"] = response.css("span.price::text").get()
        house_item["location"] = response.css("h2.street-address::text").get()
        house_item["location_tag"] = response.css("h1.postingtitle span")[-1].get()
        house_item["google_maps_url"] = response.css("p.mapaddress a").attrib.get("href")
        house_item["br_ba"] = br_ba
        house_item["ft"] = ft
        house_item["available_till"] = available_till
        house_item["cover_img"] = response.xpath('//*[@class="slide first visible"]//img').attrib.get("src")
        house_item["posting_id"] = response.css(".postinginfos p.postinginfo ::text")[0].get().split(": ")[-1]
        house_item["posting_date"] = response.css(".postinginfos .date")[0].attrib.get("datetime")
        house_item["is_available_now"] = is_available_now
        house_item["has_cats_ok"] = has_cats_ok
        house_item["has_dogs_ok"] = has_dogs_ok
        house_item["has_wd_in_unit"] = has_wd_in_unit
        house_item["is_furnished"] = is_furnished
        house_item["has_attached_garage"] = has_attached_garage
        house_item["no_smoking"] = no_smoking
        house_item["is_wheelchair_accessible"] = is_wheelchair_accessible
        house_item["has_air_conditioning"] = has_air_conditioning
        house_item["has_ev_charging"] = has_ev_charging

        yield house_item