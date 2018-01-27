#import dependencies
import time
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    #visit the url
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    #set html as the browser's html to parse with BS
    html = browser.html
    #set the soup object
    soup = bs(html, 'html.parser')
    #find the title/body for the newest item
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    news_date = soup.find("div", class_="list_date").text
    

    #time to navigate and find the featured image url
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    #sleep for 2 sec to let it load
    time.sleep(2)

    #set a new soup object to parse this website
    html = browser.html
    soup = bs(html, "html.parser")
    #set the browser to click the full image button
    browser.find_by_css("div.carousel_container div.carousel_items a.button").first.click()

    #find the image url
    img_url = browser.find_by_css("div.fancybox-inner img")
    img_url = img_url["src"]
    print(img_url)
    #now go to the official twitter page
    twitter_url = "https://mobile.twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)

    #2 sec sleep for load time
    time.sleep(2)
    #new soup object for this site
    html = browser.html
    soup = bs(html, "html.parser")

    #scrape for the newest weather
    tweets = soup.find_all("div", class_="_10YWDZsG")
    #create empty lists to collect tweets
    tweet_list = []
    weather_tweets = []
    #first loop through all the tweets and gather the text
    for tweet in tweets:
        text = tweet.text
        tweet_list.append(text)
    #all weather tweets start with Sol, so if tweet.text starts with Sol append. then get index[0] for the first one 
    for tweet in tweet_list:
        if tweet[0:3] == "Sol":
            weather_tweets.append(tweet)
    #variable for latest weather tweet
    latest_weather_tweet = weather_tweets[0]

    #use pandas to scrape the table
    #set the url
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)

    #make dataframe
    df = tables[0]
    df.columns = ["Description", "Value"]
    df = df.set_index("Description")

    #save table to html
    html_table = df.to_html()
    #clean up the new lines
    html_table = html_table.replace('\n', '')

    #visit website for the 4 hemisphere pictures
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    #sleep counter for load time
    time.sleep(2)
    mars_hemis = []

    #create a for loop to go through all 4 hemispheres
    for i in range(4):
        time.sleep(2)
        image_link = browser.find_by_tag("h3")
        image_link[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        hemi_img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":hemi_img_url}
        mars_hemis.append(dictionary)
    
    completed_dict = {
        "newest_title" : news_title,
        "newest_text" : news_p,
        "newest_date" : news_date,
        "img_url_found" : img_url,
        "latest_weather" : latest_weather_tweet,
        "fact_table" : html_table,
        "mars_hemis" : mars_hemis,
    }
    return completed_dict

