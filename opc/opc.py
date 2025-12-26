import threading
import time

import OpenOPC
import pywintypes
from rx.subjects import Subject

from opc.parameters import Parameters

pywintypes.datetime = pywintypes.TimeType


class OPCListener:

    def __init__(self, parameters: Parameters, incomming_tags_subject: Subject, update_time=1):
        self.parameters = parameters
        self.incomming_tags_subject = incomming_tags_subject
        self.update_time = update_time

    def start_opc(self):
        threading.Thread(target=lambda: self._run(), daemon=True).start()

    def _run(self):
        try:
            opc = OpenOPC.client()
            opc.connect(self.parameters.OPCname)
            self.incomming_tags_subject.on_next('clear')
            opc.read(self.parameters.tags, group=self.parameters.group, update=self.update_time)
            while True:
                time.sleep(self.update_time)
                try:
                    tags = opc.read(group=self.parameters.group)
                    for i in range(len(tags)):
                        tags[i] = tags[i] + (self.parameters.messages[tags[i][0]], )
                    self.incomming_tags_subject.on_next(tags)
                except OpenOPC.TimeoutError as e:
                    print("Reading exception occurred: ", e)
                    opc.remove(self.parameters.group)
                    opc.close()
                    break
        except OpenOPC.OPCError as e:
            print("Connection exception occurred: ", e)
        self.incomming_tags_subject.on_next('OPC error')
        time.sleep(5)
        self.start_opc()
