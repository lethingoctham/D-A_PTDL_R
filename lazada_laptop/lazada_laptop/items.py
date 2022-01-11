# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LazadaLaptopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Ảnh sản phẩm
    image = scrapy.Field()
    #Tên sản phẩm
    p_name = scrapy.Field()
    #Giá sản phẩm
    price = scrapy.Field()
    #Thương hiệu sản phảm
    brand = scrapy.Field()
    #Tên nhà bán hàng
    s_name = scrapy.Field()
    # Tỉ lệ đánh giá tích cực 
    p_rating = scrapy.Field()
    # Tỉ lệ phản hồi
    response_rate = scrapy.Field()
    # Tổng số lượng đánh giá
    total_reviews = scrapy.Field()
    # Tỉ lệ giao hàng đúng hạn
    delivered_on_time = scrapy.Field()
    # Thời gian giao hàng
    delivery_time = scrapy.Field()
    # Phí vận chuyển
    shipping_fee =scrapy.Field()
    # Giá gốc sản phẩm
    original_price = scrapy.Field()
    # Tỉ lệ giảm giá
    discount_price = scrapy.Field()

   