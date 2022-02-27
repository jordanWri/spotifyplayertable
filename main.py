from time import sleep, time
import rfid_com as rfid
import spotify_api as spotify
import hw_com as gpio

volume = None
tmp_vol = volume
vol_thread_active = False


def main():
    global volume
    print("Scan the learn-card to add a Playlist to the system.")
    print("Scan the setup-card to assign the current playing device as default.")
    sleep(0.5)
    refresh_shuffle_led()
    volume = spotify.get_volume()
    print("Waiting for RFID Signal...")
    # =====Main Loop=====
    while True:
        uid, str_uid = rfid.check_once(10)
        '''
print(
            "state shuffle:",
            gpio.pi.read(gpio.shuffle_in),
            "state skip:",
            gpio.pi.read(gpio.skip_in),
            "state playpause:",
            gpio.pi.read(gpio.playpause_in),
        )
        '''
# timeout controlls refresh time for e.g. shuffle refresh
        refresh_shuffle_led()
        volume = spotify.get_volume()
        if uid == -1:
            continue
        # =====Checking uids for detected Card=====
        print("UID: ", str_uid)
        # Device Learning
        if str_uid == spotify.device_card_uid:
            device_id, device_name = spotify.current_device()
            if device_id != -1:
                spotify.set_config_value("DEVICE", "device_id", str(device_id))
                print("Set {} as new device. ID:{}".format(device_name, device_id))
                sleep(2)
                continue
            print("No playback detected, can't set device.")
            sleep(2) # Starting Card-Writing
            if str_uid == spotify.learn_card_uid:
                if write_card() == -1:
                    print("Something went wrong writing the new Music-Card.")
                    sleep(2)
                    # read data and play
                else:
                        uri = rfid.read_uri(uid)
                        if uri == -1:
                            print("Make sure you already added this Card.")
                            sleep(1)
                            continue
                        print("Found Music-Card.")
                        if spotify.play_context_URI(uri) == -1:  # play uri playlist at device
                            print(
                                "Current device unavailable, please select an available device."
                                )  # maybe use fallback device?
                            print(
                                "This can happen if you use a Phone or PC that is not always online."
                                )
                            sleep(1)
                            continue
                        print("Playing now!")
                        spotify.playstate = True
                        sleep(1)

def write_card():
    # Get current playlist uri and playing song info
    try:
        current = spotify.current_playback()
#         except TypeError:
#             print("oops")
#             return -1
        print("")
        print("Playing a playlist containing: {}, by {}.".format(current[1], current[2]))
        uri = current[0]
        sleep(2)
        print("Scan and hold the card you want to learn now.")
        print("Scan the learn-card again to abort.")
        str_uid = rfid.wait_for_uid()[1]
        if str_uid == spotify.learn_card_uid or str_uid == spotify.device_card_uid:
            print(" >Can't write uri to learn or device card. Arborting!")
            return -1
        
        if rfid.write_uri(uri) == -1:
            print(" >Error while writing.")
            return -1
        print("Successfully leaned!")
        if __name__ == "__main__":
            while True:
                try:
                    main()
                except:
                    print("CRASHED! Restarting in 6 seconds")
