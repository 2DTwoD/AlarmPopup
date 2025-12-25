from panels.message_table import MessageTable
from panels.main_window import MainWindow
from opc.parameters import Parameters
from opc.opc import OPCListener

from rx.subjects import Subject

from panels.tag_viewer import TagViewer

if __name__ == "__main__":
    version = "1.0"
    app_win_width = '800'
    app_win_height = '400'
    app_title = "AlarmPopup v" + version
    tv_win_width = '800'
    tv_win_height = '200'
    tv_title = "Tag viewer v" + version

    app_size = app_win_width + 'x' + app_win_height
    tv_size = app_win_width + 'x' + tv_win_height

    show_tag_viewer_subject = Subject()
    incomming_tags_subject = Subject()

    main_window = MainWindow(title=app_title, size=app_size, show_tag_viewer_subject=show_tag_viewer_subject)

    parameters = Parameters('opc_tags.cfg')
    parameters.print_cfg()

    opcListener = OPCListener(parameters, incomming_tags_subject, 5)
    opcListener.start_opc()

    messageTable = MessageTable(main_window, incomming_tags_subject)

    tagViewer = TagViewer(title=tv_title, size=tv_size,
                          incomming_tags_subject=incomming_tags_subject,
                          show_tag_viewer_subject=show_tag_viewer_subject)

    main_window.mainloop()
