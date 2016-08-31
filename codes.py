#!/usr/bin/env python

import pi_switch

print('Listening for RF codes...')
while True:
    # print the RF codes for easy setup
    receiver = pi_switch.RCSwitchReceiver()
    receiver.enableReceive(2)
    while True:
        if receiver.available():
            received_value = receiver.getReceivedValue()
            if received_value:
                print('Received code %i' % received_value)
            receiver.resetAvailable()
