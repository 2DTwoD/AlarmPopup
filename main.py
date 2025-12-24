from message.messages import Messages
from panels.main_window import MainWindow
from opc.parameters import Parameters
from opc.opc import OPCListener

from rx.subjects import Subject

win_width = '400'
win_height = '390'

version = "1.0"


if __name__ == "__main__":
    incomming_subject = Subject()
    parameters = Parameters('opc_tags.cfg')
    parameters.print_cfg()
    opcListener = OPCListener(parameters, incomming_subject, 4)
    opcListener.start_opc()

    messages = Messages(parameters, incomming_subject)

    title = "AlarmPopup v" + version
    size = win_width + 'x' + win_height
    main_window = MainWindow(title=title, size=size)
