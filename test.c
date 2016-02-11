
#include "ufloat8.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>


bool test() {
    int32_t previous_value = -1;
    bool passed = true;
    for (int i=0; i<256; i++) {
        uint8_t fl = i;
        int32_t value = ufloat8_dec(fl);
        uint8_t fl2 = ufloat8_enc(value);
        if (fl != fl2) {
            printf("%02x: produces value %d but encodes back to %02x\n", fl, value, fl2);
            passed = false;
        }
        if (value <= previous_value) {
            printf("%02x: value %d <= previous_value %d\n", fl, value, previous_value);
            passed = false;
        }
        previous_value = value;
    }
    return passed;
}

int main() {
    if (test()) {
        printf("All tests passed.\n");
        exit(0);
    }
    exit(1);
}
