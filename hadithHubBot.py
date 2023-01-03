import io
import os
from PIL import Image, ImageFont, ImageDraw
import textwrap
import tweepy
from subprocess import call

def generateImage():
    my_image = Image.open("HadithBackground.png")

    font = ImageFont.truetype(
        '/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf', 42)
    imageWidth = 1200
    araHadith = '''أَخْبَرَنَا مُحَمَّدُ بْنُ إِسْمَاعِيلَ بْنِ إِبْرَاهِيمَ، عَنْ سَعِيدِ بْنِ عَامِرٍ، عَنْ هَمَّامٍ، عَنِ ابْنِ جُرَيْجٍ، عَنِ الزُّهْرِيِّ، عَنْ أَنَسٍ، أَنَّ رَسُولَ اللَّهِ صلى الله عليه وسلم كَانَ إِذَا دَخَلَ الْخَلاَءَ نَزَعَ خَاتَمَهُ'''
    engHadith = "It was narrated from Anas that:When entering the Khala', the Messenger of Allah [SAW] would take off his ring"
    reference = "Sunan an Nasai 5213"
    gradings = "Al-Albani - Daif&&Abu Ghuddah - Daif&&Bashar Awad Maarouf - Sahih Maqtu&&Zubair Ali Zai - Sahih Lighairihi&&Shuaib Al Arnaut - Sahih"
    gradingList = gradings.split('&&')
    link = "hadithhub.com/nasai:5213"
    image_editable = ImageDraw.Draw(my_image)

    para = textwrap.wrap(araHadith, width=90)
    current_h, pad = 250, 130

    for line in reversed(para):
        w, h = image_editable.textsize(line, font=font, direction='rtl')
        image_editable.text(((imageWidth - w) / 2, current_h), line, font=font)
        current_h += h - pad

    font = ImageFont.truetype(
        '/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Light.ttf', 42)
    para = textwrap.wrap(engHadith, width=60)
    current_h, pad = 450, 10

    for line in para:
        w, h = image_editable.textsize(line, font=font)
        image_editable.text(((imageWidth - w) / 2, current_h), line, font=font)
        current_h += h + pad

    font = ImageFont.truetype(
        '/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Light.ttf', 35)

    for i in range(len(gradingList)):
        padding=40
        if(i%2==1):
            padding=700
        else:
            current_h = current_h+100
        image_editable.text((padding, current_h),gradingList[i], font=font)

    w, h = image_editable.textsize(reference, font=font)
    image_editable.text(((imageWidth - w) / 2, 20), reference, font=font)

    w, h = image_editable.textsize(link, font=font)
    image_editable.text(((imageWidth - w) / 2, 1120), link, font=font)

    my_image.save("result.png", "PNG")
    # img_byte_arr = io.BytesIO()
    # my_image.save(img_byte_arr, format='PNG')
    # img_byte_arr = img_byte_arr.getvalue()


def tweet(api: tweepy.API, message: str):
    api.update_status_with_media(message, './tmp/result.png')
    print('Tweeted successfully!')


def lambda_handler(event, context):
    auth = tweepy.OAuthHandler(os.environ['api_key'], os.environ['api_secret'])
    auth.set_access_token(os.environ['access_token'], os.environ['access_token_secret'])
    tweet(tweepy.API(auth), "Read More -> www.hadithhub.com")
    call('rm -rf /tmp/*', shell=True)
