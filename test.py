listClass = []
with open("DanhSach.txt", "r") as f:
    for line in f.readlines():
        line = line[0:-1]
        line.strip()
        listClass.append(line)
    print(listClass)

if "6" in listClass:
    print('có')