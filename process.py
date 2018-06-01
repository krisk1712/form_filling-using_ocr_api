#!/usr/bin/python

# Usage: process.py <input file> <output file> [-l <Language>] [-pdf|-txt|-rtf|-docx|-xml]

import argparse
import os
import time

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


def create_parser():
	parser = argparse.ArgumentParser(description="Recognize a file via web service")
	parser.add_argument('source_file')
	parser.add_argument('target_file')

	parser.add_argument('-l', '--language', default='English', help='Recognition language (default: %(default)s)')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-txt', action='store_const', const='txt', dest='format', default='txt')
	group.add_argument('-pdf', action='store_const', const='pdfSearchable', dest='format')
	group.add_argument('-rtf', action='store_const', const='rtf', dest='format')
	group.add_argument('-docx', action='store_const', const='docx', dest='format')
	group.add_argument('-xml', action='store_const', const='xml', dest='format')

	return parser


def main():
	global processor

	#------------------------------------ GLOBAL -----------------------------------------------------#
	browser = Browser('firefox')
	url = "https://goo.gl/gTWejF"
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
		print text


		
if __name__ == "__main__":
    main()
