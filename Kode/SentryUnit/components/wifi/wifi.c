#include "wifi.h"
#include "lwip/def.h"
#include "lwip/inet.h"
#include "lwip/sockets.h"
#include "esp_event.h"
#include "esp_event_base.h"
#include "esp_netif.h"
#include "esp_netif_types.h"
#include "esp_wifi.h"
#include "esp_wifi_default.h"
#include "esp_wifi_types.h"
#include "freertos/portmacro.h"
#include "freertos/projdefs.h"
#include "unistd.h"

const char *_TAG = "wifi_lib";
int retry_num = 0;

static void eventHandler(void *arg, esp_event_base_t event_base,
                         int32_t event_id, void *event_data){
  if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START)
      esp_wifi_connect();
  else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED){
    if (retry_num < WIFI_MAX_RETRIES){
      esp_wifi_connect();
      retry_num++;
      ESP_LOGI(_TAG, "Retrying AP connection");
    } else {
      xEventGroupSetBits(wifi_event_group, WIFI_FAIL_BIT);
    }
    ESP_LOGI(_TAG, "Connection failed");
  }
  else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP){
    ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
    ESP_LOGI(_TAG, "Got ip:" IPSTR, IP2STR(&event->ip_info.ip));
    retry_num = 0;
    xEventGroupSetBits(wifi_event_group, WIFI_CONNECTED_BIT);
  }
}




void connectWifi(){
  wifi_event_group = xEventGroupCreate();

  /* Init network interface */
  ESP_ERROR_CHECK(esp_netif_init());

  ESP_ERROR_CHECK(esp_event_loop_create_default());
  esp_netif_create_default_wifi_sta();
  
  wifi_init_config_t config = WIFI_INIT_CONFIG_DEFAULT();
  ESP_ERROR_CHECK(esp_wifi_init(&config));

  esp_event_handler_instance_t instance_any_id;
  esp_event_handler_instance_t instance_got_ip;

  ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT,
                                                    ESP_EVENT_ANY_ID,
                                                    &eventHandler,
                                                    NULL,
                                                    &instance_any_id));
  
  ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT,
                                                    IP_EVENT_STA_GOT_IP,
                                                    &eventHandler,
                                                    NULL,
                                                    &instance_got_ip));

  /* Setup and connect to wifi */
  wifi_config_t wifi_config = {
    .sta = {
      .ssid = SSID,
      .password = PASS,
      .threshold.authmode = WIFI_AUTH_WPA2_PSK,
    },
  };

  ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
  ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
  ESP_ERROR_CHECK(esp_wifi_start());

  EventBits_t bits = xEventGroupWaitBits(wifi_event_group,
                       WIFI_CONNECTED_BIT | WIFI_FAIL_BIT,
                                         pdFALSE,
                                         pdFALSE,
                                         portMAX_DELAY);

  if (bits & WIFI_CONNECTED_BIT) {
    ESP_LOGI(_TAG, "Connected to AP: %s, PASS: %s",
             SSID, PASS);
  } else if (bits & WIFI_FAIL_BIT) {
    ESP_LOGI(_TAG, "Failed to connect to AP: %s, with PASS: %s",
             SSID, PASS);
  } else {
    ESP_LOGE(_TAG, "IDK WHAT HAPPENED");
  }

  
}

// TODO: Setup UDP client for videofeed
void udpClientTask(void *pvParameters){
  char rcv_buf[128];
  char host_ip[] = EDGE_IP;
  int addr_family = AF_INET;
  int ip_protocol = IPPROTO_IP;

  while(1){
    struct sockaddr_in dest_addr;
    dest_addr.sin_addr.s_addr = inet_addr(EDGE_IP);
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(UDP_PORT);



    int sock = socket(addr_family, SOCK_DGRAM, ip_protocol);
    if (sock < 0){
      ESP_LOGE(_TAG, "Couldn't create socket");
      break;
    }
    ESP_LOGI(_TAG, "Socket created, sending to %s:%d", EDGE_IP, UDP_PORT);

    while(1){
      ImgPacket payload;
      void (*tp) (ImgPacket*)=pvParameters;
      tp(&payload);
      int err = sendto(sock, &payload, sizeof(payload), 0, (struct sockaddr*)&dest_addr, sizeof(dest_addr));
      if (err < 0){
        ESP_LOGE(_TAG, "Error occured during send off errno: %d", errno);
        break;
      }
      vTaskDelay(2000 / portTICK_PERIOD_MS);
    }

    
    
  }
  vTaskDelete(NULL);
}

// TODO: Setup TCP client for cmds
