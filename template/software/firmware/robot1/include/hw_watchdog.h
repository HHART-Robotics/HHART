// Resets board if loop() hangs, software watchdog can't see that (Rule 8)
#pragma once

#include <stdint.h>

// False until implemented for board, motors stay off
bool hw_watchdog_begin(uint32_t timeout_ms);
void hw_watchdog_feed();
