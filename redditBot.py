import praw
import pdb
import re
import urllib
import io
import os
import PIL
from PIL import Image

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Set which subreddit you would like to run the bot on
sub = "pics"
# Set number of posts you want to run the bot on in the hot posts
hot_posts_num = 5

bot_reply1 = "\n\n-------------------- \n \nHere are my top "
bot_reply2 = " possible classifications: "
auto_bot = "---------\n\n^^I ^^am ^^a ^^**Bot**. ^^**Upvote** ^^or ^^**Downvote** ^^to ^^let ^^me ^^know ^^how ^^I ^^did ^^with ^^this ^^classification!"

def get_image_labels():
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        'test1.jpg')
    img = Image.open(file_name)

    file_size = os.stat('test1.jpg').st_size
    file_size = file_size*0.000001
    print "File size:", file_size, "MB"

    if file_size > 4:
        print "Inside file_size>4 if statement"
        basewidth = 1000
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        img.save('test1.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    output = []

    print('Labels:')
    for label in labels:
        print label.description
        output.append(label.description)

    return output


# urllib.urlretrieve("http://www.digimouth.com/news/media/2011/09/google-logo.jpg", "local-filename.jpg")

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit(sub)

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

for submission in subreddit.hot(limit=hot_posts_num):
    print "Title:", submission.title

    if submission.id not in posts_replied_to:
        if ".jpg" in submission.url or ".png" in submission.url:
            urllib.urlretrieve(submission.url, "test1.jpg")
            output = get_image_labels()
            lengthOfList = len(output)

            all_labels = ""
            i = 0
            for label in output:
                if i == 0:
                    all_labels = ""+label
                    i = 1
                else:
                    all_labels = all_labels + ", " + label

            print "Bot replying to : ", submission.title
            print "Classification:", output[0], ", ", output[1]
            submission.reply("This image is probably a " + output[0] + " and/or " + output[1] +
                             "." + bot_reply1 + str(lengthOfList) + bot_reply2 + all_labels + "\n\n" + auto_bot)
            print "adding", submission.id, " to replied to list"
            posts_replied_to.append(submission.id)

with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
