from scapy.all import *
import struct

pcaps = PcapNgReader("./udpstream.pcapng")

caplist = pcaps.read_all()

imgpktlst = []

for i,x in enumerate(caplist[UDP]):
    if x.dport == 2024:
        imgpktlst.append(x)
        # payload = bytes(x.load)
        # header = payload[:20]
        # sequence, imgLen, datid, totalpackets, datalen = struct.unpack("IIIII", header)
        # print(f"[SEQ]: {sequence:>8}",
        #       f"[IMGLEND]: {imgLen:>8}", 
        #       f"[DATID]: {datid:>8}", 
        #       f"[TOTALPACKETS]: {totalpackets:>8} ", 
        #       f"[DATALEN]: {datalen:>8}")
        # data = payload[20:]
        # if datid == 0:
        #     for j in range(datalen):
        #         k = i + 1
        #         nxt_packet = caplist[UDP][k]
        #         while nxt_packet.dport != 2024:
        #             k += 1
        #             nxt_packet = pcaps[UDP][k]
imgpktlst = iter(imgpktlst)
for x in imgpktlst:
    payload = bytes(x.load)
    header = payload[:20]
    sequence, imgLen, datid, totalpackets, datalen = struct.unpack("IIIII", header)
    print(f"[SEQ]: {sequence:>8}",
          f"[IMGLEND]: {imgLen:>8}", 
          f"[DATID]: {datid:>8}", 
          f"[TOTALPACKETS]: {totalpackets:>8} ", 
          f"[DATALEN]: {datalen:>8}")
    data = payload[20:]
    if datid == 0:
        for j in range(datalen):
            nxt_packet = next(imgpktlst)
            nxt_header = struct.unpack("IIIII", nxt_packet.load[:20])
