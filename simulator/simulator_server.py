#!/usr/bin/env python3
import asyncio
import logging

from pymodbus.server.simulator.http_server import ModbusSimulatorServer
from pymodbus import pymodbus_apply_logging_config

# Настраиваем логирование pymodbus
pymodbus_apply_logging_config(logging.DEBUG)


async def main():
    server = ModbusSimulatorServer(
        modbus_server='signetic_server',
        modbus_device='signetic_device',
        http_host='127.0.0.1',
        http_port=8080,
        json_file='./setup.json'
    )

    print("Симулятор Signetic запущен")
    print("Modbus TCP: 127.0.0.1:5020")
    print("HTTP UI: http://localhost:8080")

    # Запускаем сервер
    await server.run_forever(only_start=False)


if __name__ == "__main__":
    asyncio.run(main())