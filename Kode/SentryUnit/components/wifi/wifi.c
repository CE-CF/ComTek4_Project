#include "wifi.h"
#include "cam.h"
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
#include "packets.h"
#include "string.h"
#include "unistd.h"
#include "math.h"

const char *WIFI_TAG = "wifi_lib";
int retry_num = 0;

static void eventHandler(void *arg, esp_event_base_t event_base,
                         int32_t event_id, void *event_data){
  if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START)
      esp_wifi_connect();
  else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED){
    if (retry_num < WIFI_MAX_RETRIES){
      esp_wifi_connect();
      retry_num++;
      ESP_LOGI(WIFI_TAG, "Retrying AP connection");
    } else {
      xEventGroupSetBits(wifi_event_group, WIFI_FAIL_BIT);
    }
    ESP_LOGI(WIFI_TAG, "Connection failed");
  }
  else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP){
    ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
    ESP_LOGI(WIFI_TAG, "Got ip:" IPSTR, IP2STR(&event->ip_info.ip));
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
    ESP_LOGI(WIFI_TAG, "Connected to AP: %s, PASS: %s",
             SSID, PASS);
  } else if (bits & WIFI_FAIL_BIT) {
    ESP_LOGI(WIFI_TAG, "Failed to connect to AP: %s, with PASS: %s",
             SSID, PASS);
  } else {
    ESP_LOGE(WIFI_TAG, "IDK WHAT HAPPENED");
  }

  
}

