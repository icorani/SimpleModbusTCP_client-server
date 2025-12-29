#!/usr/bin/env python3
"""Тестовый клиент для Signetic."""
import asyncio
from pymodbus.client import AsyncModbusTcpClient


async def read_float(client: AsyncModbusTcpClient, address: int, device_id: int = 7) -> float | None:
    """
    Читает float32 значение (2 регистра) с указанного адреса.

    :param client: AsyncModbusTcpClient
    :param address: Адрес первого регистра (в терминах Modbus сервера)
    :param device_id: Slave ID
    :return: float значение или None при ошибке
    """
    # Читаем 2 регистра для float32
    regs = await client.read_input_registers(
        address=address - 1,  # конвертируем адрес сервера -> клиент
        count=2,
        device_id=device_id
    )

    if regs.isError():
        print(f"Ошибка чтения адрес {address}: {regs}")
        return None

    if len(regs.registers) != 2:
        print(f"Ожидалось 2 регистра, получили {len(regs.registers)}")
        return None

    # Конвертируем регистры во float
    try:
        return client.convert_from_registers(
            registers=regs.registers,
            data_type=client.DATATYPE.FLOAT32,
            word_order="big"
        )
    except Exception as e:
        print(f"Ошибка конвертации: {e}")
        return None


async def read_bits(client: AsyncModbusTcpClient, start_address: int, count: int, device_id: int = 7) -> list[
                                                                                                             bool] | None:
    """
    Читает биты (discrete inputs) с указанного адреса.

    :param client: AsyncModbusTcpClient
    :param start_address: Адрес первого бита (в терминах Modbus сервера)
    :param count: Количество бит
    :param device_id: Slave ID
    :return: Список значений bool или None при ошибке
    """
    bits = await client.read_discrete_inputs(
        address=start_address - 1,  # конвертируем адрес
        count=count,
        device_id=device_id
    )

    if bits.isError():
        print(f"Ошибка чтения битов {start_address}: {bits}")
        return None

    return bits.bits


async def test_connection(host: str = '127.0.0.1', port: int = 5020, device_id: int = 7):
    """
    Тестирует подключение и чтение данных.

    :param host: Хост Modbus сервера
    :param port: Порт Modbus сервера
    :param device_id: Slave ID
    """
    print(f"Тест подключения к {host}:{port} (slave={device_id})...")

    try:
        async with AsyncModbusTcpClient(host, port=port) as client:
            await client.connect()

            if not client.connected:
                print("Не удалось подключиться")
                return

            print("✓ Подключено")

            # Тест float значений
            test_addresses = [1, 3]  # адреса из сервера
            for addr in test_addresses:
                value = await read_float(client, addr, device_id)
                if value is not None:
                    print(f"  Адрес {addr}-{addr + 1} (float32): {value}")

            # Тест битов
            bits = await read_bits(client, start_address=275, count=5, device_id=device_id)
            if bits:
                print(f"  Биты 275-279: {bits}")

    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Точка входа для теста."""
    asyncio.run(test_connection())


if __name__ == "__main__":
    main()