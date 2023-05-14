import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

# specify the base url of the website
base_url = "https://kaboompics.com/gallery?page="

# loop through pages 1 to 390
for page in range(1, 391):

    # specify the url of the website for the current page
    url = base_url + str(page)

    # send a GET request to the url
    response = requests.get(url)

    # create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all the img tags in the HTML content
    img_tags = soup.find_all('img')

    # create a list to store the image URLs
    img_urls = []

    # iterate through each img tag and extract the data-srcset attribute
    for img in img_tags:
        img_srcset = img.get('data-srcset')
        if img_srcset:
            # extract the first URL link from the srcset attribute
            img_url = img_srcset.split(',')[1].split()[0]
            # if the img URL is relative, make it absolute using urljoin
            if not img_url.startswith('http'):
                img_url = urljoin(url, img_url)
            img_urls.append(img_url)

    # download the images from their respective URLs
    for img_url in img_urls:
        response = requests.get(img_url)
        filename = os.path.join("C:/Users/georg/Desktop/Other/AI Project/Images/", img_url.split("/")[-1])
        with open(filename, 'wb') as f:
            f.write(response.content)