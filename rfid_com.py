import time
from spotify_api import learn_card_uid, sp
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import configparser
from requests.models import HTTPError
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.oauth2 as oauth2
import urllib.request
from PIL import Image
from pynput.keyboard import Key, Controller

keyboard = Controller()
key = "Key.f11"

# =====Spotipy Oauth Init=====
client_id = "8cbea6b5526346d4970b340a9dfe417f"
client_secret = "2cf17fe6fbba498c85dc2d16a00d9fee"
redirect_uri = "http://google.com/"
scope = "user-modify-playback-state user-library-read playlist-read-private user-read-playback-state user-read-currently-playing"
while True:
    reader = SimpleMFRC522()
    tester = sp.current_playback()
    imgfiletest = tester["item"]["album"]["images"][0]["url"]
    time.sleep(2)
    a,b = reader.read_no_block()
    if a != None:
        id, text = reader.read()
        print(id)
        print(text)
        GPIO.cleanup()
        if str(id) == str(learn_card_uid):
            print("nice")
            playback = sp.current_playback()
            if playback != None:
                nuri=playback["context"]["uri"]
                time.sleep(2)
                try:
                    reader.write(nuri)
                    print("Written")
                finally:
                    GPIO.cleanup()
        if str(id) != str(learn_card_uid):
            print("cool")
            data = sp.current_playback()
            print(data["device"]["id"])
            print(data["device"]["name"])
            pushuri=text.replace(" ","")
            sp.start_playback(device_id=str(data["device"]["id"]), context_uri=pushuri)
            GPIO.cleanup()
    time.sleep(1)
    data = sp.current_playback()
    imgfile = data["item"]["album"]["images"][0]["url"]
    if imgfile != imgfiletest:
        (need,dont) = urllib.request.urlretrieve(imgfile)
        img = Image.open(need)
        img.show()
        time.sleep(2)
        keyboard.press(Key.f11)
        keyboard.release(Key.f11 )

    


        
    
#     if text is not None:
#         sp.start_playback(uris=name)
#     else text is None:
#         print("oops")
#     
    
    
# 
# if text == learn_card_uid
# try:
#         playback = sp.current_playback()
#     if playback != None:
#         try:
#             return [
#                 playback["context"]["uri"],
#                 playback["item"]["name"],
#                 playback["item"]["artists"][0]["name"],
#             ]
#         except TypeError:  # Personal playlists cant be learned that easy. WIP
#             return -1
#     else:
#         return -1
#         text = "uri"
#         print("Now place your tag to write")
#         reader.write(text)
#         print("Written")
# finally:
#         GPIO.cleanup()
