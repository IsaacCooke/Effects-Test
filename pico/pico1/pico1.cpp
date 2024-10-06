#include "pico/stdlib.h"
#include "hardware/adc.h"
#include <pico/time.h>
#include <stdio.h>

const uint ADC_PIN = 26;

int main(){
    stdio_init_all();

    // Init ADC
    adc_init();

    adc_gpio_init(ADC_PIN);
    adc_select_input(0);

    while (true){
        uint16_t result = adc_read();
        printf("ADC Value: %d\n", result);
        sleep_ms(10);
    }
}