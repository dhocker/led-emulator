#
# test client - for testing LED Emulator
# Copyright © 2019  Dave Hocker (email: AtHomeX10@gmail.com)
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

import socket
import time
from struct import pack

def main():
    """
    Main program for test client. This client connects to the LED Emulator
    and sends it a number of LED data frames.
    :return: Nothing
    """
    num_pixels = 150
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Connecting...")
        sock.connect(("localhost", 5555))
        print("Connected")

        print("Sending frames...")
        rgb = [
            [0x0E, 0xFF, 0, 0],
            [0x0E, 0x00, 0xFF, 0],
            [0x0E, 0x00, 0xFF, 0xFF],
            [0x0E, 0xFF, 0x00, 0xFF],
            [0x0E, 0xFF, 0xFF, 0x00],
        ]
        shift = 0
        for i in range(10):
            frame = bytes([0, 0, 0, 0])
            for i in range(num_pixels):
                frame += bytes(rgb[(i + shift) % len(rgb)])
            frame += bytes([0xFF, 0xFF, 0xFF, 0xFF])
            frame_send(sock, frame)
            print("Frame sent")
            time.sleep(0.500)
            shift = (shift + 1) % len(rgb)
    except Exception as ex:
        print(str(ex))
    finally:
        sock.close()

def frame_send(sock, frame):
    block_send(sock, len(frame))
    block_send(sock, frame)

def block_send(sock, block):
    total_sent = 0
    if isinstance(block, int):
        block = pack('!i', block)
    while total_sent < len(block):
        sent = sock.send(block[total_sent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        total_sent = total_sent + sent

#
# Run as an application
#
if __name__ == "__main__":
    main()
