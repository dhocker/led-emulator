# coding: utf-8
#
# AtHomeSocketServer
# Copyright © 2016, 2018  Dave Hocker (email: AtHomeX10@gmail.com)
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

import json
from collections import OrderedDict

class CommandHandler:
    """
    Handles commands sent by a network client.

    The protocol is very simple (loosely based on the mpd (music player daemon) protocol).
    The client sends a command line terminated by a newline (\n). In this case, the command line
    consists of a command and any number of operands.
    The command handler parses the command line into into its constituent parts.
    The command handler executes the command a returns a JSON formatted response.
    The response is one line, terminated with a newline.
    The JSON payload is a dictionary. The following properties appear in all responses.
        command: the command for which the response was generated
        result: OK or ERROR
    The remainder of the response is command dependent.

    Examples
    Client sends:
        scriptfiles\n
    Server responds:
        {"command": "scriptfiles", "result": "OK", "scriptfiles": ["definitions.dmx", "test-end.dmx", "test.dmx"]}\n

    Client sends:
        bad-command\n
    Server responds:
        {"command": "bad-command", "result": "ERROR", "messages": ["Unrecognized command"]}\n

    The easiest way to experiment with the client is to use telnet. Simply open
    a connection and type commands.
        telnet server host
    """

    # Protocol constants
    OK_RESPONSE = "OK"
    ERROR_RESPONSE = "ERROR"
    END_RESPONSE_DELIMITER = "\n"

    class Response:
        def __init__(self, command, result=None, state=None):
            self._response = OrderedDict()
            self._response["command"] = command
            if result:
                self._response["result"] = result
            if state:
                self._response["state"] = state

        def set_result(self, result):
            self._response["result"] = result

        def set_state(self, state):
            self._response["state"] = state

        def is_closed(self):
            if "state" in self._response:
                return self._response["state"] == "CLOSED"
            return False

        def set_value(self, key, value):
            self._response[key] = value

        def __str__(self):
            return json.dumps(self._response) + CommandHandler.END_RESPONSE_DELIMITER

    def __init__(self):
        """
        Constructor for an instance of CommandHandler
        """
        # Valid commands and their handlers
        # Note that the command handler MUST implement either a close or quit command.
        self._valid_commands = {
            "status": self.get_status,
            "test": self.test_command,
            "close": self.close_connection,
        }

    def execute_command(self, port, raw_command):
        """
        Execute a client command/request.
        :param port:
        :param raw_command:
        :return: Returns a response instance
        """
        tokens = raw_command.lower().split()
        if (len(tokens) >= 1) and (tokens[0] in self._valid_commands):
            if self._valid_commands[tokens[0]]:
                response = self._valid_commands[tokens[0]](tokens, raw_command)
            else:
                r = CommandHandler.Response(tokens[0], result=CommandHandler.ERROR_RESPONSE)
                r.set_value("messages", "Command not implemented")
                response = r
        else:
            r = CommandHandler.Response(tokens[0], result=CommandHandler.ERROR_RESPONSE)
            r.set_value("messages", "Unrecognized command")
            response = r

        # Return the command generated response with the end of response
        # delimiter tacked on.
        return response


    def get_status(self, tokens, command):
        """
        Return current status of DMX script engine.
        :param tokens:
        :param command:
        :return:
        """
        r = CommandHandler.Response(tokens[0], result=CommandHandler.OK_RESPONSE)
        return r

    def test_command(self, tokens, command):
        """
        An example of a command.
        :param tokens:
        :param command:
        :return:
        """
        r = CommandHandler.Response(tokens[0], result=CommandHandler.OK_RESPONSE)
        r.set_state("Doing nothing")
        r.set_value("arg1", "value of arg1")
        r.set_value("message", "This is an example test command")
        return r

    def close_connection(self, tokens, command):
        """
        Close the current connection/session.
        :param tokens:
        :param command:
        :return:
        """
        r = CommandHandler.Response(tokens[0], result=CommandHandler.OK_RESPONSE, state="CLOSED")
        return r
