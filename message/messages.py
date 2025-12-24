from message.dt_message import DtMessage
from opc.parameters import Parameters
from rx.subjects import Subject
from dateutil import parser



class Messages:
    def __init__(self, parameters: Parameters, incomming_subject: Subject):
        self.incomming_subject = incomming_subject
        self.incomming_subject.subscribe(lambda tag_info: self._newTagInfo(tag_info))
        self.strokes = []
        for key, value in parameters.messages.items():
            dt_message = DtMessage(value, key)
            self.strokes.append(dt_message)


    def _newTagInfo(self, tag_info):
        if len(tag_info) != 4:
            print('Wrong signal, wrong len(tuple)')
            return
        tag = tag_info[0]
        value = tag_info[1]
        status = tag_info[2]
        date_time = parser.parse(tag_info[3])
        if status != 'Good' and type(value) != bool:
            print('Wrong signal, BAD or not bool')
            return
        for stroke in self.strokes:
            if stroke.tag == tag:
                stroke.set(value, date_time)
                break
        print(self.strokes)
