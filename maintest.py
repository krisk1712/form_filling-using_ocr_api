from PIL import Image
import pytesseract
from splinter import Browser
import time
import urllib
import re
#------------------------------------ GLOBAL -----------------------------------------------------#
browser = Browser('chrome')
url = "http://ffwork.in/"
browser.visit(url)


#------------------------------------------------------- LOGIN -----------------------------------------#

browser.find_by_id("ctl00_ContentPlaceHolder1_txt_Uname").fill("C31052018437")     # Enter the Users name
browser.find_by_id("ctl00_ContentPlaceHolder1_txt_pass").fill("daivakripa")             # entering the password
browser.find_by_id("ctl00_ContentPlaceHolder1_btnsubmit").click()                     # submit to login

#------------------------------------------------ LOGED IN ----------------------------------------------#


#------------------------------------------------- FORM FILLING ------------------------------------------#
no_box = browser.find_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_drp_pagejump"]/option')
print "#----------------------START HERE -----------------------------------#"

tic = time.clock()
print "#------------------ INFORMATION ON THE PAGE ARE : -----------------#"
print "THE LENGTH OF THE TOTAL PAGES ARE: "
print len(no_box)

# ------------------------------------------------ PRINTING THE IMAGE URL FOR DOWNLOAD ----------------------------------------------#
image_url = browser.find_by_id('ctl00_ContentPlaceHolder1_MainImg')['src']

# ----------------------------------------- SAVING IMAGE VIA URLLIB --------------------------------#
urllib.urlretrieve(image_url, "locol1.png")
# -------------------------------------------- IMAGE SAVED AS (loco.png) -----------------------------#

# ----------------------------------------- PYTESSRACT OCR -------------------------------------------#
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
text = pytesseract.image_to_string(Image.open('locol1.png'))

# -------------------------------------- TEXT COVERTERD BY THE OCR --------------------------------------#
out = text.split("-")
print "THE LENGTH OF OUT IS AFTER SEP OF - : "
print len(out)
print out