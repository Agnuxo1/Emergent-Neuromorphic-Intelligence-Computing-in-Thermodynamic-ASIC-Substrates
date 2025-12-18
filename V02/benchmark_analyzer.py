"""
CHIMERA BENCHMARK ANALYZER
Analiza los resultados del benchmark de comunicacion PC-Minero
"""

import re
from datetime import datetime

def analyze_benchmark_log(log_file):
    """
    Analiza el log de benchmark y genera estadisticas
    """
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraer shares totales
    shares = re.findall(r'\[SHARE\] #(\d+)', content)
    total_shares = len(shares)

    # Extraer reportes de telemetria
    telemetry_reports = re.findall(
        r'Tiempo transcurrido: ([\d.]+)s.*?'
        r'Shares/segundo \(ventana 1000\): ([\d.]+).*?'
        r'Shares/segundo \(promedio\): ([\d.]+).*?'
        r'Total shares recibidos: (\d+).*?'
        r'Hashrate estimado: ([\d.]+) MH/s',
        content,
        re.DOTALL
    )

    if not telemetry_reports:
        print("[ERROR] No se encontraron reportes de telemetria en el log")
        return

    print("\n" + "="*80)
    print("ANALISIS DE BENCHMARK CHIMERA - COMUNICACION PC-MINERO")
    print("="*80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

    print(f"Total de shares capturados: {total_shares}")
    print(f"Reportes de telemetria generados: {len(telemetry_reports)}\n")

    if telemetry_reports:
        last_report = telemetry_reports[-1]
        elapsed, window_rate, avg_rate, total, hashrate = last_report

        print("METRICAS FINALES:")
        print("-" * 80)
        print(f"Duracion total de la prueba: {float(elapsed):.2f} segundos")
        print(f"Shares/segundo (ventana): {float(window_rate):.2f}")
        print(f"Shares/segundo (promedio): {float(avg_rate):.2f}")
        print(f"Hashrate estimado: {float(hashrate):.2f} MH/s")
        print("-" * 80 + "\n")

        # Comparacion con configuracion anterior
        print("COMPARACION CON CONFIGURACION ANTERIOR:")
        print("-" * 80)
        print("Configuracion anterior (diff=1024): ~1 share/minuto (0.017 sh/s)")
        print(f"Configuracion actual (diff=1): {float(avg_rate):.2f} sh/s")

        improvement_factor = float(avg_rate) / 0.017
        print(f"\nMEJORA: {improvement_factor:.1f}x mas shares por segundo")
        print(f"Esto representa {improvement_factor:.0f}x mas flujo de entropia")
        print("-" * 80 + "\n")

        # Proyeccion de datos
        shares_per_minute = float(avg_rate) * 60
        shares_per_hour = shares_per_minute * 60

        print("PROYECCION DE FLUJO DE DATOS:")
        print("-" * 80)
        print(f"Shares por minuto: {shares_per_minute:.0f}")
        print(f"Shares por hora: {shares_per_hour:.0f}")
        print(f"Datos disponibles para HNS: CONTINUO")
        print("-" * 80 + "\n")

        # Diagnostico
        print("DIAGNOSTICO:")
        print("-" * 80)
        if float(avg_rate) > 1.0:
            print("[OK] El flujo de entropia es OPTIMO para CHIMERA")
            print("[OK] El ASIC esta reportando 'pensamientos debiles' correctamente")
            print("[OK] El cuello de botella de Stratum ha sido ELIMINADO")
        elif float(avg_rate) > 0.1:
            print("[WARNING] Flujo de entropia ACEPTABLE pero puede mejorarse")
            print("[SUGERENCIA] Considerar bajar dificultad a 0.5 o menos")
        else:
            print("[ERROR] Flujo de entropia INSUFICIENTE")
            print("[ACCION] Verificar conexion minero-PC y configuracion")
        print("-" * 80 + "\n")

    # Historial de progresion
    print("PROGRESION TEMPORAL:")
    print("-" * 80)
    for i, report in enumerate(telemetry_reports[-5:], 1):  # Ultimos 5 reportes
        elapsed, window_rate, avg_rate, total, hashrate = report
        print(f"Reporte {i}: {float(elapsed):.1f}s | "
              f"{float(window_rate):.2f} sh/s | "
              f"{total} shares acumulados")
    print("-" * 80 + "\n")

    print("="*80)
    print("FIN DEL ANALISIS")
    print("="*80)

if __name__ == "__main__":
    print("\n[BENCHMARK ANALYZER] Esperando archivo de log...")
    print("Instrucciones:")
    print("1. Ejecuta chimera_wifi_bridge.py")
    print("2. Deja que el minero trabaje durante 30-60 segundos")
    print("3. Copia la salida del terminal y guardala en 'benchmark_log.txt'")
    print("4. Ejecuta este script de nuevo: python benchmark_analyzer.py")
    print("\nAlternativamente, pasa el archivo de log como argumento:")
    print("python benchmark_analyzer.py benchmark_log.txt\n")

    import sys
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
        analyze_benchmark_log(log_file)
    else:
        # Intentar leer de archivo por defecto
        try:
            analyze_benchmark_log('benchmark_log.txt')
        except FileNotFoundError:
            print("[INFO] No se encontro 'benchmark_log.txt'")
            print("El servidor esta ejecutandose. Espera a ver datos de telemetria.")
