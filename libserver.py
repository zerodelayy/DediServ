import sys
import selectors
import json
import io
import struct
from datetime import datetime
import subprocess
import signal
import os
import psutil

server_path = {
    "Island": 'calc.exe',
    "Center": 'notepad.exe',
    "Scorched": 'C:\ARK\ARKServer\ShooterGame\Binaries\Win64\ShooterGameServer.exe "ScorchedEarth_P?SessionName=UMU - Scorched Earth?RCONPort=27123?Port=7781?QueryPort=27019?CrossARKAllowForeignDinoDownloads=true?MaxPlayers=20?AltSaveDirectoryName=Server_3_SC?" -NoBattlEye -NoTransferFromFiltering -log -ClusterDirOverride=C:\ARK\Cluster -clusterid=UMUsCluster',
    "Ragnarok": 'C:\ARK\ARKServer 4\ShooterGame\Binaries\Win64\ShooterGameServer.exe "Ragnarok?SessionName=UMU - Ragnarok?RCONPort=27124?Port=7783?QueryPort=27021?CrossARKAllowForeignDinoDownloads=true?MaxPlayers=20?" -NoBattlEye -NoTransferFromFiltering -log -ClusterDirOverride=C:\ARK\Cluster -clusterid=UMUsCluster',
    "Aberration": 'C:\ARK\ARKServer\ShooterGame\Binaries\Win64\ShooterGameServer.exe "Aberration_P?SessionName=UMU - Aberration?RCONPort=27125?Port=7785?QueryPort=27023?CrossARKAllowForeignDinoDownloads=true?MaxPlayers=20?AltSaveDirectoryName=Server_5_Abe?" -NoBattlEye -NoTransferFromFiltering -log',
    "Extinction": 'C:\ARK\ARKServer\ShooterGame\Binaries\Win64\ShooterGameServer.exe "Extinction?SessionName=UMU - Extinction?RCONPort=27126?Port=7787?QueryPort=27025?CrossARKAllowForeignDinoDownloads=true?MaxPlayers=20?AltSaveDirectoryName=Server_6_Ext?" -NoBattlEye -NoTransferFromFiltering -log -ClusterDirOverride=C:\ARK\Cluster -clusterid=UMUsCluster'
}


server_list = {
    "Island": 0,
    "Center": 0,
    "Scorched": 0,
    "Ragnarok": 0,
    "Aberration": 0,
    "Extinction": 0
}

class Arkserver:
    def __init__(self):
        self.serverstate = False
        self.updatestate = False

    def updatestatus(self):
        tasklistr = os.popen("tasklist").read()
        if "steamcmd.exe" in tasklistr:
            self.updatestate = True
            print("Update in progress.")
            with open("Transactions.txt", "a") as w1:
                w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Update in progress")
        else:
            self.updatestate = False
            print("Update finished.")
            with open("Transactions.txt", "a") as w1:
                w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Update stopped")

    def serverstatus(self, server_name):
        server_pid = server_list.get(server_name)
        if psutil.pid_exists(server_pid):
            print("Server Status of {0} is Running".format(server_name))
            with open("Transactions.txt", "a") as w1:
                w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server Status of {0} is Running".format(server_name))
                return True
        else:
            print("Server Status of {0} is Stopped".format(server_name))
            with open("Transactions.txt", "a") as w1:
                w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server Status of {0} is Stopped".format(server_name))
                return False


    def launch_server(self, server_name, path):
        try:
            servproc = subprocess.Popen(path, shell=False)
            server_list[server_name] = servproc.pid
            print("Server {0} launched with PID {1}.".format(server_name, servproc.pid))
            with open("Transactions.txt", "a") as w1:
                w1.write(
                    "\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server {0} launched with PID {1}.".format(
                        server_name, servproc.pid))
        except Exception as ex:
            print("main error: {0}".format(ex))
            with open("Transactions.txt", "a") as w1:
                w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "main error:{0}".format(ex))

    def kill_server(self, server_name):
        if server_list.get(server_name) != 0:
            os.kill((server_list.get(server_name)), signal.SIGTERM)
            print("Server {0} has been terminated.".format(server_name))
            with open("Transactions.txt", "a") as w1:
                w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "Server {0} has been terminated.".format(
                    server_name))
        else:
            print("Server {0} cannot be terminated as it is not currently running.".format(server_name))
            with open("Transactions.txt", "a") as w1:
                w1.write("\n" + datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S") + " Server {0} cannot be terminated as it is not currently running.".format(
                    server_name))


class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False

    def _set_selector_events_mask(self, mode):
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            data = self.sock.recv(4096)
        except BlockingIOError:
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer connection has been closed.")

    def _write(self):
        if self._send_buffer:
            print("Sending", repr(self._send_buffer), "to", self.addr)
            try:
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                if sent and not self._send_buffer:
                    self.close()

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(
            self, *, content_bytes, content_type, content_encoding
    ):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def _create_response_json_content(self):
        print(server_list)
        action = self.request.get("action")
        if action == "action":
            command = self.request.get("value")
            print(server_path.get(command))
            Arkserver.launch_server(Arkserver, command, server_path.get(command))
            answer = "It works"
            content = {"result": answer}
        else:
            content = {"result": f'Error: invalid action "{action}".'}
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response


    def _create_response_binary_content(self):
        response = {
            "content_bytes": b"First 10 bytes of request: "
            + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

        self._write()

    def close(self):
        print("Closing connection to {0}".format(self.addr))
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                f"error: selector.unregister() exception for ",
                f"{self.addr}: {repr(e)}",
            )

        try:
            self.sock.close()
        except OSError as e:
            print(
                f"error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            self.sock = None

    def process_protoheader(self):
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_buffer[:hdrlen]
            )[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in(
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f'Missing required header "{reqhdr}".')

    def process_request(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            print("Received Request {0} from {1}".format(repr(self.request), self.addr))
        else:
            self.request = data
            print(
                f'Received {self.jsonheader["content-type"]} request from',
                self.addr,
            )
        self._set_selector_events_mask("w")

    def create_response(self):
        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()
        else:
            response = self._create_response_binary_content()
        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message



