class Parameters:
    def __init__(self, path: str):
        self.messages = {}
        with open(path, 'r') as f:
            content = f.read()
        strokes = content.split("\n")
        num_of_strokes = len(strokes)
        if num_of_strokes < 4:
            raise Exception("wrong config: num of strokes or empty file " + path)
        self.OPCname = self._getPar(strokes[0], "OPCname")
        self.group = self._getPar(strokes[1], "group")
        self.prefix = self._getPar(strokes[2], "prefix")
        for i in range(3, num_of_strokes):
            pair = self._getPair(self.prefix + strokes[i])
            self.messages[pair[0]] = pair[1]
        self.tags = list(self.messages.keys())


    def _getPar(self, stroke: str, name: str):
        pair = stroke.split("@")
        if len(pair) != 2 and name != pair[0]:
            raise Exception("wrong config: parameter " + stroke)
        return pair[1]

    def _getPair(self, stroke: str):
        pair = stroke.split("@")
        if len(pair) != 2:
            raise Exception("wrong config: parameter " + stroke)
        return pair

    def print_cfg(self):
        print(self.OPCname, self.group, self.messages)
