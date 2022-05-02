# Webscraping
from datetime import time
import time

import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

# Data gathering
import csv


def gatherAddress(file):
    file = open(str(file) + '.csv')
    csvreader = csv.reader(file)
    address = []
    for row in csvreader:
        address.append(
            (row[len(row) - 1] + ' ' + row[len(row) - 2].split(';')[-1]))
    return address[1:]


def searchProperty(driver, address):
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'rsbSearch')))
    search_bar.send_keys(address)
    time.sleep(2)
    search_bar.send_keys(Keys.DOWN)
    search_bar.send_keys(Keys.ENTER)


def gatherData(driver):
    propertyName = driver.find_elements(By.ID, "mainaddresstitle")[0].text
    totalVal = driver.find_elements(By.ID, "lblTotalAssessedValue")[0].text
    landVal = driver.find_elements(By.ID, "lblTotalAssessedLand")[0].text
    buildingVal = driver.find_elements(By.ID, "lblTotalAssessedBuilding")[0].text
    yearBuilt = driver.find_elements(By.ID, "lblYearBuilt")[0].text
    landSize = driver.find_elements(By.ID, "lblLandSize")[0].text
    data = [propertyName, totalVal, landVal, buildingVal, yearBuilt, landSize]

    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'rsbSearch')))
    search_bar.send_keys(Keys.CONTROL + "a")
    search_bar.send_keys(Keys.DELETE)

    return data


def gatherInformation(driver, address):
    searchProperty(driver, address)
    time.sleep(5)
    return gatherData(driver)


def writeDataToCSV(information, f):
    file = f
    with open(file, 'a', encoding='UTF8', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(information)

def writeHeaderToCSV(f):
    file = f
    header = ['Address', 'Total_value', 'Land_value', 'Building_value', 'Year_Built', 'Land_Size']
    with open(file, 'w', encoding='UTF8', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

def runCollection(addresses, index):
    driver = webdriver.Chrome()
    driver.get("https://www.bcassessment.ca/?sp=1&act=")
    driver.maximize_window()

    indexUpdated = index
    try:
        for i in range(index, len(addresses)):
            indexUpdated = i
            if indexUpdated - index == 10:
                driver.close()
                runCollection(addresses, indexUpdated)
            writeDataToCSV(gatherInformation(driver, addresses[i]), 'x.csv')
    except (selenium.common.exceptions.ElementNotInteractableException, selenium.common.exceptions.InvalidSessionIdException, IndexError):
        driver.close()
        runCollection(addresses, indexUpdated + 1)


if __name__ == "__main__":

    def main():
        # Gather address
        addresses = gatherAddress('property-addresses')

        # Gather Information
        runCollection(addresses, 0)

    writeHeaderToCSV('x.csv')
    main()
