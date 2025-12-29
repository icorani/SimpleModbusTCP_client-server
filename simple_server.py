#!/usr/bin/env python3
"""Минимальный Modbus TCP сервер."""
import asyncio
import signal
import logging
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusServerContext, ModbusDeviceContext, ModbusSequentialDataBlock
from pymodbus import pymodbus_apply_logging_config

pymodbus_apply_logging_config(logging.DEBUG)
regs = [16490, 57672] # this is 3.71 in two byte struct

def create_store():
    """Создаём хранилище."""

    ir_block = ModbusSequentialDataBlock(1, regs)  # тестовые значения
    slave_context = ModbusDeviceContext(ir=ir_block)
    context = ModbusServerContext(devices={7: slave_context}, single=False)
    return context


async def run_server():
    print("Старт эмулятора Signetic (slave_id=7)...")
    context = create_store()

    # StartAsyncTcpServer запускает сервер и не возвращает объект
    server_task = asyncio.create_task(
        StartAsyncTcpServer(
            context=context,
            address=("", 5020),
        )
    )

    print("Сервер запущен: 0.0.0.0:5020, slave_id=7")
    for idx, value in enumerate(regs):
        print(f"Регистр ({idx}): {value}")
    print("Нажми Ctrl+C для остановки")

    stop_event = asyncio.Event()

    def signal_handler():
        print("\nПолучен сигнал остановки")
        stop_event.set()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, signal_handler)

    await stop_event.wait()
    # Отменяем задачу сервера
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

    print("Сервер остановлен")


if __name__ == "__main__":
    asyncio.run(run_server())