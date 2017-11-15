#!/usr/bin/env python3

import os
import usb.core
import usb.util
from derp.component import Component

class UsbServo(Component):

    def __init__(self, config):
        """
        Interface through USB to the servo controller. At the moment the only
        supported capabilities are vague controls of the speed and steering. 
        """
        super(UsbServo, self).__init__(config)
        self.device = None
        
        self.usb_vendor_id = 0x1ffb # Polulu
        self.usb_product_id = 0x0089  # maestro 6
        
        self.state_name = self.config['act_state']
        self.state_offset_name = self.state_name + '_offset'


    def __del__(self):
        pass


    def act(self, state):

        if self.device is None:
            return False

        # Prepare turning command
        value = state[self.state_name]
        if self.state_offset_name in state:
            value += state[self.state_offset_name]

        # Limit command to known limits and convert to command
        value = min(value, self.config['max_value'])
        value = max(value, self.config['min_value'])
        command = int((1500 + 500 * value) * 4)
        
        return self.device.ctrl_transfer(0x40, 0x85, command, self.config['index'])
                                

    def discover(self):

        self.configuration = None
        self.device = usb.core.find(idVendor=self.usb_vendor_id,
                                    idProduct=self.usb_product_id)
        if self.device is None:
            return False
        
        self.configuration = self.device.get_active_configuration() 
        return True


    def scribe(self, state):
        return True


    def sense(self, state):
        return True

    
    def write(self):
        return True       