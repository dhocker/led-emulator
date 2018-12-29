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

#
# Socket server running on its own thread
#

import threading
from .ThreadedTCPServer import ThreadedTCPServer
from .TCPRequestHandler import TCPRequestHandler

# This class should be used as a singleton
class SocketServerThread:
    # Constructor of an instance to serve a given host:port
    def __init__(self, host, port, handler, connection_time_out=-1, frame_size=None):
        self.host = host
        self.port = port
        self.server_thread = threading.Thread(target=self.RunServer)
        ThreadedTCPServer.allow_reuse_address = True
        # Inject the command handler class into the request handler
        TCPRequestHandler.set_command_handler_class(handler, connection_time_out=connection_time_out)
        # Inject LED data frame size
        if frame_size:
            TCPRequestHandler.set_frame_size(frame_size)

        self.server = ThreadedTCPServer((host, port), TCPRequestHandler)

    # Start the TCPServer on its own thread
    def Start(self):
        self.server_thread.start()

    # Stop the TCPServer thread
    def Stop(self):
        print("Shutting down TCPServer thread")
        self.server.shutdown()
        self.server_thread.join()
        print("TCPServer thread down")

    # Run TCPServer on a new thread
    def RunServer(self):
        print("Now serving sockets at {0}:{1}".format(self.host, self.port))
        self.server.serve_forever()
