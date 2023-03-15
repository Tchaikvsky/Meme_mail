import os
import urllib.request
import praw
import random
from pathlib import Path
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import ssl

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

me_me_image = Path(__file__).parent.joinpath("random_image.jpg").read_bytes()

#create the email
msg = MIMEMultipart()
msg['From'] = email_address
msg['To'] = receiver_address
msg["Subject"] = ("It's me me time")
msg.attach(MIMEText('<img src="cid:image1">', 'html'))

#mail attachment
with open("random_image.jpg", 'rb') as file:
    img_data = file.read()
    image = MIMEImage(img_data, name="random_image.jpg")
    image.add_header('Content-ID', '<image1>')
    msg.attach(image)

#security layer
context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_address, email_password)
    smtp.sendmail(email_address, receiver_address, msg.as_string())

os.remove("random_image.jpg")