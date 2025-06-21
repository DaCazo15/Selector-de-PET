int num = 0;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT); // Configura el pin 13 como salida
}

void loop() {
  if (Serial.available()) {
    String num_str = Serial.readStringUntil('\n'); 
    num = num_str.toInt();

    if (num == 1) {
      while (num == 1)
      {
        digitalWrite(13, HIGH); // Enciende el pin 13 si es "pet"
      }      
    } else {
      digitalWrite(13, LOW);  // Apaga el pin 13 en cualquier otro caso
    }
  }
}