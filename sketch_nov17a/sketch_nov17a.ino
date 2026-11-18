
/*
==============================================
       PROYECTO INTEGRADOR - CAJA FUERTE
==============================================

Arduino Mega 2560

Potenciometro 1 -> A0
Potenciometro 2 -> A1
Potenciometro 3 -> A2

Comunicacion serial con Python mediante USB.

Los valores se envian solamente cuando los
tres potenciometros permanecen estables.
*/


// ==========================================
// CONFIGURACION
// ==========================================

// Pines analogicos de los potenciometros

const int POT1 = A0;
const int POT2 = A1;
const int POT3 = A2;


// Velocidad de comunicacion serial

const int VELOCIDAD = 9600;


// Tiempo que deben permanecer quietos
// los potenciometros para enviar los datos

const unsigned long TIEMPO_ESTABLE = 000;


// Tolerancia para evitar que el ruido
// electrico reinicie constantemente el tiempo

const int TOLERANCIA = 5;


// Intervalo entre lecturas

const unsigned long INTERVALO_LECTURA = 15;


// ==========================================
// VARIABLES
// ==========================================

// Lecturas actuales

int valor1 = 0;
int valor2 = 0;
int valor3 = 0;


// Valores de referencia para detectar movimiento

int referencia1 = 0;
int referencia2 = 0;
int referencia3 = 0;


// Variables de tiempo

unsigned long ultimoMovimiento = 0;
unsigned long ultimaLectura = 0;


// Control de envio

bool primeraLectura = true;

int ultimaCombinacion1 = -1;
int ultimaCombinacion2 = -1;
int ultimaCombinacion3 = -1;


// ==========================================
// SETUP
// ==========================================

void setup() {

    // Iniciar comunicacion serial

    Serial.begin(VELOCIDAD);

    // Leer los valores iniciales

    referencia1 = analogRead(POT1);
    referencia2 = analogRead(POT2);
    referencia3 = analogRead(POT3);

    // Registrar el momento inicial

    ultimoMovimiento = millis();

    ultimaLectura = millis();

}


// ==========================================
// LOOP PRINCIPAL
// ==========================================

void loop() {

    // Controlar el intervalo de lectura

    if (millis() - ultimaLectura < INTERVALO_LECTURA) {
        return;
    }

    ultimaLectura = millis();


    // ======================================
    // LEER POTENCIOMETROS
    // ======================================

    valor1 = analogRead(POT1);
    valor2 = analogRead(POT2);
    valor3 = analogRead(POT3);


    // ======================================
    // DETECTAR MOVIMIENTO
    // ======================================

    bool huboMovimiento = false;


    if (abs(valor1 - referencia1) > TOLERANCIA) {

        referencia1 = valor1;
        huboMovimiento = true;

    }


    if (abs(valor2 - referencia2) > TOLERANCIA) {

        referencia2 = valor2;
        huboMovimiento = true;

    }


    if (abs(valor3 - referencia3) > TOLERANCIA) {

        referencia3 = valor3;
        huboMovimiento = true;

    }


    // Si se detecto movimiento,
    // reiniciar el tiempo de estabilidad

    if (huboMovimiento) {

        ultimoMovimiento = millis();

    }


    // ======================================
    // COMPROBAR ESTABILIDAD
    // ======================================

    if (millis() - ultimoMovimiento >= TIEMPO_ESTABLE) {


        // Convertir valores analogicos
        // en numeros digitales del 0 al 9

        int numero1 = map(referencia1, 0, 1023, 0, 9);

        int numero2 = map(referencia2, 0, 1023, 0, 9);

        int numero3 = map(referencia3, 0, 1023, 0, 9);


        // ==================================
        // ENVIAR DATOS A PYTHON
        // ==================================

        // Enviar solamente si la combinacion
        // cambio respecto del ultimo envio

        if (
            numero1 != ultimaCombinacion1 ||
            numero2 != ultimaCombinacion2 ||
            numero3 != ultimaCombinacion3
        ) {

            Serial.print(numero1);
            Serial.print(",");

            Serial.print(numero2);
            Serial.print(",");

            Serial.println(numero3);


            // Guardar la ultima combinacion enviada

            ultimaCombinacion1 = numero1;
            ultimaCombinacion2 = numero2;
            ultimaCombinacion3 = numero3;

        }

    }

}
