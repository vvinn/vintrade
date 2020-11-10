from selenium import webdriver

def getQuote(driver, symbol):
#    chromdriver = "C:\\Users\\vinay.yadav\\Downloads\\chromedriver"
#    driver = webdriver.Chrome(chromdriver)
   # driver.get("https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=tcs")
    url = "https://www.google.com/search?q=" + symbol + "+stock"
    driver.get(url)
    
    try:
        sym = driver.find_element_by_xpath('//*[@id="knowledge-finance-wholepage__entity-summary"]/div/g-card-section/div/g-card-section/div[1]/div/div[2]')
    except:
        return None
        
    name = driver.find_element_by_xpath('//*[@id="knowledge-finance-wholepage__entity-summary"]/div/g-card-section/div/g-card-section/div[1]/div/div[1]')
    price = driver.find_element_by_xpath('//*[@id="knowledge-finance-wholepage__entity-summary"]/div/g-card-section/div/g-card-section/span[1]/span/span[1]')
    
    s = sym.text
    n = name.text
    p = price.text
    
    return {
        "symbol": s,
        "name": n,
        "price": float(p.replace(',', ''))
    }
	
if __name__ == "__main__":
    print(getQuote("maruti"))