# Universal Lucky Miner LV06 Drivers

Este paquete convierte un **Lucky Miner LV06** (o cualquier dispositivo BM1366 con AxeOS) en un coprocesador neuromórfico.

## 🛠️ Requisitos
1. **Hardware**: Lucky Miner LV06.
2. **Firmware**: AxeOS (ESP-Miner). *Se requiere flashear el dispositivo.*
   - Repositorio: [https://github.com/skot/ESP-Miner](https://github.com/skot/ESP-Miner)
3. **Software**: Python 3.7+ (Sin librerías externas).

## 🚀 Instalación y Uso
1. **Configurar Minero**:
   - En la web de AxeOS, apunta el Pool a:
     - **URL**: `stratum+tcp://<TU_IP_LOCAL>:3333`
     - **User**: `chimera`
     - **Pass**: `x`

2. **Ejecutar Driver**:
   ```bash
   python Universal_LV06_Drivers.py
   ```

3. **Verificación**:
   - El script mostrará `🔌 Connected` cuando el minero se conecte.
   - Si detecta que la frecuencia es baja (<300MHz), automáticamente inyectará `400MHz` para despertar al chip.

## 🔌 API de Entropía
El driver expone un puerto local (**4028**) para aplicaciones científicas.
- **Protocolo**: Raw TCP.
- **Formato**: Lee 32 bytes y recibes 32 bytes de entropía criptográfica (SHA-256 de los hashes del minero).
- **Fallback**: Si el minero está ocupado, el driver sirve entropía del sistema (os.urandom) para evitar latencia.

## ⚠️ Notas Técnicas
- **Autodetector**: No es necesario configurar la IP del minero; el driver la detecta cuando este se conecta por Stratum.
- **Seguridad**: El driver tiene permisos de escritura sobre la configuración del minero (Voltaje/Frecuencia). Úsalo con precaución.
