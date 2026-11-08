// No dynamic allocation, loop() never blocks (Rule 9)
#include <Arduino.h>
#include <robot1_core.h>

#include "hw_watchdog.h"

constexpr uint32_t HW_WATCHDOG_MS = 1000;  // Well over longest loop, only a hang trips it
constexpr uint32_t REPORT_MS = 100;

robot1::Watchdog watchdog;
bool motorsAllowed = false;
int16_t left = 0, right = 0;
char line[32];
size_t length = 0;
uint32_t lastReport = 0;

void applyMotors(int16_t leftPct, int16_t rightPct) {
  // Fill in: board's motor driver, -100 to 100 %
  (void)leftPct;
  (void)rightPct;
}

void stopMotors() {
  left = right = 0;
  applyMotors(0, 0);
}

void setup() {
  Serial.begin(115200);
  stopMotors();
  motorsAllowed = hw_watchdog_begin(HW_WATCHDOG_MS);  // No hardware watchdog, no motors (Rule 8)
}

void loop() {
  hw_watchdog_feed();
  const uint32_t now = millis();
  while (Serial.available() > 0) {
    const char c = Serial.read();
    if (c == '\n') {
      line[length] = '\0';
      length = 0;
      int16_t l, r;
      if (motorsAllowed && robot1::parse_motor(line, &l, &r)) {
        left = l;
        right = r;
        applyMotors(left, right);
        watchdog.command(now);
      }
    } else if (length < sizeof(line) - 1) {
      line[length++] = c;
    } else {
      length = 0;
    }
  }
  if (watchdog.expired(now)) {
    stopMotors();
    watchdog.stopped();
  }
  if (now - lastReport >= REPORT_MS) {
    lastReport = now;
    Serial.print("A ");
    Serial.print(left);
    Serial.print(' ');
    Serial.println(right);
  }
}
