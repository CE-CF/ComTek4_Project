#include "wifi.h" 
#include "esp_event.h"
#include "esp_event_base.h"
#include "esp_netif.h"
#include "esp_netif_types.h"
#include "esp_tls.h"
#include "esp_wifi.h"
#include "esp_wifi_default.h"
#include "esp_wifi_types.h"
#include "freertos/portmacro.h"
#include "freertos/projdefs.h"

static void eventHandler(void *arg, esp_event_base_t event_base, int32_t event_id, void event_data){
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




void connectWifi(char *SSID, char *PASS){
  wifi_event_group = xEventGroupCreate();

  /* Init network interface */
  ESP_ERR_CHECK(esp_netif_init());

  ESP_ERR_CHECK(esp_event_loop_create_default());
  esp_netif_create_default_wifi_sta();
  
  wifi_init_config_t config = WIFI_INIT_CONFIG_DEFAULT();
  ESP_ERR_CHECK(esp_wifi_init(&config));

  esp_event_handler_instance_t instance_any_id;
  esp_event_handler_instance_t instance_got_ip;

  ESP_ERR_CHECK(esp_event_handler_instance_register(WIFI_EVENT,
                                                    ESP_EVENT_ANY_ID,
                                                    &event_handler,
                                                    NULL,
                                                    &instance_any_id));
  
  ESP_ERR_CHECK(esp_event_handler_instance_register(IP_EVENT,
                                                    IP_EVENT_STA_GOT_IP,
                                                    &event_handler,
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

  ESP_ERR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
  ESP_ERR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
  ESP_ERR_CHECK(esp_wifi_start());

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
