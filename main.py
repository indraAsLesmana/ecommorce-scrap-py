import requests
from bs4 import BeautifulSoup
from dbconnection import DBConnection

db_connection = DBConnection()

url = "https://www.jakartanotebook.com"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    ul_element = soup.find('ul', class_='home__brand')

    if ul_element:
        li_elements = ul_element.find_all('li')

        for li in li_elements:
            a_element = li.find('a')
            if a_element:
                title = a_element.get('title')
                img_element = a_element.find('img')
                if img_element:
                    img_src = img_element.get('src')
                    print(f"Title: {title}")
                    print(f"Image URL: {img_src}")

                    # Insert the product into the database
                    db_connection.insert_product(title, img_src)
    else:
        print("Element with class 'home__brand' not found.")
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