// TODO: Setup UDP client for videofeed
void udpClientTask(void *pvParameters){
  int addr_family = AF_INET;
  int ip_protocol = IPPROTO_IP;

  ImgPacket *payload;
  ImgData *data;
  data = (ImgData *) malloc(sizeof(ImgData));
  payload = (ImgPacket *) malloc(sizeof(ImgPacket));
  const size_t buflen = sizeof(payload->dat);
  const size_t headerSize = sizeof(ImgPacket) - buflen;

  ESP_LOGI(WIFI_TAG, "LEFTOVER HEAP SPACE: %u", xPortGetFreeHeapSize());
  while(1){
    struct sockaddr_in dest_addr;
    dest_addr.sin_addr.s_addr = inet_addr(EDGE_IP);
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(UDP_PORT);



    int sock = socket(addr_family, SOCK_DGRAM, ip_protocol);
    if (sock < 0){
      ESP_LOGE(WIFI_TAG, "Couldn't create socket");
      break;
    }
    ESP_LOGI(WIFI_TAG, "Socket created, sending to %s:%d", EDGE_IP, UDP_PORT);
    payload->sequence = 0;

    while(1){
      void (*tp) (ImgData*)=pvParameters;
      tp(data);
      /*
        Split data into multiple packets
       */
      payload->maxPackets = (unsigned int)
        ceil((float) data->imgLen/buflen);
      payload->imgLen = data->imgLen;
      payload->datLen = buflen;

      ESP_LOGI(WIFI_TAG, "Got pic with len: %u, splitting into: %u",
               payload->imgLen, payload->maxPackets);
      for (int j = 0; j <= payload->maxPackets - 1; j++){
        payload->datId = j; // Set split packet id

        // Load image data into 
        ESP_LOGI(WIFI_TAG, "Loading data into packet %u of %u", j +1,
                 payload->maxPackets);
        for (int i = 0; i < buflen-1; i++){
          if (i > payload->imgLen - buflen*j){
            payload->datLen = i;
            goto send;
          }
          payload->dat[i] = *data->imgData;
          data->imgData++;
        }

      send:
        ESP_LOGI(WIFI_TAG, "Data len: %u", payload->datLen);
        // =====================================================
        // Send split packets to Edge node, and check for errors
        size_t packetSize = headerSize + payload->datLen;
        ESP_LOGI(WIFI_TAG, "Sending packet %u of %u, with size %u", j + 1,
                 payload->maxPackets, packetSize);
        int err = sendto(sock, payload, packetSize, 0,
                         (struct sockaddr*)&dest_addr, sizeof(dest_addr));


        memset(payload->dat,0,buflen); //Clear data array
        if (err < 0){
          ESP_LOGE(WIFI_TAG, "Error occured during send off errno: %d", errno);
          break;
        }


        ESP_LOGI(WIFI_TAG, "DONE with packet: %u, SEQ: %u", j + 1, payload->sequence);
      }
      // Free image data from heap, as the next image can have different length
      data->imgData = NULL;
      // Return and free the frame buffer
      returnCam();

      ESP_LOGI(WIFI_TAG, "===========================================");
      payload->sequence++; // Increment sequence
      /* vTaskDelay((1000/15) / portTICK_PERIOD_MS); */
      vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
    
    
  }
  free(data);
  free(payload);
  vTaskDelete(NULL);
}
void handlePacket(const int sock){
  int len;
  char rcvPacket[5];

  do{
    len = recv(sock, rcvPacket, sizeof(rcvPacket)-1, 0);
    if (len < 0){
      ESP_LOGE(WIFI_TAG, "Error occurred during receiving: errno %d", errno);
    } else if (len == 0) {
      ESP_LOGW(WIFI_TAG, "Connection closed");
    } else {
      rcvPacket[len] = 0; // Null-terminate whatever is received and treat it like a string
      ESP_LOGI(WIFI_TAG, "Received %d bytes: %s", len, rcvPacket);

      CmdPacket rcvCmds = char2packet(rcvPacket);
      dumpCmdPacket(rcvCmds);

      // send() can return less bytes than supplied length.
      // Walk-around for robust implementation.
      /* int to_write = len; */
      /* while (to_write > 0) { */
      /*   int written = send(sock, rx_buffer + (len - to_write), to_write, 0); */
      /*   if (written < 0) { */
      /*     ESP_LOGE(WIFI_TAG, "Error occurred during sending: errno %d", errno); */
      /*   } */
      /*   to_write -= written; */
      /* } */
    }
  }while (len > 0);
}

// TODO: Setup TCP client for cmds
void  tcpServerTask(void *pvParameters){
  char addr_str[128];
  int addr_family = AF_INET;
  int ip_protocol = IPPROTO_IP;
  int keepAlive = 1;
  int keepIdle = 5;
  int keepInterval = 5;
  int keepCount = 3;


  struct sockaddr_in dest_addr;
  dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
  dest_addr.sin_family = addr_family;
  dest_addr.sin_port = htons(TCP_PORT);

  int lsock = socket(addr_family, SOCK_STREAM, ip_protocol);
  if (lsock < 0){
       ESP_LOGE(WIFI_TAG, "Unable to create socket: errno %d", errno);
       vTaskDelete(NULL);
       return;
  }
  int opt = 1;
  setsockopt(lsock, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

  ESP_LOGI(WIFI_TAG, "Socket created");

  int err = bind(lsock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
  if (err != 0) {
    ESP_LOGE(WIFI_TAG, "Unable to bind socket: errno %d", errno);
    goto clean_up;
  }
  ESP_LOGI(WIFI_TAG, "Socket bound to port: %d", TCP_PORT);

  err = listen(lsock, 1);
  if (err != 0){
    ESP_LOGE(WIFI_TAG, "Error occured during listen: errno %d", errno);
    goto clean_up;
  }

  while(1){
    ESP_LOGI(WIFI_TAG, "Socket listening");

    struct sockaddr src_addr;
    socklen_t addr_len = sizeof(src_addr);
    int sock = accept(lsock, &src_addr, &addr_len);
    if (sock < 0){
      ESP_LOGE(WIFI_TAG, "Can't accept connection: errno %d", errno);
      break;
    }

    setsockopt(sock, SOL_SOCKET, SO_KEEPALIVE, &keepAlive, sizeof(int));
    setsockopt(sock, IPPROTO_TCP, TCP_KEEPIDLE, &keepIdle, sizeof(int));
    setsockopt(sock, IPPROTO_TCP, TCP_KEEPINTVL, &keepInterval, sizeof(int));
    setsockopt(sock, IPPROTO_TCP, TCP_KEEPCNT, &keepCount, sizeof(int));

    inet_ntoa_r(((struct sockaddr_in *)&src_addr)->sin_addr, addr_str, sizeof(addr_str) - 1);
    ESP_LOGI(WIFI_TAG, "Socket accepted IP adress: %s", addr_str);

    handlePacket(sock);
    shutdown(sock, 0);
    close(sock);
  }
  
 clean_up:
  close(lsock);
  vTaskDelete(NULL);
}


