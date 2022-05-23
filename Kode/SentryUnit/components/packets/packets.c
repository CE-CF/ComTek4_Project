#include <stdio.h>
#include "packets.h"

void dumpCmdPacket(CmdPacket packet){
  /* printf("Length: %u\n", sizeof(packet)); */
  printf("Yaw values:\n\tsign: %u\n\tspeed: %u\n\tangle: %u\n",
         packet.yawVals.sign, packet.yawVals.speed, packet.yawVals.angle);
  printf("Pitch values:\n\tsign: %u\n\tspeed: %u\n\tangle: %u\n",
         packet.pitchVals.sign, packet.pitchVals.speed, packet.pitchVals.angle);
}


pVals byte2pVal(unsigned int byte){
  pVals res = {
    .sign = (byte & 0b10000000) >> 7,
    .speed = (byte & 0b01100000) >> 5,
    .angle = (byte & 0b00011111),
  };
  return res;
}

CmdPacket char2packet(char *src){
  pVals yaw, pitch;
  yaw = byte2pVal(src[0] & 0xFF);
  pitch = byte2pVal(src[1] & 0xFF);

  CmdPacket result = {
    .yawVals = yaw,
    .pitchVals = pitch,
  };
  return result;
}
