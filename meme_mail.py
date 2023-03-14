import os
import urllib.request
import praw
import random
import mailtrap as mt
import imghdr
import base64
from pathlib import Path
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
#from email.mime.image import MIMEImage
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
mailtrap_token = os.environ.get("MAILTRAP_TOKEN")

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

#create the email using email.mime *legacy*
"""
msg = MIMEMultipart()
msg['From'] = email_address
msg['To'] = receiver_address
msg["Subject"] = ("It's memeing taimu")
"""

#mail attachment using legacy method
"""
with open("random_image.jpg", 'rb') as file:
    img_data = file.read()
    image = MIMEImage(img_data, name="random_image.jpg")
    msg.attach(image)
"""


#create mail using mailtrap
mail = mt.Mail(
    sender=mt.Address(email=email_address, name="Michael"),
    to=[mt.Address(email=receiver_address)],
    subject="TIME TO MEME IT UP",
    html="""<html>
            <body>
                <h1>Pain.</h1>
                <img src="cid:me_me_image">
            </body>
            </html>""",
    attachments=[
        mt.Attachment(
            content=base64.b64encode(me_me_image),
            filename="random_image.jpg",
            disposition=mt.Disposition.INLINE,
            mimetype="image/jpg",
            content_id="me_me_image",
        )
    ],
)


#To avoid the hastle of authentication, authentication, setting up a smtp server, let's use email sending through mailtrap
client = mt.MailtrapClient(token=mailtrap_token)
client.send(mail)

os.remove("random_image.jpg")