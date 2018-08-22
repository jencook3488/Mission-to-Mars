from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pymongo
from splinter import Browser
import tweepy
import time
import pandas as pd

driver = webdriver.Chrome()

def scraped():
    finished_data = {}
    finished_data["mars_news"] = mars_news()
    finished_data["mars_image"] = mars_img()
    finished_data["mars_weather"] = mars_weather()
    finished_data["mars_facts"] = mars_facts()
    finished_data["mars_hemisphere"] = mars_hemisphere()
    
    return finished_data

def mars_news():
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    html = requests.get(news_url)  
    soup = BeautifulSoup(html.text, 'html.parser')
    news_title = soup.find('div', 'content_title').text

    news_body = soup.find("div", "article_teaser_body").text

    return {news_title: news_body}

def mars_img():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    driver = webdriver.Chrome()
    driver.get(image_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find("a", class_ = "button fancybox")
    mars_image_url = image_url + images.get('data-fancybox-href')
    return mars_image_url

def mars_weather():
    weather_url = "https://twitter.com/marswxreport?lang=en"
    driver = webdriver.Chrome()
    driver.get(weather_url)
    tweets = driver.find_elements_by_class_name("js-tweet-text-container")
    tweets = [x.text for x in tweets]
    return tweets

def mars_facts():
    facts_url = "https://space-facts.com/mars/"
    facts = pd.read_html(facts_url)[0]
    return facts

def mars_hemisphere():
    driver = webdriver.Chrome()
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    driver.get(hemisphere_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_img_urls = []
    pictures = soup.find("div", "result-list")
    hemispheres = pictures.find_all("div", "item")


    for hemisphere in hemispheres:
            title = hemisphere.find("h3").text
            title = title.replace(" Enhanced", "")
            end = hemisphere.find("a")["href"]
            image_url = "https://astrogeology.usgs.gov/" + end
            hemisphere_img_urls.append({"title": title, "img_url": image_url})

    return hemisphere_img_urls

