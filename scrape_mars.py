from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    ### NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # Retrieve latest elements that contain news information
    lists = soup.find('li', class_='slide')
    title = lists.find('div', class_='content_title')
    news_title = title.find('a').text
    news_p = lists.find('div', class_='article_teaser_body').text

    ### JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # HTML object
    html = browser.html
    # # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # # Retrieve Featured Image
    feature = soup.find('section', class_='centered_text clearfix main_feature primary_media_feature single')
    carousel_item = feature.find('div', class_='carousel_items')
    article = carousel_item.find('article')
    title = article.find('h1', class_='media_feature_title')
    style = article['style']
    url = style.split()[1].split("'")[1]
    featured_image_url='https://www.jpl.nasa.gov' + url

    ### Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    # HTML object
    html = browser.html
    # # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # # Retrieve Weather info
    valid_entry = soup.find('div', class_='tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet has-cards has-content')
    entry_text = valid_entry.find('div', class_='js-tweet-text-container')
    entry_p = entry_text.find('p').text
    hidden_link = entry_text.find('a').text
    mars_weather = entry_p.split(hidden_link)[0]

    ### Mars Facts
    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description', 'Value']
    df = df.set_index('Description')
    # convert to html
    mars_facts = df.to_html()
    # mars_facts = BeautifulSoup(html_table, 'html.parser')

    ### Mars Hemispheres (without search url)

    url = 'https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives'
    browser.visit(url)
    # HTML object
    html = browser.html
    # # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # # Retrieve Featured Image
    hemisphere_image_urls=[]
    Hemispheres = soup.select('a[href*="_enhanced"]')
    for item in Hemispheres:
        item_name = item.find('h3').text
        item_name = item_name.split(" Enhanced")[0]

        href = 'https://astrogeology.usgs.gov' + item['href']
    #     Use new html
        browser.visit(href)
        # HTML object
        new_html = browser.html
        # # Parse HTML with Beautiful Soup
        new_soup = BeautifulSoup(new_html, 'html.parser')
        image_link = new_soup.find('div', class_='downloads')
        image_item = image_link.find('li')
        image_href = image_item.find('a')['href']
        hemisphere_image_urls.append({"title":item_name,"img_url":image_href})

    

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image_url":featured_image_url,
        "mars_weather":mars_weather,
        "mars_facts":mars_facts,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
