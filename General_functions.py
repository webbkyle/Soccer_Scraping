from selenium.common.exceptions import ElementNotVisibleException
import time

#some general webscraping functions

def check_exists_by_css(d, css):
    try:
        d.find_element_by_css_selector(css).click()
    except ElementNotVisibleException:
        return False
    return True

def search_google_query(d, searchString):
    d.get('http://www.google.com')
    body = d.find_element_by_name("q")
    body.send_keys(searchString)
    body.submit()

