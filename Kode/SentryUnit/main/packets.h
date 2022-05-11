#ifndef __PACKETS_H
#define __PACKETS_H

#include <stdbool.h>
#include <stdio.h>

#define IMG_SIZE 4096


typedef struct ImgPacket {
  unsigned int sequence : 32;
  char imgData[IMG_SIZE];
} ImgPacket;


/* 0
 * 0 1 2 3 4 5 6 7
 * +-+-+-+-+-+-+-+-+
 * |s|ya.|yaw angle|
 * +-+-+-+-+-+-+-+-+
 * |s|pi.|pitch an.|
 * +-+-+-+-+-+-+-+-+
 */
typedef struct pVals {
  unsigned int sign : 1;
  unsigned int speed : 2;
  unsigned int angle : 5;
} pVals;

typedef struct CmdPacket {
  pVals yawVals;
  pVals pitchVals;
} CmdPacket;

void dumpCmdPacket(CmdPacket packet){
  puts("[CmdPacket content]:");
  printf("Length: %u\n", sizeof(packet));
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
  pitch = byte2pVal(src[2] & 0xFF);

  CmdPacket result = {
    .yawVals = yaw,
    .pitchVals = pitch,
  };
  return result;
}

#endif
