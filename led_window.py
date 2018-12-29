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
    def __init__(self, num_pixels, polling_interval_ms=20):
        """
        Constructor
        :param num_pixels: Number of pixels in LED string
        :param polling_interval: Polling time in ms.
        """
        super(LEDTestFrame, self).__init__()
        self.title("Color Cycler Test")
        self.num_pixels = num_pixels

        # Determine width of a light
        sw = self.winfo_screenwidth()
        w = int((sw - 500) / num_pixels)
        h = 30
        # w = 30

        # This is the polling time
        self.wait_ms = polling_interval_ms

        gr = 0

        # The color box
        # self.f = Tk.Frame(self, height=80, width=800)
        self.f = Tk.Frame(self, height=h + w + 5, width=(num_pixels * w))
        self.f.grid(row=gr, column=0)

        # Speed/wait
        self.speed_wait = Tk.Label(self, width=10)
        self.speed_wait.grid(row=gr, column=1)
        self.speed_wait["text"] = str(self.wait_ms) + "ms"

        # The color value
        self.c = Tk.Label(self, width=10)
        self.c.grid(row=gr, column=3)

        gr += 1

        self.canvas = Tk.Canvas(self, height=h * 2, width=self.num_pixels * w)
        self.canvas.grid(row=gr, column=0)

        self.lights = []
        y0 = (80 - h) / 2 + 2
        y1 = y0 + w - 2
        for i in range(self.num_pixels):
            # n circles across
            # oval(x0, y0, x1, y1)
            x0 = (w * i) + 3
            x1 = x0 + w - 3
            # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_oval.html
            self.lights.append(self.canvas.create_oval(x0, y0, x1, y1))

        gr += 1

        # Slower/Faster buttons
        self.slower_botton = Tk.Button(self, text="Slower", width=6, command=self.run_slower)
        self.slower_botton.grid(row=gr, column=1)
        self.faster_botton = Tk.Button(self, text="Faster", width=6, command=self.run_faster)
        self.faster_botton.grid(row=gr, column=2)

        # Run/Pause button
        self.rb = Tk.Button(self, text="Pause", width=6, command=self.run_pause)
        self.rb.grid(row=gr, column=3)
        # Quit button
        self.q = Tk.Button(self, text="Quit", width=4, command=self.destroy)
        self.q.grid(row=gr, column=4)

        # Prime the color and timer event
        self.run = True
        self.next_frame()

    def run_slower(self):
        self.wait_ms += 50
        self.speed_wait["text"] = str(self.wait_ms)

    def run_faster(self):
        if self.wait_ms > 50:
            self.wait_ms -= 50
        self.speed_wait["text"] = str(self.wait_ms)

    def run_pause(self):
        if self.run:
            self.run = False
            self.rb["text"] = "Run"
        else:
            self.run = True
            self.rb["text"] = "Pause"
            self.next_frame()

    def next_frame(self):
        """
        Process all queued LED data frames
        :return:
        """
        # Here's where we need to get the next data frame
        frame = LEDConnectionHandler.get_frame()
        while frame:
            tkcolor = "#%02x%02x%02x" % (frame[0][1], frame[0][2], frame[0][3])

            # Update all widgets with this color
            self.c["text"] = tkcolor.upper()
            self.f.config(bg=tkcolor)

            for i in range(len(self.lights)):
                p = (frame[i][1], frame[i][2], frame[i][3])
                self.canvas.itemconfigure(self.lights[i], fill="#%02x%02x%02x" % p)

            # Check for another LED data frame
            frame = LEDConnectionHandler.get_frame()

        if self.run:
            self.f.after(self.wait_ms, self.next_frame)

def run_led_window():
    test_frame = LEDTestFrame(50)
    test_frame.mainloop()
    print("LED window closed")