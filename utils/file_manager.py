class FileManager:
    def __init__(self, file):
        self.file = open(file, 'r', encoding='utf-8')
        self.list = []

    def read_emissions(self):
        # Read table
        line = self.file.readline()
        while line[0:1] == '#':
            line = self.file.readline()
        for i in range(0, 40):
            line = line.strip('\n')
            links = line.split(',')
            self.list.append(links)
            line = self.file.readline()
        return self.list


def test():
    fm = FileManager("D:\\PyProject\\AI_HMM\\AI_HMM\\examples\\hmm_customer_1586733275442.txt")
    # print(fm.read_emissions())


test()
