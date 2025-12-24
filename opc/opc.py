import threading
import time

import OpenOPC
import pywintypes
from rx.subjects import Subject

from opc.parameters import Parameters

pywintypes.datetime = pywintypes.TimeType


class OPCListener:

    def __init__(self, parameters: Parameters, incomming_subject: Subject, update_time=1):
        self.parameters = parameters
        self.incomming_subject = incomming_subject
        self.tags = []
        self.update_time = update_time

    def start_opc(self):
        threading.Thread(target=lambda: self._run(), daemon=True).start()

    def _run(self):
        try:
            opc = OpenOPC.client()
            opc.connect(self.parameters.OPCname)
            opc.read(self.parameters.tags, group=self.parameters.group, update=self.update_time)
            while True:
                time.sleep(self.update_time)
                try:
                    self.tags = opc.read(group=self.parameters.group)
                    for tag in self.tags:
                        self.incomming_subject.on_next(tag)
                except OpenOPC.TimeoutError as e:
                    print("Reading exception occurred: ", e)
                    opc.remove(self.parameters.group)
                    opc.close()
        except OpenOPC.OPCError as e:
            print("Connection exception occurred: ", e)
            time.sleep(5)
            self.start_opc()
