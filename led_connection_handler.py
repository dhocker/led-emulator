#
# Server socket connection handler
# Copyright (C) 2016  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#

import app_logger
from configuration import Configuration
# import engine.led_engine
from threading import Lock

logger = app_logger.getAppLogger()

class LEDConnectionHandler:
    """
    The socket server creates one instance of this class for each
    incoming connection. That instance handles LED data sent by a network client.

    The protocol is simple. The client sends a stream of data as if the
    server is a WS281X or APA102 LED string.

    Each transmission is (n * 4) + 8 bytes in length where n is the
    number of LEDs in the string. The 8 bytes comes from a 4 byte
    header and a 4 byte trailer.
    """

    frame_list = []
    frame_lock = Lock()

    def __init__(self):
        """
        Constructor for an instance. A LED data frame looks like this.
        Header = 4 bytes of 0x00
        Body = 4 bytes for each pixel (brightness, r, g, b)
        Trailer = 4 bytes of 0xFF
        """
        # There are 4 bytes for each pixel
        self.frame_pixel_size = 4
        self.num_pixels = Configuration.num_pixels()
        self.frame_body_size = self.num_pixels * self.frame_pixel_size
        self.frame_start = self.frame_pixel_size # starts after the header
        self.frame_end = self.frame_start + self.frame_body_size

    def execute_command(self, port, led_data):
        """
        Execute a client command/request.
        :param port: The port number receiving the request. It can be used
        to qualify or descriminate the request. The idea is to be able to
        map a port number to a device.
        :param led_data: The LED data sent by the client.
        :return: None
        """
        print("Frame received")
        # print(str(led_data))
        # Let's reformat the frame into something that the LED window can readily use
        pixels = []
        for fx in range(self.frame_start, self.frame_end, self.frame_pixel_size):
            # brightness, r, g, b
            pixels.append((led_data[fx], led_data[fx + 1], led_data[fx + 2], led_data[fx + 3]))

        LEDConnectionHandler.frame_lock.acquire()

        LEDConnectionHandler.frame_list.append(pixels)

        LEDConnectionHandler.frame_lock.release()

        return None

    @classmethod
    def get_frame(cls):
        """
        Gets the next available LED data frame. The frame is a list of 4-tuples,
        where each tuple is (brightness, r, g, b).
        :return: Returns the frame or None
        """
        frame = None

        LEDConnectionHandler.frame_lock.acquire()

        if len(cls.frame_list):
            frame = cls.frame_list.pop()

        LEDConnectionHandler.frame_lock.release()

        return frame