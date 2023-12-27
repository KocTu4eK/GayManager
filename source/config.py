import json


class Config:
    __config = None
    __filename = None

    @classmethod
    def load(cls, filename):
        file = open(filename, "a+", encoding="utf-8")
        file.seek(0)

        data = file.read()
        if data == "":
            file.write(r"{}")
            file.close()
            data = r"{}"

        cls.__config = json.loads(data)
        cls.__filename = filename

        return list(cls.__config)

    @classmethod
    def save(cls):
        file = open(cls.__filename, "w")
        file.write(json.dumps(cls.__config, indent=4))
        file.close()

    @classmethod
    def get(cls, key):
        return cls.__config[key]

    @classmethod
    def add(cls, key, data):
        cls.__config[key] = data

    @classmethod
    def remove(cls, key):
        del cls.__config[key]
