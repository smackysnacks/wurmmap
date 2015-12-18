#!/usr/bin/env python

import datetime
import Xlib.display
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from imgurpython import ImgurClient

CLIENT_ID = "xxxxxxxxxxxxxxx"
CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
REFRESH_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


def maximize_browser():
    dpy = Xlib.display.Display()
    root = dpy.screen().root
    geometry = root.get_geometry()
    for win in root.query_tree().children:
        win.configure(x=0, y=0,
                      width=geometry.width, height=geometry.height)
    dpy.sync()


def upload_screenshot(path):
    client = ImgurClient(CLIENT_ID, CLIENT_SECRET, None, REFRESH_TOKEN)
    client.upload_from_path(path, anon=False, config={
        'name': path,
        'album': 'Dy947'
    })


display = Display(visible=0, size=(1920, 1080 + 71))
display.start()

try:
    browser = webdriver.Firefox()
    maximize_browser()
    browser.get("http://38.130.218.66/stats/map/")
    zoomin_elem = browser.find_element_by_css_selector("div#zoomin")
    search_elem = browser.find_element_by_css_selector("input#searchbox")
    webdriver.ActionChains(browser).click(zoomin_elem).perform()
    (webdriver.ActionChains(browser)
        .click(search_elem)
        .send_keys("Valhalla")
        .send_keys(Keys.RETURN)
        .perform())
    today = datetime.date.today()
    filename = "%s-%s-%s.png" % (today.year, today.month, today.day)
    browser.save_screenshot(filename)
    browser.quit()
    upload_screenshot(filename)
except Exception as e:
    print "something went wrong: %s" % e
finally:
    display.stop()
