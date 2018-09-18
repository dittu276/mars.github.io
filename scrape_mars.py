from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup 

# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# Function to scrape for weather in Cost Rica
def scrape_mars ():

    # Initialize browser
    browser = init_browser()

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "lxml")
    # find latest news title
    news = soup.find_all('div', class_='content_title')
    latest_news=news[0]
    news_title=latest_news.a.text
    # find latest news paragraph text
    news = soup.find_all('div', class_='article_teaser_body')
    latest_p=news[0]
    news_p=latest_p.text

    # JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    button=soup.find_all('div', class_='carousel_items')
    button_text=button[0].a.text.strip()
    browser.click_link_by_partial_text(button_text)
    browser.click_link_by_partial_text('more info')
    # get html of latest page
    image_html=browser.html
    soup = BeautifulSoup(image_html, 'lxml')
    # pull image_url
    image=soup.find('figure',class_='lede').a
    image_url=image['href']
    featured_image_url='https://www.jpl.nasa.gov'+image_url

    # Mars Weather
    url='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    mars_weather=soup.find('div',class_='js-tweet-text-container').p.text

    # Mars Facts
    import pandas as pd
    url='http://space-facts.com/mars/'
    tables = pd.read_html(url)
    df=tables[0]
    df.columns=['Fact','Value']
    # convert the data to a HTML table string.
    fact_table = df.to_html().replace('\n', '')

    # Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    hemisphere_image_urls=[]
    click_text=soup.find_all('div',class_='description')
    for items in click_text:
        image_links=items.find_all('a')
        text=image_links[0].h3.text
        browser.click_link_by_partial_text(text)
        current_page_html=browser.html
        soup = BeautifulSoup(current_page_html, 'lxml')
        title=soup.find_all('section',class_='block')[0].h2.text
        url=soup.find_all('img',class_='wide-image')[0]
        image_url='https://astrogeology.usgs.gov'+url['src']
        image_dict={}
        image_dict['Title']=title
        image_dict['Image_URL']=image_url
        hemisphere_image_urls.append(image_dict)
        browser.back()

    # Store in dictionary
    mars_mission = {
        "News Title": news_title,
        "News Paragraph": news_p,
        "Featured Image": featured_image_url,
        "Mars Weather": mars_weather,
        "Mars Facts":fact_table,
        "Hemisphere Images": hemisphere_image_urls
    }

    # Return results
    return mars_mission