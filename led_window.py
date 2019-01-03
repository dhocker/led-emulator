#
# LED Emulator Window - for testing AtHomeLED
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

# Python 2/3
import sys
if sys.version_info.major is 3:
    import tkinter as Tk, tkinter.font as tkFont
else:
    import Tkinter as Tk, tkFont
from led_connection_handler import LEDConnectionHandler

class LEDTestFrame(Tk.Tk):
    def __init__(self, num_pixels, polling_interval_ms=20, frame_size=0):
        """
        Constructor
        :param num_pixels: Number of pixels in LED string
        :param polling_interval: Polling time in ms.
        """
        super(LEDTestFrame, self).__init__()
        self.title("LED Emulator")
        self.num_pixels = num_pixels

        # Largest row size, max 50 LEDs per line
        if self.num_pixels < 50:
            max_row_size = self.num_pixels
        else:
            max_row_size = 50

        # Determine width of a light for max of 50 LEDs per line
        sw = self.winfo_screenwidth()
        w = int((sw * 0.75) / 50)
        h = 30

        # This is the polling time
        self.polling_interval__ms = polling_interval_ms

        # main frame grid row tracker
        main_gr = 0

        nrows = int((self.num_pixels - 1) / max_row_size) + 1
        self.canvas = Tk.Canvas(self, height=h * 2 * nrows, width=max_row_size * w, bd=1, relief="solid")
        self.canvas.grid(row=main_gr, column=0)

        self.lights = []
        # Top and bottom
        y0 = (80 - h) / 2 + 2
        y1 = y0 + w - 2
        npx = self.num_pixels
        while npx > 0:
            if npx >= 50:
                row_size = 50
            else:
                row_size = npx
            for i in range(row_size):
                # n circles across
                # oval(x0, y0, x1, y1)
                # Left and right
                x0 = (w * i) + 3
                x1 = x0 + w - 3
                # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_oval.html
                self.lights.append(self.canvas.create_oval(x0, y0, x1, y1))

            # Set up for next row
            y0 += h
            y1 += h
            npx -= 50

        main_gr += 1

        # Metrics frame
        self.metrics_frame = Tk.Frame(self, height=h + w + 5, width=(self.num_pixels * w))
        self.metrics_frame.grid(row=main_gr, column=0)

        # Metrics frame grid row tracker
        metrics_gr = 0

        # Metrics
        self.speed_wait = Tk.Label(self.metrics_frame)
        self.speed_wait.grid(row=metrics_gr, column=0)
        self.speed_wait["text"] = "Polling Interval: " + str(self.polling_interval__ms) + "ms"

        self.frame_pixels = Tk.Label(self.metrics_frame)
        self.frame_pixels.grid(row=metrics_gr, column=1)
        self.frame_pixels["text"] = "Number pixels: " + str(self.num_pixels)

        self.frame_count = 0
        self.frame_count_w = Tk.Label(self.metrics_frame)
        self.frame_count_w.grid(row=metrics_gr, column=2)
        self.frame_count_w["text"] = "Frame count: " + str(self.frame_count)

        main_gr += 1

        # Quit button
        self.q = Tk.Button(self, text="Quit", width=4, command=self.destroy)
        self.q.grid(row=main_gr, column=0)

        # Prime the color and timer event
        self.run = True
        self.next_frame()

    def next_frame(self):
        """
        Process all queued LED data frames
        :return:
        """
        # Here's where we need to get the next data frame
        frame = LEDConnectionHandler.get_frame()
        while frame:
            self.frame_count += 1
            self.frame_count_w["text"] = "Frame count: " + str(self.frame_count)
            for i in range(len(self.lights)):
                p = (frame[i][1], frame[i][2], frame[i][3])
                self.canvas.itemconfigure(self.lights[i], fill="#%02x%02x%02x" % p)

            # Check for another LED data frame
            frame = LEDConnectionHandler.get_frame()

        if self.run:
            self.after(self.polling_interval__ms, self.next_frame)

def run_led_window(num_pixels):
    test_frame = LEDTestFrame(num_pixels)
    test_frame.mainloop()
    print("LED window closed")