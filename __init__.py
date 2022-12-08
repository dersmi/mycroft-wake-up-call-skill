"""
skill WakeUpCall

Sends a signal to the Adafruit Monster M4sk using GPIO, telling 
the eyes to open when the wakeword is heard.  Actually, we're hooking
into the record event since I wasn't able to get it working using 
the wakeword directly.
"""

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util import LOG
import gpiod
import time

GPIO_CHIP = 'gpiochip1'
M4SK_LINE_OFFSET = 94

chip = gpiod.chip(GPIO_CHIP)
M4SK_signal_pin = chip.get_line(M4SK_LINE_OFFSET)

config = gpiod.line_request()
config.consumer = "WakeUpCall"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT

M4SK_signal_pin.request(config)

class WakeUpCall(MycroftSkill):

    def __init__(self):
        super(WakeUpCall, self).__init__(name="WakeUpCall")

    def initialize(self):
        self.add_event('recognizer_loop:record_begin',
                       self.record_begin_handler)

    def record_begin_handler(self, message):
        self.log.info("Record begin event handler starting, waking the mask!")

        # based on observation, 1 sets the pin to 3.3v (low signal), telling the eyes to wake up
        M4SK_signal_pin.set_value(1)
        time.sleep(45)
        # shut the eyes after a while
        # todo: find an event to hook into or schedule this action on the bus
        self.log.info("Record begin event handler ending, closing the eyes.")
        M4SK_signal_pin.set_value(0)

def create_skill():
    return WakeUpCall()