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
load_dotenv()

#Get the environment variables we need 
client_id = os.environ.get('REDDIT_CLIENT_ID')
client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
user_agent = os.environ.get('REDDIT_USER_AGENT')
email_address = os.environ.get('EMAIL_ADDRESS')
email_password = os.environ.get('EMAIL_PASSWORD')
receiver_address = os.environ.get('RECEIVER_ADDRESS')

#create a PRAW instance
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

#list of valid subreddits from my friends choice
subreddits = []

#picking a random subreddit
random_subreddit = reddit.subreddit(random.choice(subreddits))


