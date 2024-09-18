#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include "hardware/clocks.h"
#include "hardware/gpio.h"

// Set the PWM pin
const uint PWM_PIN = 15;

// Function to initialize the PWM on the specified GPIO pin
void setup_pwm(uint gpio_pin, uint frequency) {
    // Set the PWM pin to output mode
    gpio_set_function(gpio_pin, GPIO_FUNC_PWM);

    // Get the PWM slice number (each PWM slice can control two pins)
    uint slice_num = pwm_gpio_to_slice_num(gpio_pin);

    // Set the PWM frequency
    uint32_t clock_freq = clock_get_hz(clk_sys);  // Get system clock frequency
    uint16_t wrap_value = clock_freq / frequency; // Calculate the wrap value for the given frequency
    pwm_set_wrap(slice_num, wrap_value);

    // Enable the PWM slice
    pwm_set_enabled(slice_num, true);
}

// Function to change PWM duty cycle
void set_pwm_duty(uint gpio_pin, uint16_t duty) {
    // Get the PWM slice number
    uint slice_num = pwm_gpio_to_slice_num(gpio_pin);

    // Set the duty cycle (maximum value is the wrap_value)
    pwm_set_gpio_level(gpio_pin, duty);
}

// Main function to test the PWM output
int main() {
    // Initialize stdio
    stdio_init_all();

    // Set up the PWM on GPIO 15 with a frequency of 1 kHz
    uint frequency = 10000; // 10 kHz
    setup_pwm(PWM_PIN, frequency);

    // Maximum duty cycle (this is the wrap_value calculated earlier)
    uint16_t max_duty = (clock_get_hz(clk_sys) / frequency) * 2;

    while (true) {
        // Sweep the duty cycle from low to high
        for (uint16_t duty = 0; duty < max_duty; duty += 1000) {
            set_pwm_duty(PWM_PIN, duty);
            sleep_ms(10);  // Delay for 10 milliseconds
        }

        // Sweep the duty cycle from high to low
        for (uint16_t duty = max_duty; duty > 0; duty -= 1000) {
            set_pwm_duty(PWM_PIN, duty);
            sleep_ms(10);  // Delay for 10 milliseconds
        }
    }

    return 0;
}
