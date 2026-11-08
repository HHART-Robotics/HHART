#include <robot1_core.h>
#include <unity.h>

using robot1::Watchdog;
using robot1::WATCHDOG_MS;
using robot1::parse_motor;

void setUp() {}
void tearDown() {}

void test_unarmed_never_expires() {
  Watchdog w;
  TEST_ASSERT_FALSE(w.expired(1000000));
}

void test_expires_w_after_the_last_command() {
  Watchdog w;
  w.command(100);
  TEST_ASSERT_FALSE(w.expired(100 + WATCHDOG_MS - 1));
  TEST_ASSERT_TRUE(w.expired(100 + WATCHDOG_MS));
}

void test_a_command_restarts_it() {
  Watchdog w;
  w.command(0);
  w.command(400);
  TEST_ASSERT_FALSE(w.expired(400 + WATCHDOG_MS - 1));
}

void test_survives_millis_wrapping() {
  Watchdog w;
  w.command(0xFFFFFF00u);
  TEST_ASSERT_FALSE(w.expired(0x00000010u));
  TEST_ASSERT_TRUE(w.expired(0xFFFFFF00u + WATCHDOG_MS));
}

void test_stopped_disarms() {
  Watchdog w;
  w.command(0);
  w.stopped();
  TEST_ASSERT_FALSE(w.expired(WATCHDOG_MS * 10));
}

void test_parses_a_motor_command() {
  int16_t l = 0, r = 0;
  TEST_ASSERT_TRUE(parse_motor("M -40 100", &l, &r));
  TEST_ASSERT_EQUAL_INT16(-40, l);
  TEST_ASSERT_EQUAL_INT16(100, r);
  TEST_ASSERT_TRUE(parse_motor("M 0 0\r", &l, &r));
}

void test_refuses_anything_else_and_leaves_the_last_command() {
  int16_t l = 7, r = 7;
  const char* bad[] = {"", "M", "M 10", "M 101 0", "M -1000 0", "M 10 x", "M 10 10 10", "A 10 10", "M  10 10"};
  for (const char* line : bad) TEST_ASSERT_FALSE_MESSAGE(parse_motor(line, &l, &r), line);
  TEST_ASSERT_EQUAL_INT16(7, l);
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_unarmed_never_expires);
  RUN_TEST(test_expires_w_after_the_last_command);
  RUN_TEST(test_a_command_restarts_it);
  RUN_TEST(test_survives_millis_wrapping);
  RUN_TEST(test_stopped_disarms);
  RUN_TEST(test_parses_a_motor_command);
  RUN_TEST(test_refuses_anything_else_and_leaves_the_last_command);
  return UNITY_END();
}
