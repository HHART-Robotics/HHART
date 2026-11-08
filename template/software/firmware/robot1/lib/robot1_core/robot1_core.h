// No hardware headers, so it builds and tests on host (Rule 9)
#pragma once

#include <stdint.h>

namespace robot1 {

constexpr uint32_t WATCHDOG_MS = 500;  // W, must exceed host resend period P (Rule 8)

class Watchdog {
 public:
  void command(uint32_t now_ms) {
    last_ms_ = now_ms;
    armed_ = true;
  }
  // Unsigned subtraction survives millis() wrap
  bool expired(uint32_t now_ms) const { return armed_ && now_ms - last_ms_ >= WATCHDOG_MS; }
  void stopped() { armed_ = false; }

 private:
  uint32_t last_ms_ = 0;
  bool armed_ = false;
};

// Must match core/protocol.py (Rule 4)
inline bool parse_motor(const char* line, int16_t* left, int16_t* right) {
  if (line[0] != 'M' || line[1] != ' ') return false;
  const char* p = line + 2;
  int16_t value[2];
  for (int i = 0; i < 2; ++i) {
    const bool negative = *p == '-';
    if (negative) ++p;
    if (*p < '0' || *p > '9') return false;
    int16_t n = 0;
    while (*p >= '0' && *p <= '9') {
      n = n * 10 + (*p++ - '0');
      if (n > 100) return false;
    }
    value[i] = negative ? -n : n;
    if (i == 0 && *p++ != ' ') return false;
  }
  if (*p != '\0' && *p != '\r') return false;
  *left = value[0];
  *right = value[1];
  return true;
}

}  // namespace robot1
