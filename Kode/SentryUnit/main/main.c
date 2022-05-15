/* Standard libraries */
#include <stdio.h>

#include "wifi.h"
#include "nvs_flash.h"
#include "cam.h"



void app_main(void)
{
  esp_err_t ret = nvs_flash_init();
  if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
    ESP_ERROR_CHECK(nvs_flash_erase());
    ret = nvs_flash_init();
  }

  ESP_ERROR_CHECK(ret);

  /*
    For some reason this is needed to initialize Camera...
    Don't know why, but it makes it work
   */
  printf("Free heap:%u\n",xPortGetFreeHeapSize());
  initCamera();

  connectWifi();

  /* xTaskCreatePinnedToCore(udpClientTask, "UDP Client", 4096,&takePic,5, NULL, 0 ); */
  xTaskCreatePinnedToCore(tcpServerTask, "TCP Server", 4096,NULL,5, NULL, 0 );
}
