import scrapy
from ..items import LazadaLaptopItem
from selenium import webdriver
from scrapy.utils.project import get_project_settings
import os
from scrapy_selenium import SeleniumRequest
class LazadaspiderSpider(scrapy.Spider):
    name = 'LazadaSpider'
    def start_requests(self):
        number_of_pages = 3         # Số lượng trang sẽ cào ở mỗi danh mục sản phẩm
        number_of_cate = 10         # Số lượng danh mục sản phẩm sẽ cào dữ liệu
        
        path = "C:\\Users\\acer\\lazada_laptop\\lazada_laptop\\lazada_laptop\\spiders"  # Đường dẫn đến thư mục chứa 
        os.chdir(path)
        file = open('url_cate_product.txt', 'r', encoding='UTF-8')  
        data_url_cate = file.readlines()       #  Đọc file  
        file.close()                                   

        # Nếu không test code thì comment dòng này
        #data_url_cate = ['https://www.lazada.vn/dau-nhot-mo-to/']

        url_cate_list = []
        for item in data_url_cate:
            for count_page in range(number_of_pages):
                url = str(item) + "?page=" + str(count_page+1)
                url_cate_list.append(url)

        for item in url_cate_list[:number_of_cate]:
            settings= get_project_settings()
            driver_path = 'C:\\Users\\acer\\lazada_laptop\\lazada_laptop\\chromedriver_win32\\chromedriver.exe'
            options= webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(driver_path, options=options)
            driver.get(item)
            link_elements = driver.find_elements_by_xpath('//*[@data-qa-locator="product-item"]//a[text()]')
            
            for link in link_elements:
                link = link.get_attribute('href')
                file = open('history.txt', 'a+', encoding='UTF-8')
                data = file.read()
                if link not in data:
                    file.write(str(link) + "\n")
                    yield SeleniumRequest(
                        url = link,
                        wait_time = 10,
                        screenshot = True,
                        callback = self.parse,
                        script='window.scrollTo(0, document.body.scrollHeight);',
                        dont_filter = True
                    )
                else:
                    continue
                file.close()
            driver.quit()

    def parse(self, response):
        #<img class="pdp-mod-common-image gallery-preview-panel__image" src="//vn-live-05.slatic.net/p/c5b84771aa2a04eabdaf1122e0fd3da9.jpg_720x720q80.jpg_.webp" alt="Áo hoodie oversize ODIN Acid, áo nỉ dài nay có mũ unisex ODIN">
        image = response.css('.gallery-preview-panel__image').css("::attr(src)").extract()
        #<h1 class="pdp-mod-product-badge-title">Áo hoodie oversize ODIN Acid, áo nỉ dài nay có mũ unisex ODIN</h1>
        p_name= response.xpath('//h1[@class="pdp-mod-product-badge-title"]//text()').get()
        #<span class="pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl">249.000 ₫</span>
        price = response.xpath('//span[@class="pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl"]/text()').getall()
        #<a class="pdp-link pdp-link_size_s pdp-link_theme_blue pdp-product-brand__brand-link" target="_self" href="https://www.lazada.vn/odin-brand/?type=brand">Odin</a>
        brand = response.xpath('//a[@class="pdp-link pdp-link_size_s pdp-link_theme_blue pdp-product-brand__brand-link"]/text()').get()
        #<a class="pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name" target="_self" href="//www.lazada.vn/shop/odin-studio/?itemId=1519369785&amp;channelSource=pdp">ODIN STUDIO</a>
        s_name = response.xpath('//a[@class="pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name"]/text()').get()
        #<div class="seller-info-value rating-positive ">95%</div>
        p_rating = response.xpath('//div[@class="seller-info-value rating-positive "]/text()').get()
        #<div style="color:" class="seller-info-value ">99%</div>
        response_rate = response.xpath('//div[@class="info-content"][3]/div[2]/text()').get()
        #<a class="pdp-link pdp-link_size_s pdp-link_theme_blue pdp-review-summary__link">298 đánh giá</a>
        total_reviews = response.xpath('//a[@class="pdp-link pdp-link_size_s pdp-link_theme_blue pdp-review-summary__link"]/text()').get()
        #<div class="info-content"><div class="seller-info-title">Giao đúng hạn</div><div style="color:" class="seller-info-value ">94%</div></div>
        delivered_on_time = response.xpath('//div[@class="info-content"][2]/div[2]/text()').get()
        #<div class="delivery-option-item__time">3 - 7 ngày</div>
        delivery_time = response.xpath('//div[@class="delivery-option-item__time"]/text()').get()
        #<div class="delivery-option-item__shipping-fee no-subtitle">22.000 ₫</div>
        shipping_fee = response.xpath('//div[@class="delivery-option-item__shipping-fee no-subtitle"]/text()').get()
        #<span class="pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs">300.000 ₫</span>
        original_price = response.xpath('//span[@class="pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs"]/text()').get()
        #<span class="pdp-product-price__discount">-34%</span>
        discount_price = response.xpath('//span[@class="pdp-product-price__discount"]/text()').get()
        
       
        
        item= LazadaLaptopItem()
        item['p_name']=p_name
        item['price']=price
        item['brand']= brand
        item['s_name']=s_name
        item['p_rating']=p_rating
        item['response_rate']= response_rate
        item['image']= image
        item['total_reviews']=total_reviews
        item['delivered_on_time']=delivered_on_time
        item['delivery_time']=delivery_time
        item['shipping_fee']=shipping_fee
        item['original_price']=original_price
        item['discount_price']=discount_price
       
       
        yield item
        pass
        
    