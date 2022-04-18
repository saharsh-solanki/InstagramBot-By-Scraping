import random
import time
from selenium.webdriver.common.by import By
import pickle
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests


class NotLoginException(Exception):
    def __int__(self, message):
        return super().__init__(message)


class InvalidDetailsException(Exception):
    def __int__(self, message):
        return super().__init__(message)


class InitiateBot:
    '''
        Use this class to get the cookies of account or if you another method or cookie there is another method available you can use that
    '''

    def __init__(self, username=None, password=None):
        if not username and password:
            raise NotLoginException("Please Provide Username or Password To Generate Cookie")
        self.username = username
        self.password = password
        self.instagram_page_url = "https://www.instagram.com/accounts/login/"
        self.cookie = False
        self.cookie_data = None

    def InitiateDriver(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = driver
        return driver

    def GotoInstagramLoginPage(self):
        self.driver.get(self.instagram_page_url)

    def PerformLogin(self):
        self.InitiateDriver()
        self.GotoInstagramLoginPage()
        ''' Not Perfrom Login Operation '''
        self.waitAndEnterText("//input[@name='username']", self.username)
        self.waitAndEnterText("//input[@name='password']", self.password)
        self.clickButton("//div[text()='Log In']/../../button")

        if self.CheckPageContainsOrNot("//p[@id='slfErrorAlert']"):
            raise InvalidDetailsException("Your Username and Password is incorrect")

        if self.CheckPageContainsOrNot("//button[text()='Save information']"):
            self.clickButton("//button[text()='Not now']")

        self.GenerateCookieFile()
        self.CloseBrowser()

    def CloseBrowser(self):
        self.driver.quit()

    def GenerateCookieFile(self):
        cookies = self.driver.get_cookies()
        CookieToBeWrite = ""
        file = open("cookies.txt", "w")
        for cookie in cookies:
            CookieToBeWrite =  CookieToBeWrite + str(cookie["name"] + "=" + cookie["value"] + ";")
            file.write("'"+CookieToBeWrite+"'")
        file.close()
        self.cookie = True
        print("Cookie Generated Successfully")

    def setAndCheckCookie(self):
        files = open("cookies.txt", "r")
        cookie = files.read()
        if cookie:
            self.cookie_data = cookie
            return True
        else:
            return False

    def GetCookie(self):
        files = open("cookies.txt", "r")
        cookie = files.read()
        return cookie

    def waitAndEnterText(self, xpath, text):
        ''' Methods  that we use again again  '''
        time.sleep(5)
        field = self.driver.find_element_by_xpath(xpath)
        field.send_keys(text)
        time.sleep(3)

    def clickButton(self, xpath):
        ''' Methods  that we use again again  '''
        field = self.driver.find_element_by_xpath(xpath)
        field.click()
        time.sleep(5)

    def CheckPageContainsOrNot(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except:
            return False

    '''Method for geting follower or extra details perfromation'''

    def GetIdByUsername(self, username):
        url = "https://www.instagram.com/" + username + "/?__a=1"
        payload = {}
        headers = {
            'Cookie': self.cookie_data
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()["graphql"]["user"]["id"]

    def GetDetail(self, username):
        url = "https://www.instagram.com/" + username + "/?__a=1"
        payload = {}
        headers = {
            'Cookie': self.cookie_data
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        user_data = {}
        user_data["id"] =  str(response["graphql"]["user"]["id"]) if response["graphql"]["user"]["id"] else None
        user_data["follower"] = str(response["graphql"]["user"]["edge_followed_by"]["count"]) if \
            response["graphql"]["user"]["edge_followed_by"]["count"] else None
        user_data["following"] = str(response["graphql"]["user"]["edge_follow"]["count"]) if \
            response["graphql"]["user"]["edge_follow"]["count"] else None
        user_data["full_name"] = response["graphql"]["user"]["full_name"] if response["graphql"]["user"][
            "full_name"] else None
        return user_data

    def GetFollowerList(self, username):
        detail = self.GetDetail(username)
        url = "https://i.instagram.com/api/v1/friendships/" + detail["id"] + "/followers/?count="+detail["follower"]+"&search_surface=follow_list_page"
        payload = {}
        headers = {
            'authority': 'i.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': self.cookie_data,
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR0S0ZnJWbdlZYiVwr68c7kAjq-IjqYIG1tT6RnVVj-H37rx'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()

        return response

    def GetFollowing(self,username):
        detail = self.GetDetail(username)
        url = "https://i.instagram.com/api/v1/friendships/" + detail["id"] + "/following/?count=" + detail["follower"]
        payload = {}
        headers = {
            'authority': 'i.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie':self.cookie_data,
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'x-asbd-id': '198387',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR0S0ZnJWbdlZYiVwr68c7kAjq-IjqYIG1tT6RnVVj-H3y_n'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        return  response

    def FollowAPersonById(self,id):
        if type(id) == int:
            id=str(id)
        url = "https://www.instagram.com/web/friendships/"+id+"/follow/"

        payload = {}

        headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-length': '0',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': self.cookie_data,
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'x-asbd-id': '198387',
            'x-csrftoken': 'ze4wDAmxqF8JmNZHYfPFzKVmpirP9c8X',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR0S0ZnJWbdlZYiVwr68c7kAjq-IjqYIG1tT6RnVVj-H3y_n',
            'x-instagram-ajax': '2cd27df1ee26',
            'x-requested-with': 'XMLHttpRequest'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return  response.json()

    def FollowFollowerOfAPersonByUsername(self,username,sleepRangeFrom=20,sleepRangeTo=50):
        follower = self.GetFollowerList(username)
        if follower["users"]:
            for user in follower["users"]:
                wait = random.randint(sleepRangeFrom,sleepRangeTo)
                result = self.FollowAPersonById(user["pk"])
                if result["status"]:
                    print("Followed : - " + user['username'])
                else:
                    print("Can not follow this user error may be  : - " + result["result"])
                print("Waiting For  : - " + str(wait))
                time.sleep(wait)
            print("Completed Following All Users=  "+str(follower.count()))
        return True