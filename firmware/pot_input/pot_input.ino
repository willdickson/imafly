const int AIN_PIN = A0;
const int AIN_READ_RESOLUTION = 16;
const int AIN_READ_AVERAGING = 32; 
const uint16_t AIN_MAX_INT = uint16_t((uint32_t(1) << AIN_READ_RESOLUTION) -1);
const float AIN_MAX_VOLT = 3.3; 

float ain_uint16_to_volt(uint16_t int_value);

void setup() {
    Serial.begin(115200);
    analogReadResolution(AIN_READ_RESOLUTION);
    analogReadAveraging(AIN_READ_AVERAGING);
    delay(1000);
}

void loop() {
    static bool running = false;
    static uint8_t cnt = 0;
    while (Serial.available() > 0) {
        uint8_t cmd = Serial.read();
        switch (cmd) {
            case 'b':
                running = true;
                break;
            case 'e':
                running = false;
                break;
            default:
                break;

        }
    }
    if (running) {
        uint16_t ain_int = analogRead(AIN_PIN);
        float volt = ain_uint16_to_volt(ain_int);
        Serial.println(volt,6);
    }
    delay(5);
}

float ain_uint16_to_volt(uint16_t int_value) {
    return AIN_MAX_VOLT*float(int_value)/float(AIN_MAX_INT);
}
