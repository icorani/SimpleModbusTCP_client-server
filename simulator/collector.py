#!/usr/bin/env python3
import asyncio
from pymodbus.client import AsyncModbusTcpClient


async def main():
    print("Тест с convert_from_registers...")

    try:
        async with AsyncModbusTcpClient('127.0.0.1', port=5020) as client:
            await client.connect()

            if client.connected:
                print("Подключено")

                # Читаем 2 регистра (float32)
                regs = await client.read_input_registers(address=0, count=2, device_id=7)

                if not regs.isError():
                    print(f"Сырые регистры: {regs.registers}")

                    # Конвертируем через встроенный метод
                    float_value = client.convert_from_registers(
                        registers=regs.registers,
                        data_type=client.DATATYPE.FLOAT32,
                        word_order="big"
                    )
                    print(f"Float значение: {float_value}")

                    # Для проверки: ручной способ
                    import struct
                    packed = struct.pack('>HH', regs.registers[0], regs.registers[1])
                    manual_val = struct.unpack('>f', packed)[0]
                    print(f"Ручная конвертация: {manual_val}")

            else:
                print("Не подключено")

    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())