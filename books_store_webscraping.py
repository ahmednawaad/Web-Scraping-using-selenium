#!/usr/bin/env python
# coding: utf-8

# # Ahmed Nabil Awaad

# ## web scraping
# ### http://books.toscrape.com/

# In[1]:


#importing useful libraries
from selenium import webdriver
import time
import re
import pandas as pd
#cteate instance from webdtiver
webdriver_path = r"D:\webdriver\chromedriver.exe"
driver = webdriver.Chrome(webdriver_path)


# In[2]:


def getstars(stars):
    if stars.split()[1] == "One":
        return 1
    elif stars.split()[1] == "Two":
        return 2
    elif stars.split()[1] == "Three":
        return 3
    elif stars.split()[1] == "Four":
        return 4
    elif stars.split()[1] == "Five":
        return 5
    
def getbookslinks(link):
    #open the page
    driver.get(link)
    #searching for books' links
    links = driver.find_elements_by_xpath('''//h3/a''')
    #extracting links
    links_list =[]
    for link in links:
        temp = link.get_attribute("href")
        links_list.append(temp)
    return links_list
    
def getbook(link):
    #open the book link
    driver.get(link)
    #get data of book
    title = driver.find_element_by_xpath('''//div[@class="col-sm-6 product_main"]/h1''')
    category = driver.find_element_by_xpath('''//ul/li[3]''')
    price = driver.find_element_by_xpath('''//div[@class="col-sm-6 product_main"]/p[@class="price_color"]''')
    stock = driver.find_element_by_xpath('''//div[@class="col-sm-6 product_main"]/p[2]''')
    stars = driver.find_element_by_xpath('''//div[@class="col-sm-6 product_main"]/p[3]''').get_attribute("class")
    discription = driver.find_element_by_xpath('''//article/p''')
    UPC = driver.find_element_by_xpath('''//tr[1]/td''')
    Tax = driver.find_element_by_xpath('''//tr[5]/td''')
    Number_of_reviews = driver.find_element_by_xpath('''//tr[7]/td''')
    img_link = driver.find_element_by_xpath('''//img''').get_attribute("src")
    #put data in dic
    book = {"Title": title.text ,        "Type" : category.text ,       "Price £" : float(price.text.strip("£")) ,        "Tax £" : float(Tax.text.strip("£")) ,        "Stars" : getstars(stars) ,        "Stock" : int(re.findall("\d+",stock.text)[0]) ,        "No. of reviews": int(Number_of_reviews.text) ,        "UBC" : UPC.text,        "Discription" : discription.text ,        "Image" : img_link 
       }
    return book
    


# In[3]:


next_ = "http://books.toscrape.com/"
books =[]
count = 1
for _ in range(50):
    books_links = getbookslinks(next_)
    for link in books_links:
        book = getbook(link)
        books.append(book)
        print(f"Writing {count} books..")
        count += 1
        
    try:
        driver.get(next_)
        next_ = driver.find_element_by_xpath('''//ul[@class="pager"]/li[@class="next"]/a''').get_property("href")
        print("Next page")
        print(f"{next_}")
        
    except:
        print("breaking")
        break
driver.close()


# In[4]:


#convert data to data frame using pandas
df = pd.DataFrame(books)
df


# In[5]:


#saving data to csv file
df.to_csv("books.csv",index= False)

