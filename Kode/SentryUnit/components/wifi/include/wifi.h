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
#include "packets.h"

#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "freertos/task.h"

EventGroupHandle_t wifi_event_group;

#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT BIT1
#define WIFI_MAX_RETRIES 10

#define PASS "SentryUnit"
#define SSID "451_RPT"



#define EDGE_IP "192.168.1.188"
#define UDP_PORT 2024
#define TCP_PORT 2025

void connectWifi();

/*
  pvParameters should be a reference to the function which takes the pictures
 */
void udpClientTask(void *pvParameters);

#endif
