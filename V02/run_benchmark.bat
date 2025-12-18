@echo off
echo [BENCHMARK] Iniciando servidor CHIMERA...
echo [INFO] Los datos se guardaran en benchmark_output.txt
echo.
python "d:\Holographic Reservoir Computing\V02\chimera_wifi_bridge.py" 2>&1 | tee benchmark_output.txt
