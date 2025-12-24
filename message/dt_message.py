from datetime import datetime


class DtMessage:
    def __init__(self, message: str, tag: str):
        self.dt = datetime.min
        self._active = False
        self.message = message
        self.tag = tag
        self._confirm = True

    def __repr__(self):
        return '{0} / {1} / {2}'.format(self.dt_str(), self.tag, self.message)

    def dt_str(self):
        return self.dt.strftime("%d.%m.%Y %H:%M:%S")

    def set(self, active: bool, dt: datetime):
        if not self._active and active:
            self.dt = dt
        if active:
            self._confirm = False
        self._active = active

    def confirm(self):
        self._confirm = True

    def active(self):
        return self._active

    def confirmed(self):
        return self._confirm
