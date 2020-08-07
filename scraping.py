# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
   # Initiate headless driver for deployment
   browser = Browser("chrome", executable_path="chromedriver", headless=True)

   news_title, news_paragraph = mars_news(browser)
   # Run all scraping functions and store results in dictionary
   data = {
       "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
   }
   # Stop webdriver and return data
   browser.quit()
   return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')    
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

# ### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()


    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

# Hemisphere Image Dictionary

def image_hemisphere(hemisphere: int):
    hemi_dict = {'Cerberus Hemisphere': 'https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg',
        'Schiaparelli Hemisphere': 'https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg',
        'Syrtis Major Hemisphere': 'https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg',
        'Valles Marineris': 'https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'
    }
    hemi_list = ['Cerberus Hemisphere', 'Schiaparelli Hemisphere', 'Syrtis Major Hemisphere', 'Valles Marineris']
    
    return hemi_dict[hemi_list[hemisphere]]

# ## Mars Facts

def mars_facts():

    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    return df.to_html()

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())
