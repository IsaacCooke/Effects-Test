// #include "pico/stdlib.h"
// #include "hardware/pwm.h"
// #include <cstdint>
// #include <hardware/gpio.h>
// #include <hardware/structs/io_bank0.h>
// #include <cmath>
// #include <pico/stdio.h>
// #include <pico/time.h>

// const uint PWM_PIN = 16;

// void setup_pwm(uint slice_num, uint channel){
//     pwm_set_wrap(slice_num, 4095);
//     pwm_set_enabled(slice_num, true);
// }

// int main(){
//     stdio_init_all();
//     gpio_set_function(PWM_PIN, GPIO_FUNC_PWM);
    
//     uint slice_num = pwm_gpio_to_slice_num(PWM_PIN);
//     uint channel = pwm_gpio_to_channel(PWM_PIN);

//     setup_pwm(slice_num, channel);

//     const float frequency = 440.0;
//     const int amplitude = 2048;
//     const int offset = 2048;

//     const float sample_rate = 10000.0;
//     const float increment = 2 * M_PI * frequency * sample_rate;

//     float phase = 0.0;

//     while (true){
//         int16_t sine_wave = (int16_t)(amplitude * sin(phase)) + offset;

//         pwm_set_chan_level(slice_num, channel, sine_wave);

//         phase

//         sleep_us(1000000 / sample_rate);
//     }
// }

#include "pico/stdlib.h"

const uint LED_PIN = 0;

int main(){
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    while (1){
        gpio_put(LED_PIN, 0);
        sleep_ms(250);
        gpio_put(LED_PIN, 1);
        sleep_ms(1000);
    }
}