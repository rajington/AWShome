#!/usr/bin/env python

import os
import json
import time
import pi_switch
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

class OnOff:
    def __init__(self, name, onCode, offCode, rf, iot):
        self.name = name
        self.onCode = onCode
        self.offCode = offCode
        self.rf = rf

        self.shadow = iot.createShadowHandlerWithName(self.name, True)
        self.shadow.shadowRegisterDeltaCallback(self.newShadow)
        self.set(False)

    def set(self, state):
        code = self.onCode if state else self.offCode
        print('Turning %s %s using code %i' % (self.name, 'ON' if state else 'OFF', code))
        self.rf.sendDecimal(code, 24)
        self.shadow.shadowUpdate(json.dumps({
            'state': {
                'reported': {
                    'light': state
                    }
                }
            }
        ), None, 5)

    def newShadow(self, payload, responseStatus, token):
        newState = json.loads(payload)['state']['light']
        self.set(newState)

def createIoT():
    iot = AWSIoTMQTTShadowClient('AWSHome', useWebsocket=True)
    iot.configureEndpoint('a236biar7596mr.iot.us-east-1.amazonaws.com', 443)
    iot.configureCredentials(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'root-CA.pem'))
    iot.configureConnectDisconnectTimeout(10)  # 10 sec
    iot.configureMQTTOperationTimeout(5)  # 5 sec
    iot.connect()
    return iot

def createRF():
    rf = pi_switch.RCSwitchSender()
    rf.enableTransmit(0)
    rf.setPulseLength(194)
    return rf

if __name__ == "__main__":
    iot = createIoT()
    rf = createRF()

    # Create your switches here, using the format:
    #   OnOff(<THING NAME>, <ON CODE>, <OFF CODE>, rf, iot)
    #
    # Example:
    #   OnOff('floor-lamp', 284099, 284108, rf, iot)
    #
    OnOff('floor-lamp', 284099, 284108, rf, iot)
    OnOff('table-lamp', 283955, 283964, rf, iot)

    print('Listening...')

    while True:
        time.sleep(0.2)
