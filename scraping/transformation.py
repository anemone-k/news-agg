
class Transformation:
    def del_punctuation(data):
        data = data.replace(".", " ")
        data = data.replace(",", " ")
        data = data.replace("-", " ")
        data = data.replace("—", " ")
        data = data.replace("–", " ")
        data = data.replace("?", " ")
        data = data.replace("'", " ")
        data = data.replace('"', " ")
        data = data.replace('!', " ")
        data = data.replace(':', " ")
        data = data.replace('(', " ")
        data = data.replace(')', " ")
        data = data.replace('>', " ")
        data = data.replace('<', " ")
        data = data.replace('/', " ")
        data = data.replace('\\', " ")
        data = data.replace(';', " ")
        return data
    del_punctuation = staticmethod(del_punctuation)