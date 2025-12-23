import time

import OpenOPC
import pywintypes

from file_work import FileWork

pywintypes.datetime = pywintypes.TimeType


class OPCListener:

    def __init__(self, fileWork: FileWork, update_time=1):
        self.fileWork = fileWork
        self.update_time = update_time

    def start_opc(self):
        try:
            opc = OpenOPC.client()
            opc.connect(self.fileWork.OPCname)
            opc.read(self.fileWork.tags, group=self.fileWork.group, update=self.update_time)
            while True:
                time.sleep(self.update_time)
                try:
                    value = opc.read(group=self.fileWork.group)
                    print(value)
                except OpenOPC.TimeoutError as e:
                    print("Reading exception occurred: ", e)
                    opc.remove(self.fileWork.group)
                    opc.close()
        except OpenOPC.OPCError as e:
            print("Connection exception occurred: ", e)
            time.sleep(5)
            self.start_opc()