#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/pwm.h"
#include <hardware/gpio.h>
#include <stdio.h>

const int ADC_PIN = 26;
const int PWM_PIN = 15;

int main(){
    // Init stdio
    stdio_init_all();

    // Init ADC
    adc_init();
    adc_gpio_init(ADC_PIN);
    adc_select_input(0);

    // Setup PWM for pin 15
    gpio_set_function(PWM_PIN, GPIO_FUNC_PWM);
    uint slice_num = pwm_gpio_to_slice_num(PWM_PIN);
    pwm_set_wrap(slice_num, 65535); // 16 bit
    pwm_set_enabled(slice_num, true);

    while(true){
        uint16_t adc_value = adc_read();
        pwm_set_gpio_level(PWM_PIN, adc_value << 4);
        
        sleep_ms(100); // Effective sample rate
    }

    return 0;
}