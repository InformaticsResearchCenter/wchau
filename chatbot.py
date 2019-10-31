from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time


class Chatbot(object):
    def __init__(self, filename):
        self.filename = filename
        self.openDb()

    def openDb(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(self.filename)

    def getData(self, rowname, colname, sheetnum):
        self.dataError = True
        while self.dataError:
            try:
                ambilData = self.sheet.get_worksheet(sheetnum).cell(
                    self.sheet.get_worksheet(sheetnum).find(rowname).row,
                    self.sheet.get_worksheet(sheetnum).find(colname).col).value
                return ambilData
            except Exception as e:
                if str(e).find("RESOURCE_EXHAUSTED"):
                    print("wait ...")
                    time.sleep(100)
                    self.dataError = True

    def saveProfile(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-data-dir=./user_data')
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def splitString(self, string):
        li = list(string.split(" "))
        return li

    def waitLogin(self):
        self.target = '"_3RWII"'
        self.x_arg = '//div[contains(@class, ' + self.target + ')]'
        self.wait = WebDriverWait(self.driver, 600)
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.x_arg)))

    def typeAndSendMessage(self, message):
        self.message_target = self.driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
        self.message_target.send_keys(message)

        self.sendbutton = self.driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
        self.sendbutton.click()

    def searchAndClick(self):
        search = self.driver.find_element_by_tag_name("input")
        sirchsearch = search.get_attribute("title")
        if sirchsearch == "Search or start new chat":
            search.click()
            search.send_keys("sakeudap")

        time.sleep(5)

        target = self.driver.find_elements_by_class_name("_19RFN _1ovWX")[-1]
        target.click()

    def cekAndSendMessage(self):
        try:
            hello = ["maman"]
            mauNonton = ["bioskop", "film", "pilem"]
            namaKota = ["jakarta", "bandung"]
            namaLokasi = ["braga", "btc"]
            namaBioskop = ["xxi"]

            self.chat = self.driver.find_elements_by_class_name("P6z4j")[0]
            self.chat.click()
            self.chat.click()
            self.chat.click()

            time.sleep(0.5)

            self.span = self.driver.find_elements_by_xpath('(.//span)')[-10].text

            self.spanLower = self.span.lower()

            self.makeitsplit = self.splitString(self.spanLower)

            for i in self.makeitsplit:
                if i in hello:
                    self.typeAndSendMessage("iya crot, aya naon?")
                if i in mauNonton:
                    self.typeAndSendMessage("oke sip, ti antosan sakeudap")
                    for j in self.makeitsplit:
                        if j in namaKota:
                            self.namkot = j
                        if j in namaBioskop:
                            self.nambios = j
                        if j in namaLokasi:
                            self.namlok = j

            time.sleep(1)

            self.driver.get("https://jadwalnonton.com/bioskop/di-"+ self.namkot + "/" + self.namlok + "-" + self.nambios + "-" + self.namkot + ".html")

            time.sleep(1)

            self.driver.get("https://web.whatsapp.com/")

            self.waitLogin()

            #komen1

        except Exception as e:
            print(e)
            print("ga ada pesan ...")

    def openBrowser(self):
        self.saveProfile()
        self.driver.get("https://web.whatsapp.com/")
        self.waitLogin()
