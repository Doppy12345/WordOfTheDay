import requests
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup




#Url and Other Globals
URL = "https://www.merriam-webster.com/word-of-the-day"
Page = requests.get(URL)
wordOfTheDayPage = BeautifulSoup(Page.content, 'html.parser')


class emailLogin:
    def __init__(self,username,password):
        self.username = username
        self.password = password

# phoneCustomers is a list conatining phone numbers of recipiants
# emailCustomers is a list containing emails of recipiants
# alertBotEmail is the email adress (username / pass) that we are using to send these alerts
from secrets import phoneCustomers, emailCustomers, alertBotEmail

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

def send_textAlert(sender, recipiant, subject, body):
    msg = EmailMessage()
    msg.set_content(body) 
    msg['to'] = recipiant
    msg['from'] = sender.username

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender.username, sender.password)
    server.send_message(msg)
    
    server.quit()

def send_emailAlert(sender, recipiant, subject, body):
    msg = EmailMessage()
    msg.set_content(body) 
    msg['subject'] = subject
    msg['to'] = recipiant
    msg['from'] = sender.username

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender.username, sender.password)
    server.send_message(msg)
    
    server.quit()    



def send_WOTD():
    for recipiant in phoneCustomers:
        send_textAlert(alertBotEmail, recipiant, "WOTD", scrapeWOTDP(wordOfTheDayPage)) 

    for recipiant in emailCustomers:    
        send_emailAlert(alertBotEmail, recipiant, "WOTD", scrapeWOTDP(wordOfTheDayPage))



    
   
    
