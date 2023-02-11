class His():
    def __init__(self):
        self.username=''
        self.password=''
        self.win=0
        self.Def=0
        self.score=0
        self.bua=0
        self.vt=0
        self.my_list=[]
        self.doc()
    def doc(self):
        with open('vd.txt', 'r') as f:
            data = f.read()
            my = data.splitlines()
            f.seek(0, 0)
        f.close()
        self.username = my[0]

        with open('user.txt', 'r') as ff:
            data1 = ff.read()
        self.my_list = data1.splitlines()
        ff.close()
        i=0
        a=[]
        while i < len(self.my_list):
              if self.username == self.my_list[i]:

                  self.vt = i+2
                  a =self.my_list[self.vt].split()
                  a[0] = int(a[0]) # thắng
                  a[1] = int(a[1]) # thua
                  a[2] = int(a[2]) # điểm
                  a[3] = int(a[3]) #bùa
                  self.win=a[0]
                  self.Def=a[1]
                  self.score=a[2]
                  self.bua=a[3]

              i+=3
    def update(self):
        j=1

        self.my_list[self.vt] = str(self.win) + ' ' + str(self.Def) + ' ' + str(self.score) + ' ' + str(self.bua)
        with open('user.txt', 'w') as f:
            f.write(self.my_list[0])
            while j < len(self.my_list):
                f.write("\n" + self.my_list[j])
                j += 1
            f.close()

    def main(self):


        print('thang: ')
        self.win = int(input())
        self.update()
h=His()
h.main()
