import requests
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup

#Url and Other Globals
URL = "https://www.merriam-webster.com/word-of-the-day"
Page = requests.get(URL)
customers = ["7345466552@txt.att.net"]
wordOfTheDayPage = BeautifulSoup(Page.content, 'html.parser')


class emailLogin:
    def __init__(self,username,password):
        self.username = username
        self.password = password

def scrapeWOTDP(page):
    wordOfDay = page.find('h1')
    partOfSpeech = page.find('span', class_ = 'main-attr')
    pronounciation = page.find('span', class_ = 'word-syllables')
    definition = page.find('p')

    output = ("\n" +  "Word: " + (wordOfDay.text).upper() +  "\n" +
            (partOfSpeech.text).capitalize() + " | " + pronounciation.text +  "\n"  
            "Definition" + definition.text
            )
    
    

    return output

def send_message(sender, recipiant, subject, body):
    msg = EmailMessage()
    msg.set_content(body) 
    # msg['subject'] = subject
    msg['to'] = recipiant
    msg['from'] = sender.username

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender.username, sender.password)
    server.send_message(msg)
    
    server.quit()


alertBotEmail = emailLogin("wotd.alerts@gmail.com", "qovlryhgmbqiyeqt")

for recipiant in customers:
    # print(scrapeWOTDP(wordOfTheDayPage))
    send_message(alertBotEmail, recipiant, "WOTD", scrapeWOTDP(wordOfTheDayPage)) 