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
            CookieToBeWrite = CookieToBeWrite + str(cookie["name"] + "=" + cookie["value"] + ";")
            file.write("'" + CookieToBeWrite + "'")
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
        user_data["id"] = str(response["graphql"]["user"]["id"]) if response["graphql"]["user"]["id"] else None
        user_data["follower"] = str(response["graphql"]["user"]["edge_followed_by"]["count"]) if \
            response["graphql"]["user"]["edge_followed_by"]["count"] else None
        user_data["following"] = str(response["graphql"]["user"]["edge_follow"]["count"]) if \
            response["graphql"]["user"]["edge_follow"]["count"] else None
        user_data["full_name"] = response["graphql"]["user"]["full_name"] if response["graphql"]["user"][
            "full_name"] else None
        return user_data

    def GetFollowerList(self, username,maxId=""):
        detail = self.GetDetail(username)
        if maxId:
            if type(maxId) == int:
                maxId = str(maxId)
            maxId = "&max_id="+maxId


        url = "https://i.instagram.com/api/v1/friendships/" + detail["id"] + "/followers/?count=" + detail[
            "follower"] + "&search_surface=follow_list_page"+ maxId
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

    def GetFollowing(self, username):
        detail = self.GetDetail(username)
        url = "https://i.instagram.com/api/v1/friendships/" + detail["id"] + "/following/?count=" + detail["follower"]
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
            'x-asbd-id': '198387',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR0S0ZnJWbdlZYiVwr68c7kAjq-IjqYIG1tT6RnVVj-H3y_n'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        return response

    def FollowAPersonById(self, id):
        if type(id) == int:
            id = str(id)
        url = "https://www.instagram.com/web/friendships/" + id + "/follow/"

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
        self.AppendFollowedIdToFile(id)
        return response.json()

    def FollowFollowerOfAPersonByUsername(self, username, sleepRangeFrom=15, sleepRangeTo=30):
        follower = self.GetFollowerList(username)
        alreadyFollowedList  = self.getFollowedUserIdAsListByFile()
        def perform(follower):
            if follower["users"]:
                for user in follower["users"]:
                    try:
                        wait = random.randint(sleepRangeFrom, sleepRangeTo)
                        if str(user["pk"]) in alreadyFollowedList:
                            print("skkiing:" +user['username'])
                        else:
                            result = self.FollowAPersonById(user["pk"])
                            if result["status"]:
                                print("Followed : - " + user['username'])
                            else:
                                print("Can not follow this user error may be  : - " + result["result"])
                            print("Waiting For  : - " + str(wait))
                            time.sleep(wait)
                    except:
                        print("Some error Occured :")
            print("Completed Following All Users=  " + str(len(follower['users'])))
        perform(follower)
        next = True
        while next:
            if "next_max_id" in follower:
                follower = self.GetFollowerList(username,follower["next_max_id"])
                perform(follower)
            else:
                next=False
        return True

    def GetAllPendingRequest(self):
        '''Return all pending request users as json()'''

        url = "https://i.instagram.com/api/v1/friendships/pending/"

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
            'x-asbd-id': '198387',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR0S0ZnJWbdlZYiVwr68c7kAjq-IjqYIG1tT6RnVVj-H3y_n'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return  response.json()

    def ApproveAPendingRequestById(self,id):
        id = str(id) if type(id) == int else id
        url = "https://www.instagram.com/web/friendships/"+id+"/approve/"
        payload = {}
        headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-length': '0',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'mid=YlwjhQAEAAH3KUYsTfgUJp6uNkqy; ig_did=9BFD95F3-E704-4B82-A99D-4C4871D5FE57; ig_nrcb=1; csrftoken=ze4wDAmxqF8JmNZHYfPFzKVmpirP9c8X; ds_user_id=32697756216; shbid="10753\\05432697756216\\0541681742621:01f70a5d5a7c20e0a9c162e83e9d7c7593acebd3ddc416f95ee66aefc1a8ff0c49e06b1b"; shbts="1650206621\\05432697756216\\0541681742621:01f787241bfb872cb08c1295fa76a13bdfaf069a0e375ce2642c5943289b3d22b8ab7ebe"; sessionid=32697756216%3AyeHVYIuZMBlsVC%3A23; ig_lang=gu; rur="EAG\\05432697756216\\0541681746735:01f7110ec98eebb7ea0c1753fbb45bc0a745925ef91ac2a099e0af2c0a7f20e12b268714"; csrftoken=ze4wDAmxqF8JmNZHYfPFzKVmpirP9c8X; ds_user_id=32697756216; ig_did=F08DB571-706C-443C-8509-69605EA811B7; mid=Yl02lwAEAAFR8esVB61TEx_o3MF3; rur="NAO\\05432697756216\\0541681842355:01f79094d5e9f8c01f4a9cae5764e29e40e52171f20d4986ea2300702d43b6cec606fc9d"; sessionid=32697756216%3AyeHVYIuZMBlsVC%3A23; shbid="2522\\05416647639862\\0541681841710:01f793600184b55948f8d87a2d3f23a84d05ce0a5bca0eb495991991575cc546dfe3f8c6"; shbts="1650305710\\05416647639862\\0541681841710:01f7c8e6f490af744a3c6bf60b0ca1345dabc8b464385d701cd9d71dfa5bee3bfba93041"',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/sarahy_cast/',
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

    def ApproveAllPendingRequest(self):
        pendingRequest = self.GetAllPendingRequest()
        if pendingRequest["users"]:
            for user in pendingRequest["users"]:
                wait = random.randint(5, 20)
                result = self.ApproveAPendingRequestById(user["pk"])
                print('------------------------------------------------------------------')
                if result["status"]:
                    print("Approved Pending Request of  : - " + user['username'])
                else:
                    print("Can not Approve pending request   : - " + result["result"])
                print("Waiting For  : - " + str(wait))
                print('------------------------------------------------------------------')
                time.sleep(wait)
            print("Approved All Pending Request   " + str(len(pendingRequest['users'])))


    '''Methods for read write operations '''

    def getFollowedUserIdAsListByFile(self):
        userIds = []
        with open("FollowedUserIds.txt") as f:
            userIds = f.read().splitlines()
        return  userIds

    def getFollowedUserUsernameAsListByFile(self):
        username = []
        with open("FollowedUserUsername.txt") as f:
            username = f.read().splitlines()
        return username

    def AppendFollowedIdToFile(self,id):
        file = open('FollowedUserIds.txt','a')
        file.write(id+"\n")
        file.close()
        return  True

    def AppendFollowedUserNameToFile(self,username):
        file = open('FollowedUserUsername.txt','a')
        file.write(username+"\n")
        file.close()
        return  True