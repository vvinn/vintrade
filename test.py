from selenium import webdriver
import requests
import time

if __name__ == "__main__":
    chromdriver = "C:\\Users\\vinay.yadav\\Downloads\\chromedriver"
    driver = webdriver.Chrome(chromdriver)
   # driver.get("https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=tcs")
    driver.get("https://www.google.com/search?q=infy+stock")
    
    element = driver.find_element_by_xpath('//*[@id="knowledge-finance-wholepage__entity-summary"]/div/g-card-section/div/g-card-section/span[1]/span/span[1]')
    t = element.text
    print(t)
    driver.get("https://www.google.com/search?q=tcs+stock")
    element = driver.find_element_by_xpath('//*[@id="knowledge-finance-wholepage__entity-summary"]/div/g-card-section/div/g-card-section/span[1]/span/span[1]')
    t = element.text
    print(t)
    #response = requests.get('https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=tcs')
    #print (response.status_code)
    #print (response.content)
    print("vinay")