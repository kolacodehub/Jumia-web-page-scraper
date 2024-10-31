import requests
from bs4 import BeautifulSoup as bs
import lxml
from urllib.parse import quote

# url = input('Enter a jumia catalog page: ')
url = 'https://www.jumia.com.ng/catalog/?q=tecno+phones&price_discount=50-100#catalog-listing'
print()
response = requests.get(url)
soup = bs(response.content, 'lxml')
product_name = soup.select('h3', class_='name')
product_name_text = [name.get_text() for name in product_name]
product_prices = soup.select('.info .prc')
product_prices_text = [price.get_text() for price in product_prices]
product_half_link = 'https://www.jumia.com.ng'
product_links = soup.select('.prd > .core')
product_links_text = [plt['href'] for plt in product_links]
product_images = soup.select('img.img')
product_image = [p_i['data-src'] for p_i in product_images]
product_image_links = []
product_info = soup.select('.info')


for i in product_image:
    # Original link
    link = f"{i}"
    # Encode special characters
    encoded_link = quote(link, safe=":/?=&")
    product_image_links.append(encoded_link)

large_dict = {}

for i in range(len(product_image_links)):
    large_dict[product_name_text[i]] = {
        'product-discounted-price': f'{product_prices_text[i]}',
        'product-link': f'{product_half_link}{product_links_text[i]}',
        'product-image': f'{product_image_links[i]}'
    }


with open('Jumia-product-info.txt', mode='w', encoding="utf-8") as file:
    file.write("Yoo! These are the product-names, Discount-price, Link-to-buy, product-image")
    file.write("\n")
    file.write("-----------------------------------------------------------------------------")
    file.write("\n")
    file.write("\n")
    for single_product_name, product_details in large_dict.items():
        file.write(f'Name of product: {single_product_name}\n')
        for key, value in product_details.items():
            file.write(f'{key}: {value}\n')
        file.write("\n")



