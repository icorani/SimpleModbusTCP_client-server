#!/usr/bin/env python3
import asyncio
import struct
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.constants import DataType


async def main():
    async with AsyncModbusTcpClient('127.0.0.1', port=5020) as client:
        await client.connect()

        if not client.connected:
            print("Не подключился")
            return

        addresses = [
            (10, "первый float"),
            (12, "второй float")
        ]

        # Пробуем оба типа регистров
        for func_name, func in [
            ("Input registers", client.read_input_registers),
            ("Holding registers", client.read_holding_registers)
        ]:
            print(f"\n--- {func_name} ---")

            for addr, desc in addresses:
                result = await func(address=addr, count=2, device_id=7)

                if result.isError():
                    print(f"Адрес {addr}: ошибка {result}")
                else:
                    # Конвертируем 2 регистра во float
                    if len(result.registers) == 2:
                        packed = struct.pack('>HH', result.registers[0], result.registers[1])
                        float_val = struct.unpack('>f', packed)[0]
                        print(f"Адрес {addr}-{addr + 1}: {float_val} ({desc})")
                    else:
                        print(f"Адрес {addr}: получено {len(result.registers)} регистров")

async def one_address_read():
    async with AsyncModbusTcpClient('127.0.0.1', port=5020) as client:
        await client.connect()
        print('Connected...') if client.connected else None
        # print(await client.report_device_id(device_id=7)) #device id func
        # print(await client.read_device_information(device_id=7)) #device info func

        #try read first addresses from input register where float32 value placed
        first = await client.read_input_registers(address=0, device_id=7, count=2)
        second = await client.read_input_registers(address=4, device_id=7, count=2)
        middle = await client.read_input_registers(address=2, device_id=7, count=2)
        if not first.isError():
        #output received data
            for index, value in enumerate(first.registers):
                print(f"ADDR={index}: {value}")
            float_from_register = client.convert_from_registers(
                registers=first.registers,
                data_type=client.DATATYPE.FLOAT32,
                word_order="big",
            )
            print(f"Значение FLOAT32: {float_from_register}")
        if not second.isError():
        #output received data
            for index, value in enumerate(second.registers):
                print(f"ADDR={index}: {value}")
            float_from_register = client.convert_from_registers(
                registers=second.registers,
                data_type=client.DATATYPE.FLOAT32,
                word_order="big",
            )
            print(f"Значение FLOAT32: {float_from_register}")
        if not middle.isError():
        #output received data
            for index, value in enumerate(middle.registers):
                print(f"ADDR={index}: {value}")
            float_from_register = client.convert_from_registers(
                registers=middle.registers,
                data_type=client.DATATYPE.FLOAT32,
                word_order="big",
            )
            print(f"Значение FLOAT32: {float_from_register}")
        print(first)
        print(second)
        print(middle)
        print(await client.read_discrete_inputs(address=0, device_id=7, count=5))

if __name__ == "__main__":
    asyncio.run(one_address_read())