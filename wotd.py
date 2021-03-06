import requests
import smtplib
from datetime import datetime
from twilio.rest import Client
from email.message import EmailMessage
from bs4 import BeautifulSoup


# phoneCustomers is a list conatining phone numbers of recipiants
# emailCustomers is a list containing emails of recipiants
# alertBotEmail is the email adress (username / pass) that we are using to send these alerts
from secrets import phoneCustomers, emailCustomers, alertBotEmail, alertBotPhoneNumber ,auth_token, account_sid

#Url and Other Globals
URL = "https://www.merriam-webster.com/word-of-the-day"
Page = requests.get(URL)
wordOfTheDayPage = BeautifulSoup(Page.content, 'html.parser')
twilioClient = Client(account_sid, auth_token)



def archiveWord(word):
    todaysDate = datetime.today().strftime('%m-%d-%y')
    with open ('PastWord.txt', 'a') as f:
        f.write(todaysDate + " : " + word.capitalize() + "\n")
    f.close()



def scrapeWOTDP(page):

    #Looks at merriam websters word of the day page and retrieves word, defintion, part of speech and pronounciation

    wordOfDay = (page.find('h1')).text
    

    #save this word as an entry in a text file
    archiveWord(wordOfDay)

    partOfSpeech = (page.find('span', class_ = 'main-attr')).text
    pronounciation = (page.find('span', class_ = 'word-syllables')).text
    definitions = ""

    for p in page.select("div.wod-definition-container > p"):
            definitions += (p.text + "\n")
    


    output = ("\n" +  "Word: " + (wordOfDay).upper() +  "\n" +
            (partOfSpeech).capitalize() + " | " + pronounciation +  "\n"  
            "Definition: \n" + definitions
            )
    
    
    return output

def send_textAlert(sender, recipiant, content):

    twilioClient.messages.create(
    to = recipiant,
    from_ = sender,
    body = content)



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
    wotdContent = scrapeWOTDP(wordOfTheDayPage)
    for phone in phoneCustomers:
        send_textAlert(alertBotPhoneNumber,phone, wotdContent)
    for email in emailCustomers:
        send_emailAlert(alertBotEmail,email, "WOTD", wotdContent)

    


    
   
    
