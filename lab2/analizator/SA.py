import pickle

class SA:
    def __init__(self, config_path):
        config_file = open(config_path, "rb")
        config = pickle.load(config_file)
        self.syn_symbols = config[0]
        self.table = config[1]


if __name__ == '__main__':
    sa = SA('config')