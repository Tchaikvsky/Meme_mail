import os
import urllib.request
import praw
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

#loading the environment variables using dotenv
load_dotenv("meme_mail.env")

#Get the environment variables we need 
client_id = os.environ.get("REDDIT_CLIENT_ID")
client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
user_agent = os.environ.get("REDDIT_USER_AGENT")
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")
receiver_address = os.environ.get("RECEIVER_ADDRESS")

#create a PRAW instance
reddit = praw.Reddit( client_id = client_id, client_secret = client_secret, user_agent = user_agent)

#list of valid subreddits from my friends choice and randomly selecting one
subreddits = ['me_irl']
random_subreddit = reddit.subreddit(random.choice(subreddits))


#selects a random post and downloads an image if it's a jpg or png
image_found = False

while image_found == False:
    random_post = random.choice(list(random_subreddit.hot()))
    if random_post.url.endswith('.jpg') or random_post.url.endswith('.png'):
        urllib.request.urlretrieve(random_post.url, "random_image.jpg")
        image_found = True

#create the email
msg = MIMEMultipart()
msg['From'] = email_address
msg['To'] = receiver_address
msg["Subject"] = ("It's memeing taimu")

#mail attachment
with open("random_image.jpg", 'rb') as file:
    img_data = file.read()
    image = MIMEImage(img_data, name="random_image.jpg")
    msg.attach(image)

#To avoid the hastle of authentication, authentication, setting up a smtp server, let's use email sending through mailtrap


os.remove("random_image.jpg")