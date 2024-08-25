import yaml
import os
from common.file_path import fp


class YamlData(object):
    def __init__(self, file_yaml):
        self.file_yaml = file_yaml
        self.path_data = fp.data_file_path()
        self.path = os.path.join(self.path_data, file_yaml)

    def read_yaml(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            # 读取，此时读取出来的是字符串
            data = f.read()
            # 将读取的内容转化成字典
            # 添加Loader=yaml.FullLoader，不然会有warning
            result = yaml.load(data, Loader=yaml.FullLoader)
            return result

    def wierd_yaml(self, aproject):
        with open(self.path, 'w', encoding='utf-8') as f1:
            # 字符串写入yaml中
            yaml.dump(aproject, f1, default_flow_style=False, encoding='utf-8', allow_unicode=True)

    def clear_yaml(self):
        with open(self.path, 'w', encoding='utf-8') as f2:
            f2.truncate()


if __name__ == '__main__':
    yaml_data = YamlData("tc.yaml")
    data = {
        "token": "222222222222"
    }
    yaml_data.wierd_yaml(data)
    # print(yaml_data.read_yaml())
    # yaml_data.clear_yaml()
    print(yaml_data.read_yaml())
