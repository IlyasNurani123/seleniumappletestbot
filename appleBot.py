from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import time
time.sleep(1)


co = webdriver.ChromeOptions()
GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

co.add_argument("log-level=3")
co.add_argument("--headless")
co.add_argument('--disable-gpu')
co.add_argument('--no-sandbox')
co.binary_location = GOOGLE_CHROME_PATH
# chrome_options = Options()
# chrome_options.add_argument("--dns-prefetch-disable")
def apple_items_add_to_cart_test():
    driver = webdriver.Chrome(executable_path = CHROMEDRIVER_PATH, chrome_options=co)
    driver.get('https://www.apple.com/')
    while True:
      driver.refresh()
      
      if "Apple" in driver.title:   
        break
    driver.find_element_by_xpath('//*[@id="ac-gn-bag"]/div/a').click()
    time.sleep(15)
    driver.find_element_by_xpath('//*[@id="ac-gn-bagview-content"]/nav/ul/li[1]/a').click()
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="bag-content"]/div/div[2]/div/div[1]/div/a').click()
    while True:
      driver.refresh()
      signIn = driver.find_element_by_tag_name('h1')
      if signIn.text == "Please sign in.": 
        break
    apple_id="ilyasnurani1994@gmail.com"
    password="123Ilyas!@#"
    driver.find_element_by_name('appleId').send_keys(apple_id) 
    driver.find_element_by_name('password').send_keys(password) 
    
    driver.find_element_by_id('signInButtonId').click()
    try:
      time.sleep(10)
      driver.find_element_by_xpath('//*[@id="bag-content"]/div/div[2]/div/div/div/a').click()
      time.sleep(10) 
      driver.find_element_by_xpath('/html/body/main/section[3]/div[2]/div/div/a').click()
      time.sleep(10) 
      driver.find_element_by_xpath('//*[@id="section-tiles"]/div/div/div[2]/div[1]/ul/li[2]/a').click()
      time.sleep(10) 
      driver.find_element_by_xpath('//*[@id="page"]/div[7]/div[1]/div/div/div/div[2]/div[1]/a').click()
      time.sleep(10)
      driver.find_element_by_xpath('//*[@id="product-details-form"]/div/div[1]/span/button').click()
      time.sleep(5)
      driver.close()   
    except:
      print("you already add item in cart")
      driver.close()
def get_proxies(co=co):
    driver = webdriver.Chrome()
    apple_items_add_to_cart_test()
    # driver.get("https://www.daraz.com")

    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")

        if result[-1] == "yes":
            PROXIES.append(result[0] + ":" + result[1])

    driver.close()
    return PROXIES
ALL_PROXIES = get_proxies()

def proxy_driver(PROXIES, co=co):
    prox = Proxy()
    pxy = 0
    if PROXIES:
        pxy = PROXIES[-1]
    else:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES = get_proxies()

    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = pxy
    prox.socks_proxy = pxy
    prox.ssl_proxy = pxy

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(options=co, desired_capabilities=capabilities)

    return driver
# --- YOU ONLY NEED TO CARE FROM THIS LINE ---
# creating new driver to use proxy
pd = proxy_driver(ALL_PROXIES)
# code must be in a while loop with a try to keep trying with different proxies
running = True

while running:
    try:
      apple_items_add_to_cart_test()
    except:
        new = ALL_PROXIES.pop()
        # reassign driver if fail to switch proxy
        pd = proxy_driver(ALL_PROXIES)
        print("--- Switched proxy to: %s" % new)
        time.sleep(1)
