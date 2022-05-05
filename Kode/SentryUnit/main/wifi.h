/*
 * The network connection part of this library is heavily inspired by the getting
 * started source code created by espressif themselves for the ESP32.
 * As they themselves recommend, as creating robust WiFi Applications can be
 * quite the challenge, if one doesn't handle bad scenarios.
 */
#ifndef __WIFI_LIB_H
#define __WIFI_LIB_H


/* ESP libraries */
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"

static const char *_TAG = "wifi connector";
static EventGroupHandle_t wifi_event_group;

#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT BIT1
#define WIFI_MAX_RETRIES 10

static int retry_num = 0;

void connectWifi(char *SSID, char *PASS);



#endif
