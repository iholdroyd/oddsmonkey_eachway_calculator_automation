from selenium import webdriver  
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import os
import datetime

USERNAME = #yourusername
PASSWORD = #yourpassword
TIMEDIFFERENCE = 5
CHROMEDRIVER_PATH= #path to your chromedriver. E.g. mine is '/Users/ian/Downloads/chromedriver.

def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

def is_time_in_5(race):
    race = str(race).split(" ")
    racetime= race[1]
    racetime = datetime.datetime.strptime(racetime, '%H:%M')
    timein5 = datetime.datetime.now() + datetime.timedelta(minutes=TIMEDIFFERENCE)
    timein5 = timein5.strftime("%H:%M")
    timein5 = datetime.datetime.strptime(timein5, '%H:%M')
    return racetime <= timein5


#login and navigate to the eachway matcher
options = Options()
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
driver.get('https://www.oddsmonkey.com/Tools/Matchers/EachwayMatcher.aspx')  
driver.find_element_by_name("dnn$ctr433$Login$Login_DNN$txtUsername").send_keys(USERNAME)
driver.find_element_by_name("dnn$ctr433$Login$Login_DNN$txtPassword").send_keys(PASSWORD)
driver.find_element_by_name("dnn$ctr433$Login$Login_DNN$txtPassword").send_keys(Keys.ENTER) 

while True:
    t_end = time.time() + 60 * 10
    while time.time() < t_end:
        time.sleep(5)
        driver.get('https://www.oddsmonkey.com/Tools/Matchers/EachwayMatcher.aspx')  
        #sort by SNR rating
        driver.find_element_by_xpath("/html/body/form/div[3]/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/div[2]/div/table/thead/tr/th[18]/a").click()
        time.sleep(5)

        #select extraplace
        driver.find_element_by_xpath("/html/body/form[1]/div[3]/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/div[1]/div/div/div/div/ul/li[2]/a/span/span/span/span").click()

        #autorefresh every minute
        driver.find_element_by_xpath("/html/body/form[1]/div[3]/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/div[1]/div/div/div/div/ul/li[8]/div/button[2]").click()
        time.sleep(4)
        driver.find_element_by_xpath("/html/body/form[1]/div[3]/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/div[1]/div/div/div/div/ul/li[8]/div/ul/li[1]/a").click()

        while True:
            try:
                race = driver.find_element_by_xpath("/html/body/form/div[3]/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/div[2]/div/table/tbody/tr[1]/td[8]").text
                if is_time_in_5 (race) == False:
                    rating = driver.find_element_by_xpath("/html/body/form/div[3]/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/div[2]/div/table/tbody/tr[1]/td[17]").text
                    odds = driver.find_element_by_xpath("/html/body/form/div[3]/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/div[2]/div/table/tbody/tr[1]/td[13]").text
                    arbrating = driver.find_element_by_xpath("/html/body/form/div[3]/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/div[2]/div/table/tbody/tr[1]/td[19]").text
                    notify(title = "Rating: {}".format(rating), subtitle = "Race: {}".format(race), message  = "Odds: {} Arb Rating : {}".format(odds, arbrating))
                print(race)
            except: 
                Exception
            time.sleep(60)