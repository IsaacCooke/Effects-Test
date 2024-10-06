#include "pico/stdlib.h"
#include "hardware/adc.h"
#include <stdio.h>

const uint ADC_PIN = 26;  // Use GPIO 26 (ADC0)

int main() {
    // Initialize stdio to see values printed on the console
    stdio_init_all();

    // Initialize the ADC hardware on the Pico
    adc_init();

    // Select the GPIO pin for the ADC input (ADC0 -> GPIO 26)
    adc_gpio_init(ADC_PIN);

    // Select the ADC input (input 0 corresponds to GPIO 26)
    adc_select_input(0);

    // Start an infinite loop to continuously read and display the ADC value
    while (true) {
        // Read the ADC value (12-bit result: 0-4095)
        uint16_t result = adc_read();

        // Print the result to the serial monitor
        printf("ADC Value: %d\n", result);

        // Wait for a short time before sampling again
        sleep_ms(10);  // Sample every 10 milliseconds
    }

    return 0;
}
