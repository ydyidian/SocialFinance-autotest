import json


class Data:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def p_data(self):
        print(f"名字：{self.name},年龄：{self.age}")


class CopyData(Data):
    def __init__(self, name, age, add):
        # super(CopyData, self).__init__(name, age)
        super().__init__(name, age)
        self.add = add

    def ttt(self):
        print(f"{self.name},{self.age},{self.add}")


if __name__ == '__main__':
    import sys
    print(sys.platform)
    c = CopyData("lisi", "15", "henan")
    c.ttt()
    c.p_data()
