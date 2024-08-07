import SharedMethods
from Person import *
from models import *
import requests
from lxml import html

webdriverPath = "/home/mr124/Documents/Projects/SMIF/geckodriver"
profilePath =  "/home/mr124/Documents/Projects/SMIF/WhatsAppProfile"

logger = SharedMethods.logSetup.log("Twitter","log.txt")


class Twitter(Person):
	def __init__(self, name=None, dateOfBirth=None, phoneNumber=None, nickName=None, username=None, apiFilePath=None, apiPass=None):
		super().__init__(name, dateOfBirth, phoneNumber, nickName, username)
		self.logger = logger
		self.apiPass = apiPass
		self.apiFilePath = apiFilePath

	def loadApiTokens(self):
		'''
			Args: None
			Retursn: None
			just it load the api tokesn from encrypted file
		'''
		if self.apiFilePath and self.apiPass:
			encryptedData = SharedMethods.Encrypt(password=self.apiPass,filePath=self.apiFilePath)
			try:
				encryptedData.loadData()
				self.apiToken = encryptedData.data
			except Exception as e:
				self.logger.error("Error in loading the api tokens")
		else:
			self.logger.error("No ApiFilePath or Pass")
			return None
		
	
	def checkIfProtectedAcc(self):
		'''

		'''
		print(self.apiToken)


	# No API section  - Rate LIMIT MY ASS
	def NoAPICheckIfProtectedAcc(self):
		if not self.username:
			self.logger.error("No username to check for")
			return
			
		textToSearchFor="This account's tweets are protected."
		xpath = '/html/body/div/div/div[3]/div/h2'
		url = f"https://xcancel.com/{self.username}"
		
		try:
			response= requests.get(url)
			tree = html.fromstring(response.content)
			elements = tree.xpath(xpath)
			print(response.status_code)
			print(elements[0].text)
			if elements and elements[0].text == textToSearchFor:
				return True
			else:
				return False

		except Exception as e:
			self.logger.error("Error while getting the infos")
			self.logger.error(e)
		
	def fetch_user_by_screen_name(screen_name):
		# URL with a placeholder for the screen_name
		url = f'https://api.x.com/graphql/Yka-W8dz7RaEuQNkroPkYw/UserByScreenName?variables=%7b%22screen_name%22%3a%22{screen_name}%22%2c%22withSafetyModeUserFields%22%3atrue%7d&features=%7B%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue%2C%22subscriptions_feature_can_gift_premium%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D'
		
		headers = {
			'Host': 'api.x.com',
			'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
			'X-Twitter-Client-Language': 'en',
			'Accept-Language': 'en-US',
			'Sec-Ch-Ua-Mobile': '?0',
			'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36',
			'Content-Type': 'application/json',
			'X-Client-Transaction-Id': 'KsNzaQka9TRCEjYpKo+hh9FeMvjUbUcR1nmD36JWKF3gHDKjDRO9TeVz5wky2DEMvm5WTigGpQajzvpjLseG9D9lerR4KQ',
			'X-Guest-Token': '1821287470442451068',
			'X-Twitter-Active-User': 'yes',
			'Sec-Ch-Ua-Platform': '"Linux"',
			'Accept': '*/*',
			'Origin': 'https://x.com',
			'Sec-Fetch-Site': 'same-site',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Dest': 'empty',
			'Referer': 'https://x.com/',
			'Accept-Encoding': 'gzip, deflate, br',
			'Priority': 'u=1, i'
		}
		
		response = requests.get(url, headers=headers)
		
		print(response.text)

if __name__ == '__main__':
	print('hello') 
	#x = SharedMethods.BaseClass.CreatWebDriver(DriverPath=webdriverPath,profilePath=profilePath)
	logger.info("Hello First Test")
	user=input("Enter UserName: ")
	x = Twitter(username=user)
	result = x.NoAPICheckIfProtectedAcc()
	print(result)
	if result:
		print("Acc is Protected... x_x")
	else:
		print("Acc is Public.... ^_^")
