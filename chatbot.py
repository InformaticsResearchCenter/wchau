from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from time import sleep


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
                    sleep(100)
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

    def waitLocation(self):
        self.target = '"_2Wx_5 _3LG3B"'
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

        sleep(5)

        target = self.driver.find_elements_by_class_name("_19RFN _1ovWX")[-1]
        target.click()

    def cekAndSendMessage(self):
        try:
            self.chat = self.driver.find_elements_by_class_name("P6z4j")[0]
            self.chat.click()
            self.chat.click()
            self.chat.click()

            sleep(0.5)

            self.span = self.driver.find_elements_by_xpath('(.//span)')[-11].text

            self.spanLower = self.span.lower()

            self.message = self.splitString(self.spanLower)

            if "bioskop" in self.message:
                self.movieSchedule(self.message)
            if "perhutani" in self.message:
                self.perhutani()

            try:
                cariMaps = self.driver.find_elements_by_class_name("_15Rkh")[-1]
                self.gmaps()
            except Exception as e:
                print(e)

        except Exception as e:
            print("ga ada pesan ...")

    def movieSchedule(self, message):
        hello = ["maman"]
        mauNonton = ["bioskop", "film", "pilem"]
        namaKota = ["jakarta", "bandung"]
        namaLokasi = ["braga", "btc"]
        namaBioskop = ["xxi"]

        for i in message:
            if i in hello:
                self.typeAndSendMessage("iya crot, aya naon?")
            if i in mauNonton:
                self.typeAndSendMessage("oke sip, ti antosan sakeudap")
                for j in message:
                    if j in namaKota:
                        self.namkot = j
                    if j in namaBioskop:
                        self.nambios = j
                    if j in namaLokasi:
                        self.namlok = j

        sleep(1)

        self.driver.execute_script(
            "window.open('https://jadwalnonton.com/bioskop/di-" + self.namkot + '/' + self.namlok + '-' + self.nambios + '-' + self.namkot + ".html');")

        self.driver.switch_to_window(self.driver.window_handles[1])
        try:
            error = self.driver.find_element_by_xpath("//div[contains(@class, 'caution')]").text
            if "404" in error:
                self.driver.close()
                sleep(1)
                self.driver.switch_to_window(self.driver.window_handles[0])
                sleep(1)
                self.typeAndSendMessage("data tidak ditemukan euy")
        except:
            jumlah = self.driver.find_elements_by_xpath("//div[contains(@class, 'col-sm-10 sched_desc')]")
            jadwal = ""
            for i in jumlah:
                jadwal = i.text + jadwal
            self.driver.close()
            sleep(1)
            self.driver.switch_to_window(self.driver.window_handles[0])
            sleep(1)
            jadwalFix = jadwal.replace("LIHAT DI BIOSKOP LAIN", "")
            sleep(1)
            self.typeAndSendMessage(jadwalFix)

    def perhutani(self):
        usEmail = "trianggadio@gmail.com"
        usPass = "isSAME10"

        self.driver.execute_script(
            "window.open('https://www.tokoperhutani.com/beranda/searchFromRecap/4140100/4141100/4141102/010')")
        sleep(.5)

        self.driver.switch_to_window(self.driver.window_handles[1])
        sleep(2)

        self.driver.find_element_by_link_text("Login").click()
        sleep(.5)

        self.driver.find_element_by_id("email").send_keys(usEmail)
        self.driver.find_element_by_id("password").send_keys(usPass)

        self.driver.find_elements_by_class_name("le-button")[0].click()
        sleep(60)

        wekser = ['193150214695', '193150214696', '193150214751', '193150215151', '193150215166', '193150215173',
                  '193150215178', '193150215190', '193150215192', '193150215398', '193150215511', '193150215524',
                  '193150214698', '193150215373']

        cariData = True

        forCounting = []

        self.driver.find_elements_by_class_name("paginate_button")[6].click()

        asd = self.driver.find_elements_by_xpath(
            "//table[@id='example' and @class='display select nowrap dataTable no-footer']/tbody/tr")

        for i in asd:
            abc = i.text[9:22]
            waduwek = abc.splitlines()
            forCounting.append(waduwek)

        itungan = 10 - len(forCounting)

        while cariData:
            asd = self.driver.find_elements_by_xpath(
                "//table[@id='example' and @class='display select nowrap dataTable no-footer']/tbody/tr")

            for i in asd:
                itungan += 1
                abc = i.text[9:22]
                waduwek = abc.splitlines()

                if waduwek[0] in wekser:
                    i.click()
                    wektow = wekser.index(waduwek[0])
                    wekser.pop(wektow)

                if len(wekser) == 0:
                    cariData = False
                    self.driver.find_elements_by_class_name("le-button")[1].click()
                if itungan == 10 and len(wekser) >= 1:
                    print("masih ada belanjaan lanjut")
                    itungan = 0
                    self.driver.find_element_by_id("example_previous").click()

    def gmaps(self):
        self.driver.find_elements_by_class_name("_15Rkh")[-1].click()
        sleep(1)
        self.driver.switch_to_window(self.driver.window_handles[1])
        sleep(1)
        self.destination = "Politeknik Pos Indonesia"
        sleep(1)
        self.abc = self.driver.find_element_by_id("searchboxinput").get_attribute("value")
        sleep(1)
        self.driver.find_element_by_id("sb_cb50").click()
        sleep(1)
        self.driver.find_element_by_id("searchboxinput").send_keys(self.destination + Keys.ENTER)
        sleep(4)
        self.driver.find_elements_by_class_name("iRxY3GoUYUY__taparea")[0].click()
        sleep(1)
        self.driver.find_elements_by_class_name("tactile-searchbox-input")[2].send_keys(self.abc + Keys.ENTER)
        sleep(1)
        currentUrl = self.driver.current_url
        sleep(1)
        self.driver.close()
        sleep(1)
        self.driver.switch_to_window(self.driver.window_handles[0])
        sleep(1)
        self.typeAndSendMessage(currentUrl)
        sleep(1)

    def openBrowser(self):
        self.saveProfile()
        self.driver.get("https://web.whatsapp.com/")
        self.waitLogin()
