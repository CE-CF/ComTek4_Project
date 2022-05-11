#pragma once
#ifndef __PACKETS_H
#define __PACKETS_H

#include <stdbool.h>
#include <stdio.h>



typedef struct ImgPacket {
  unsigned int sequence : 32;
  size_t imgLen;
  uint8_t *imgData;
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

void dumpCmdPacket(CmdPacket packet);

pVals byte2pVal(unsigned int byte);
CmdPacket char2packet(char *src);
#endif
