from panels.message_table import MessageTable
from panels.main_window import MainWindow
from opc.parameters import Parameters
from opc.opc import OPCListener

from rx.subjects import Subject

from panels.tag_viewer import TagViewer

if __name__ == "__main__":
    version = "1.0"
    app_win_width = 800
    app_win_height = 400
    app_title = "AlarmPopup v" + version
    tv_win_width = 800
    tv_win_height = 200
    tv_title = "Tag viewer v" + version

    hotkey = 'F4'
    tag_viewer_password = 'adMin'

    show_tag_viewer_subject = Subject()
    incomming_tags_subject = Subject()
    show_hide_window_subject = Subject()

    main_window = MainWindow(title=app_title, win_width=app_win_width, win_height=app_win_height, hotkey=hotkey,
                             show_tag_viewer_subject=show_tag_viewer_subject,
                             show_hide_window_subject=show_hide_window_subject)

    parameters = Parameters(path='opc_tags.cfg')
    # parameters.print_cfg()

    opcListener = OPCListener(parameters=parameters,
                              incomming_tags_subject=incomming_tags_subject)
    opcListener.start_opc()

    messageTable = MessageTable(master=main_window,
                                incomming_tags_subject=incomming_tags_subject,
                                show_hide_window_subject=show_hide_window_subject)

    tagViewer = TagViewer(title=tv_title, win_width=tv_win_width, win_height=tv_win_height,
                          password=tag_viewer_password,
                          incomming_tags_subject=incomming_tags_subject,
                          show_tag_viewer_subject=show_tag_viewer_subject)

    main_window.mainloop()
