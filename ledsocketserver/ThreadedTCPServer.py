# coding: utf-8
#
# AtHomeSocketServer
# Copyright © 2016, 2018  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import sys
try:
    import socketserver as socketserver
except ImportError:
    import SocketServer as socketserver


"""
TCP server using threads.
"""


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
