import asyncio
import json
import urllib
import sys
import logging
import requests
from aioflic import *


def handle_button_call(channel, click_type, was_queued, time_diff):

    #1 (fönster)
    #80:e4:da:72:bf:78
    #2 (Side board)
    #80:e4:da:72:76:8a
    #3 Garage by the door
    #80:e4:da:73:58:39
    #4 Ovanvåning
    #80:e4:da:72:bf:82
    logging.info("Simple or Double or hold {} {} {} was queued {}".format(channel.bd_addr,str(click_type),time_diff, str(was_queued)))

    if was_queued == 1:
        logging.warning("Ignoring queued message")
        return
    
    # Set the light scenes Plan1
    if channel.bd_addr == '80:e4:da:72:bf:78' or channel.bd_addr == '80:e4:da:72:76:8a': 
        idx = '1'
        if click_type is ClickType.ButtonSingleClick:
            idx = '1'
        elif click_type is ClickType.ButtonDoubleClick:
            idx = '3'
        else:
            idx = '2'
            
        url = 'http://192.168.1.213:8080/json.htm?type=command&param=switchscene&idx=' + idx + '&switchcmd=On'

        try:
            r = urllib.request.urlopen(url)
            logging.info("Switched scene Plan 1 ")
        except urllib.error.HTTPError as e:
            logging.error(e.code)
    
    # Set the light scenes Plan2 
    if channel.bd_addr == '80:e4:da:72:bf:82': 
        idx = '5'
        if click_type is ClickType.ButtonSingleClick:
            idx = '5'
        elif click_type is ClickType.ButtonDoubleClick:
            idx = '4'
        else:
            idx = '4'
            
        url = 'http://192.168.1.213:8080/json.htm?type=command&param=switchscene&idx=' + idx + '&switchcmd=On'

        try:
            r = urllib.request.urlopen(url)
            logging.info("Switched scene Plan 2 ")
        except urllib.error.HTTPError as e:
            logging.error(e.code)

    # Garage button next to the door
    if channel.bd_addr == '80:e4:da:73:58:39':
            
        url = 'http://192.168.1.213:8080/json.htm?type=command&param=switchlight&idx=429&switchcmd=On'

        try:
            r = urllib.request.urlopen(url)
            logging.info("Toggle Garaget")
        except urllib.error.HTTPError as e:
            logging.error(e.code)
            

def got_button(bd_addr):
    cc = ButtonConnectionChannel(bd_addr)
    cc.on_button_single_or_double_click_or_hold = \
        lambda channel, click_type, was_queued, time_diff: \
            handle_button_call(channel, click_type, was_queued, time_diff)
    cc.on_connection_status_changed = \
        lambda channel, connection_status, disconnect_reason: \
            logging.info(channel.bd_addr + " " + str(connection_status) + (" " + str(disconnect_reason) if connection_status == ConnectionStatus.Disconnected else ""))
    client.add_connection_channel(cc)

def got_info(items):
    logging.info(items)
    for bd_addr in items["bd_addr_of_verified_buttons"]:
        got_button(bd_addr)
    scan()
        
def on_found_private_button(scan_wizard):
        logging.info("Found a private button. Please hold it down for 7 seconds to make it public.")

def on_found_public_button(scan_wizard, bd_addr, name):
        logging.info("Found public button " + bd_addr + " (" + name + "), now connecting...")

def on_button_connected(scan_wizard, bd_addr, name):
        logging.info("The button was connected, now verifying...")
        got_button(bd_addr)

def on_completed(scan_wizard, result, bd_addr, name):
        logging.info("Scan wizard completed with result " + str(result) + ".")
        if result == ScanWizardResult.WizardSuccess:
                logging.info("Your button is now ready. The bd addr is " + bd_addr + ".")


def scan():
    logging.info("Starting the scan")
    mywiz=ScanWizard()
    mywiz.on_found_private_button = on_found_private_button
    mywiz.on_found_public_button = on_found_public_button
    mywiz.on_button_connected = on_button_connected
    mywiz.on_completed = on_completed
    client.add_scan_wizard(mywiz)

            

logging.basicConfig(format='%(asctime)s %(message)s', stream=sys.stdout, level=logging.INFO)    
FlicClient.on_get_info=got_info
loop = asyncio.get_event_loop()  
try:
    coro = loop.create_connection(lambda: FlicClient( loop),
                            'localhost', 5551)
    conn,client=loop.run_until_complete(coro)
    client.on_get_info=got_info
    client.get_info()
    loop.run_forever()
except  KeyboardInterrupt:
    logging.info("Exiting at user's request")
finally:
    # Close the server
    client.close()
    loop.close()   
