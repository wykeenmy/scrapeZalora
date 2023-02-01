import os
import selenium
from time import sleep
import requests
import shutil
import pandas as pd
import argparse
from pytube import YouTube

from selenium import webdriver
from selenium.webdriver.common.by import By


N = 3
CHROME_DRIVER_PATH = "/Users/wykeen/Downloads/chromedriver_mac64/chromedriver"

parser = argparse.ArgumentParser(description= "Please input driver path")
parser.add_argument('-driverPath', dest='CHROME_DRIVER_PATH', required=True, help="filepath of chromedriver")
parser.add_argument('-n', '--N', help="n of sku to be scraped")

args = parser.parse_args()
N = -1 if args.N is None else int(args.N)
print(N)
CHROME_DRIVER_PATH = args.CHROME_DRIVER_PATH
print(CHROME_DRIVER_PATH)

root_dir = os.curdir
output_dir = os.path.join(root_dir,"Outputs")
source_path = os.path.join(root_dir,"Data/Question 1 Dataset.xlsx")
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.mkdir(output_dir)


df = pd.read_excel(source_path, engine ='openpyxl')

for sku in df["sku"][:N]:


    main_url = "https://www.zalora.com.my/catalog/?q={}".format(sku)
    sku_dir = os.path.join(output_dir,sku)

    if not os.path.exists(sku_dir):
        os.mkdir(sku_dir)
    # url = "https://www.zalora.com.my/cotton-on-the-one-organic-rib-crew-long-sleeves-top-green-3174192.html?catalogType=Search&listId=D744DAAD1D0A6BGS"


    driver = webdriver.Chrome(CHROME_DRIVER_PATH)

    # navigate to main page
    driver.get(main_url)

    # search listing
    try:
        listing = driver.find_element(By.XPATH, "//li[@id='{}']".format(sku))
    except selenium.common.exceptions.NoSuchElementException:

        sleep(5)
        print("wait for 5 seconds...")
        try:
            listing = driver.find_element(By.XPATH, "//li[@id='{}']".format(sku))
        except selenium.common.exceptions.NoSuchElementException:

            print("listing not exist")
            driver.close()
            continue


    # navigate to listing page
    listing.click()

    """
    download images
    """
    # images = driver.find_elements(By.XPATH, "//div[@class='prd-moreImages*']/div/div/ul/li")

    images = driver.find_elements(By.XPATH, "//div[@class='prd-moreImagesListWrapper']/div/ul/li")
    if len(images) == 0:
        print("warning (Image selector not found): kindly fix selector")
    for image in images:

        image_url = image.get_attribute("data-image-product")
        filename = image_url.split("/")[-1]
        filepath = os.path.join(sku_dir,filename)

        r = requests.get(image_url, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            # Open a local file with wb ( write binary ) permission.
            with open(filepath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            print('Image sucessfully Downloaded: ', filename)
        else:
            print('Image Couldn\'t be retreived')



    # check if exist play button(video media)
    try:
        play = driver.find_element(By.ID, "playButton")
        play.click()

        vid = driver.find_element(By.XPATH, "//iframe[@id='videoPlayer']")
        video_link = vid.get_attribute("src")
        print(video_link)

        yt = YouTube(video_link)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
            sku_dir)
    except:
        "no mp4 media for {}".format(sku)
        driver.close()
        continue

    driver.close()