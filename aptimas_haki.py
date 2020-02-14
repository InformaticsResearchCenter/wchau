from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep


class aptimas:
    def __init__(self):
        self.jenis_haki = []
        self.judul = []
        self.status = []
        self.post_date = []

    def finding_haki(self):
        user_name = "0410118609"
        password = "lppm.poltekpos.ac.id"
        driver = webdriver.Chrome()
        driver.get("https://www.google.com")
        driver.execute_script("window.open('http://lppm-poltekpos.net/login');")
        driver.switch_to_window(driver.window_handles[1])
        sleep(5)
        print("Opening web")
        element = driver.find_element_by_name("identity").send_keys(user_name)
        element = driver.find_element_by_name("password").send_keys(password)
        element = driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
        print("Login")
        sleep(15)
        element = driver.find_element_by_css_selector(
            "#tim_haki > a:nth-child(1) > span:nth-child(2)"
        ).click()
        sleep(5)
        a = 2
        gerbang = True
        while gerbang:
            try:
                if (
                    driver.find_element_by_xpath(
                        "/html/body/div[2]/div/section[2]/div/div/div/div[2]/form/table/tbody/tr["
                        + str(a)
                        + "]/td[4]"
                    ).text
                    != "Diterima Dirjen"
                ):
                    element1 = driver.find_element_by_xpath(
                        "/html/body/div[2]/div/section[2]/div/div/div/div[2]/form/table/tbody/tr["
                        + str(a)
                        + "]/td[2]"
                    )
                    print("Jenis Haki :", element1.text)
                    self.jenis_haki.append(element1.text)
                    element2 = driver.find_element_by_xpath(
                        "/html/body/div[2]/div/section[2]/div/div/div/div[2]/form/table/tbody/tr["
                        + str(a)
                        + "]/td[3]"
                    )
                    print("Judul :", element2.text)
                    self.judul.append(element2.text)
                    element3 = driver.find_element_by_xpath(
                        "/html/body/div[2]/div/section[2]/div/div/div/div[2]/form/table/tbody/tr["
                        + str(a)
                        + "]/td[4]"
                    )
                    print("Status :", element3.text)
                    self.status.append(element3.text)
                    element4 = driver.find_element_by_xpath(
                        "/html/body/div[2]/div/section[2]/div/div/div/div[2]/form/table/tbody/tr["
                        + str(a)
                        + "]/td[5]"
                    )
                    print("Post Date :", element4.text)
                    self.post_date.append(element4.text)
                    print("====================================================")
                    # wait until
                a += 1

            except:
                driver.quit()
                gerbang = False
            if a == 12:
                try:
                    element = driver.find_element_by_css_selector(
                        '.pagination>li:last-child>a[rel="next"]'
                    ).click()
                    sleep(5)
                    a = 2
                except:
                    driver.close()
                    gerbang = False
                    driver.switch_to_window(driver.window_handles[0])

        print("Done")
        return aptimas


dod = aptimas()
dod.finding_haki()
