# -*- coding: utf-8 -*-

# Usage: process.py <input file> <output file> [-l <Language>] [-pdf|-txt|-rtf|-docx|-xml]
import argparse
import os
import codecs
import time
import sys

from AbbyyOnlineSdk import *

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from splinter import Browser
from PIL import Image
import pytesseract
import splinter
from splinter import Browser
import cv2
import time
import urllib
import re

processor = None


def setup_processor():
    processor.ApplicationId = "TextDetectionPooja"
    processor.Password = "0COpDSY+amGxLjEZPsF0Vo+p"

    # Proxy settings
    if "http_proxy" in os.environ:
        proxy_string = os.environ["http_proxy"]
        print("Using http proxy at {}".format(proxy_string))
        processor.Proxies["http"] = proxy_string

    if "https_proxy" in os.environ:
        proxy_string = os.environ["https_proxy"]
        print("Using https proxy at {}".format(proxy_string))
        processor.Proxies["https"] = proxy_string


# Recognize a file at filePath and save result to resultFilePath
def recognize_file(file_path, result_file_path, language, output_format):
    print("Uploading..")
    settings = ProcessingSettings()
    settings.Language = language
    settings.OutputFormat = output_format
    task = processor.process_image(file_path, settings)
    if task is None:
        print("Error")
        return
    if task.Status == "NotEnoughCredits":
        print("Not enough credits to process the document. Please add more pages to your application's account.")
        return

    print("Id = {}".format(task.Id))
    print("Status = {}".format(task.Status))

    # Wait for the task to be completed
    print("Waiting..")
    # Note: it's recommended that your application waits at least 2 seconds
    # before making the first getTaskStatus request and also between such requests
    # for the same task. Making requests more often will not improve your
    # application performance.
    # Note: if your application queues several files and waits for them
    # it's recommended that you use listFinishedTasks instead (which is described
    # at http://ocrsdk.com/documentation/apireference/listFinishedTasks/).

    while task.is_active():
        time.sleep(5)
        print(".")
        task = processor.get_task_status(task)

    print("Status = {}".format(task.Status))

    if task.Status == "Completed":
        if task.DownloadUrl is not None:
            processor.download_result(task, result_file_path)
            print("Result was written to {}".format(result_file_path))
    else:
        print("Error processing task")


# def create_parser():
#     parser = argparse.ArgumentParser(description="Recognize a file via web service")
#     parser.add_argument('source_file')
#     parser.add_argument('target_file')
#
#     parser.add_argument('-l', '--language', default='English', help='Recognition language (default: %(default)s)')
#     group = parser.add_mutually_exclusive_group()
#     group.add_argument('-txt', action='store_const', const='txt', dest='format', default='txt')
#     group.add_argument('-pdf', action='store_const', const='pdfSearchable', dest='format')
#     group.add_argument('-rtf', action='store_const', const='rtf', dest='format')
#     group.add_argument('-docx', action='store_const', const='docx', dest='format')
#     group.add_argument('-xml', action='store_const', const='xml', dest='format')
#
#     return parser


