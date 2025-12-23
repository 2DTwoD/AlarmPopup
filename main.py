from file_work import FileWork
from opc import OPCListener

fileWork = FileWork('tags.cfg')

fileWork.print_cfg()

opcListener = OPCListener(fileWork)
opcListener.start_opc()