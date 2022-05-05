#include "wifi.h" 

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
