#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "hardware/adc.h"
#include <hardware/gpio.h>
#include <pico/stdio.h>

#define POT_PIN 26
#define SWITCH_PIN 15

void init_serial() {
    uart_init(uart0, 115200);
    gpio_set_function(0, GPIO_FUNC_UART);
    gpio_set_function(1, GPIO_FUNC_UART);
}

void send_pot_value(){
    adc_select_input(0);
    uint16_t raw_value = adc_read();
    uint8_t pot_value = raw_value >> 4;
    uart_putc_raw(uart0, 'p');
    uart_putc_raw(uart0, pot_value);
}

void send_switch(bool state){
    uart_putc_raw(uart0, 's');
}

int main(){
    stdio_init_all();
    init_serial();

    adc_init();
    adc_gpio_init(POT_PIN);
    gpio_init(SWITCH_PIN);
    gpio_set_dir(SWITCH_PIN, GPIO_IN);
    gpio_pull_up(SWITCH_PIN);

    bool last_switch_state = true;

    while (true){
        send_pot_value();
        send_switch(last_switch_state);
        sleep_ms(100);
    }
}