def main():
    global processor

    # ------------------------------------ GLOBAL -----------------------------------------------------#
    browser = Browser('chrome')
    url = "https://goo.gl/gTWejF"
    browser.visit(url)

    # ------------------------------------------------------- LOGIN -----------------------------------------#

    browser.find_by_id("ctl00_ContentPlaceHolder1_txt_Uname").fill("C31052018437")  # Enter the Users name
    browser.find_by_id("ctl00_ContentPlaceHolder1_txt_pass").fill("daivakripa")  # entering the password
    browser.find_by_id("ctl00_ContentPlaceHolder1_btnsubmit").click()  # submit to login

    # ------------------------------------------------ LOGED IN ----------------------------------------------#

    # ------------------------------------------------- FORM FILLING ------------------------------------------#
    no_box = browser.find_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_drp_pagejump"]/option')
    print "#----------------------START HERE -----------------------------------#"

    tic = time.clock()
    print "#------------------ INFORMATION ON THE PAGE ARE : -----------------#"
    print "THE LENGTH OF THE TOTAL PAGES ARE: "
    print len(no_box)
    id = 0

    while id < 2190 and id >= 0:
        no_box = browser.find_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_drp_pagejump"]/option')

        no_box[id].click()
        time.sleep(1)

        # ------------------------------------------------ PRINTING THE IMAGE URL FOR DOWNLOAD ----------------------------------------------#
        image_url = browser.find_by_id('ctl00_ContentPlaceHolder1_MainImg')['src']

        # ----------------------------------------- SAVING IMAGE VIA URLLIB --------------------------------#
        urllib.urlretrieve(image_url, "locol1.png")
        # -------------------------------------------- IMAGE SAVED AS (loco.png) -----------------------------#

        processor = AbbyyOnlineSdk()

        setup_processor()

        # args = create_parser().parse_args()

        # source_file = args.source_file
        # target_file = args.target_file
        # language = args.language
        # output_format = args.format

        source_file = 'locol1.png'
        target_file = 'result.txt'
        language = 'English'
        output_format = 'txt'

        if os.path.isfile(source_file):
            recognize_file(source_file, target_file, language, output_format)
        else:
            print("No such file: {}".format(source_file))

        with open('result.txt', 'r') as res:
            text = res.readlines()
        # print text
        lin_cnt = text.count("\n")
        print lin_cnt
        a = ''
        num_lines = sum(1 for line in open('result.txt'))
        print num_lines
        if num_lines == 3:
            for k in range(0,num_lines):
                a = a + text[k]
            # a = text[0] + text[1] + text[2]
            b = a.decode('unicode_escape').encode('ascii', 'ignore')
            c = str(b).split("-")
            final = []
            for items in c:
                final.append(re.sub('       ', '', items))
            time.sleep(1)
            print final
            print len(final)
            final1 = []
            for items in final:
                final1.append(re.sub('\n', '', items))
            print final1
            # try:
            print "hi there come to try "
            time.sleep(1)
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_tbc").fill(final1[0])
            time.sleep(1)  # first name
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_name").fill(final1[1])
            time.sleep(1)
            # last name
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_email").fill(final1[2])
            time.sleep(1)  # email
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_mobno").fill(final1[3])
            time.sleep(1)  # mobile number
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_gender").fill(final1[4])
            time.sleep(1)  # gender
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_licenceno").fill(
                final1[5].split('\\')[0])
            time.sleep(1)  # licence number
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_girno").fill(
                final1[6])  # grid number
            time.sleep(1)

            # ------------------------------------------- SECTION ONE END -------------------------------------------#

            # ------------------------------------------- SECTION TWO START (7) -------------------------------------#

              # provider tab click
            time.sleep(1)
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_panno").fill(final1[7])
            time.sleep(1)  # pan number
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_Hadd").fill(final1[8])
            time.sleep(1)  # state
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_Hcity").fill(final1[9])
            time.sleep(1)  # city
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_Hpin").fill(final1[10])
            time.sleep(1)  # pin
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_HState").fill(final1[11])
            time.sleep(1)  # address
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_Oadd").fill(final1[12])
            time.sleep(1)  # address
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_Ocity").fill(
                final1[13])  # city
            time.sleep(1)
            # ------------------------------------------- SECTION TWO END ----------------------------------------------#

            # -------------------------------------------##### SECTION THREE START (6) ----------------------------------#


            time.sleep(1)
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_Opincode").fill(
                final1[14])
            time.sleep(1)  # pincode
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_loanapproval").fill(
                final1[15])
            time.sleep(1)  # loan approval
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_menno").fill(
                final1[16])
            time.sleep(1)  # men number
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_af").fill(final1[17])
            time.sleep(1)  # af
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_nri").fill(
                final1[18])
            time.sleep(1)  # nri
            browser.find_by_id("ctl00_ContentPlaceHolder1_txt_cp").fill(final1[19])
            time.sleep(1)  # cpi
            time.sleep(1)
            # ------------------------------------------------- SECTION THREE END -------------------------------------------#

            # ------------------------------------------------ SUBMISION ON END -------------------------------------------#

            browser.find_by_id("ctl00_ContentPlaceHolder1_btnsubmit").click()  # submit
            toc = time.clock()
            a = tic - toc
            print
            print ("THE TIME TAKEN TO COMPLETE THE FORM IS : ")
            print(a)
            print "#------------------------ PAGE COMPLETED SUCESSFULL--------------------------#"
            time.sleep(1)
            # except:
            #     print "#---------------------------- THE ERROR SECTION --------------------------#"
            #
            #     tic = time.clock()
            #     print "Error has occurred"
            #
            #     print "THE ERREOR OCCURED PAGE NUMBER IS ALWYS (n-1):"
            #
            #     print id
            #
            #     print"THE ERROR PAGE WITH THIS LIST SO PLEASE CHECK THIS : "
            #
            #     print final
            #     toc = time.clock()
            #     b = tic - toc
            #     print "THE TIME TAKEN TO GET THE ERROR OUT IS : "
            #
            #     print b
            #
            #     print "#------------------------------ THE EROOR SECTION ENDS HERE --------------------#"
            #     id = id + 1
            #     continue
            id = id + 1
        else:
            id = id + 1
            continue
if __name__ == "__main__":
    main()
