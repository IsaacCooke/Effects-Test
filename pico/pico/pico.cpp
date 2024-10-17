#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/pwm.h"
#include <pico/stdio.h>

const uint ADC_PIN = 26;
const uint PWM_PIN = 15;

const float GAIN = 1.5;

uint pwm_slice_num;

void setup_pwm_output(){
    // Set up GPIO 15
    gpio_set_function(PWM_PIN, GPIO_FUNC_PWM);
    pwm_slice_num = pwm_gpio_to_slice_num(PWM_PIN);

    // Set frequency
    pwm_set_wrap(pwm_slice_num, 255);
    pwm_set_gpio_level(PWM_PIN, 0);
    pwm_set_enabled(pwm_slice_num, true);
}

void setup_adc_input(){
    adc_init();
    adc_gpio_init(ADC_PIN);
    adc_select_input(0);
}

int main(){
    stdio_init_all();

    setup_adc_input();
    setup_pwm_output();

    while (true){
        uint16_t adc_value = adc_read();

        float processed_signal = (float)adc_value * GAIN;

        if (processed_signal > 4095){
            processed_signal = 4095;
        } else if (processed_signal < 0){
            processed_signal = 0;
        }

        uint16_t pwm_value = (uint16_t)(processed_signal / 16);

        pwm_set_gpio_level(PWM_PIN, pwm_value);

        sleep_us(50);
    }

    return 0;
}