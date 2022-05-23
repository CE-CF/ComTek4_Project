import os

def namesplit(fname):
    seq = fname.split('_')
    datid = seq[1].split('.')[0]
    seq = seq[0]
    return int(seq), int(datid)
path = "./bytes/"
datlist = os.listdir(path)
datlist.sort(key=lambda fname: int(fname.split('_')[0] + fname.split('_')[1].split('.')[0]))

for i in range(len(datlist)):
    fname = datlist[i]
    seq, datid = namesplit(fname)
    if datid == 0:
        fname2 = datlist[i + 1]
        seq2, datid2 = namesplit(fname2)
        if seq == seq2:
            with open(path + fname, 'rb') as f1:
                with open(path + fname2, 'rb') as f2:
                    buf1 = f1.read()
                    buf2 = f2.read()
                    with open(f"./imgs/{seq}.jpeg", 'wb') as jpg:
                        buf1 = bytearray(buf1)
                        buf2 = bytearray(buf2)
                        jpg.write(buf1 + buf2)
