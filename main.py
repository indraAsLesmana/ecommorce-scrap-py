import requests
from bs4 import BeautifulSoup
from dbconnection import DBConnection


def scrape_website_and_insert_data():
    # Create a DBConnection instance
    db_connection = DBConnection()

    # Define the URL to scrape
    url = "https://www.jakartanotebook.com"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
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

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def search_product(search_key):
    # Define the base URL
    base_url = "https://www.jakartanotebook.com"
    # Construct the URL with the search key
    url = f"{base_url}/search?key={search_key}"
    print(url)
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            product_items = soup.find_all('div', class_='product-list')
            product_list = []

            # Iterate through each product item and extract information
            for product in product_items:
                product_data = {}

                # Extract product URL
                product_url = product.find('a', class_='product-list__title')
                if product_url:
                    product_data['url'] = product_url['href']

                # Extract product image URL
                product_image = product.find('img', alt='Product Image')
                if product_image:
                    product_data['img'] = product_image['src']

                # Extract product price (coret and regular price)
                price_coret = product.find('span', class_='product-list__price--coret')
                price_regular = product.find('span', class_='product-list__price')
                if price_coret:
                    product_data['price-coret'] = price_coret.get_text()
                if price_regular:
                    product_data['price'] = price_regular.get_text()

                # Extract product name
                product_name = product.find('a', class_='product-list__title')
                if product_name:
                    product_data['name'] = product_name.get_text().strip()

                # Add the product data to the list
                product_list.append(product_data)

            # Print the list of product JSON objects
            for product in product_list:
                print(product)

            return product_list

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main():
    # Call the function to scrape the website and insert data
    # scrape_website_and_insert_data()


    # Optionally, retrieve and display data from the database here if needed
    # db_connection = DBConnection()
    # products = db_connection.get_all_products()

    # if products:
    #     print("Products:")
    #     for product in products:
    #         print(f"Title: {product['title']}")
    #         print(f"Image URL: {product['image_url']}")
    #         print()
    # to test
    search_product("samsung")
    # or using curl
    # curl -u indra:indra 'http://localhost:5000/api/search?key=samsung'


if __name__ == '__main__':
    main()
