# Import necessary dependancies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# Define scrape function
def scrape():

    # Open chrome browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    # Navigate to webpage
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Wait 5 seconds to allow webpage to load
    time.sleep(5)

    # Parse html with beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Use soup find to scrape https://mars.nasa.gov/news/ for the necessary information
    news_title = soup.find('div', class_='list_text').find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # JPL Mars Space Images - Featured Image
    # Navigate to webpage
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Wait 5 seconds to allow webpage to load
    time.sleep(5)

    # Using splinter click on FULL IMAGE link
    browser.click_link_by_partial_text('FULL IMAGE')

    # Wait 5 seconds to allow webpage to load
    time.sleep(5)

    # Using splinter click on more info link
    browser.click_link_by_partial_text('more info')

    # Wait 5 seconds to allow webpage to load
    time.sleep(5)

    # Using splinter click on image
    browser.click_link_by_partial_href('/spaceimages/')

    # Wait 5 seconds to allow webpage to load
    time.sleep(5)

    # Grab url of webpage containing the image
    featured_image_url = browser.url

    # Mars Weather
    # Navigate to webpage
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Wait 5 seconds to allow webpage to load
    time.sleep(5)

    # Parse web content with beautiful soup
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    # Collect first tweet data
    latest_tweet = soup.find_all("div", class_="js-tweet-text-container")[0]
    # Divide content and pull only tweet text data
    mars_weather = latest_tweet.find("p").get_text().replace("\n","").split("pic.twitter.com")[0]

    # Mars Facts
    # Navigate to webpage
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Wait 5 seconds to allow webpage to load
    time.sleep(5)

    # Using pandas scrape tables from website
    mars_facts_table = pd.read_html(url)

    # Select first table
    mars_facts_df = mars_facts_table[0]
    # Rename columns
    mars_facts_df.columns = ['Attribute', 'Value']
    # Remove ':' from Attribute field
    mars_facts_df['Attribute'] = mars_facts_df['Attribute'].str.replace(':','')

    # Convert data to html
    mars_facts_html = mars_facts_df.to_html(index = False, justify='left')

    # Mars Hemispheres
    # Navigate to webpage
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Wait 5 seconds to allow webpage to load
    time.sleep(5)

    # Create list of hemispheres necessary for loop click
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']

    # Create blank list to store loop results
    hemisphere_image_urls = []

    # loop through each hemisphere and scrape the necessary data into a dictionary
    for hemisphere in hemispheres:
        # Create new dictionary for each hemisphere
        new_dict = {}

        browser.click_link_by_partial_text(hemisphere)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        new_dict['title'] = soup.find('h2', class_='title').text.replace("Enhanced","").strip()
        new_dict["img_url"] = soup.find("div", class_="downloads").find('a')['href']
        hemisphere_image_urls.append(new_dict)
    
        # Navigate back to original page
        browser.back()

    # Close out browser
    browser.quit()

    # Load scrape results into dictionary
    mars_web_data = {
        "mars_news_title": news_title,
        "mars_news_paragraph": news_p,
        "mars_image_url": featured_image_url,
        "mars_weather_tweet": mars_weather,
        "mars_facts": mars_facts_html,
        "mars_hemisphere_data": hemisphere_image_urls
    }

    # Output results
    return mars_web_data