#include "hw_watchdog.h"

// Fill in per board: Teensy 4 WDOG1 or RTWDOG, AVR <avr/wdt.h>, ESP32 esp_task_wdt
bool hw_watchdog_begin(uint32_t timeout_ms) {
  (void)timeout_ms;
  return false;
}

void hw_watchdog_feed() {}
