from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
from threading import Thread
import asyncio
from time import sleep
from random import random, choice
from string import ascii_letters
import logging

TYPE_BASIC = 1
TYPE_EXTRA = 2
INBOUND_QUEUE = 'inbound'
OUTBOUND_QUEUE = 'outbound'
IO_INBOUND_DELAY = 0.15
IO_TASK_DELAY = 0.025
CPU_TASK_DELAY = 0.01
CPU_TH_DELAY = 0.005
MAX_CPU_QUEUE_SIZE = 2
MAX_IO_QUEUE_SIZE = 3

def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)

    return logger

# Create loggers for each worker
cpu_logger = create_logger('[CPU]')
io_logger = create_logger('[IO]')
el_logger = create_logger('[EL]')
mh_logger = create_logger('[MH]')

# simulate a retrieval of inbound message
async def get_inbound_message() -> object:
    message = {
        'type': TYPE_BASIC,
        'char': choice(ascii_letters)
    }

    if random() > 0.5: message['type'] = TYPE_EXTRA

    await asyncio.sleep(IO_INBOUND_DELAY)

    return message

async def io_bound_task(message: object):
    char = message['char']
    io_logger.info(f"=>  {char}")

    await asyncio.sleep(IO_TASK_DELAY)

    io_logger.info(f"=>| {char}")

    # Enrich message with additional meta-data
    message['io_meta_data'] = '+IO+'

    return message

def cpu_bound_task(message):
    char = message['char']
    cpu_logger.info(f"=>  {char}")

    sleep(CPU_TASK_DELAY)

    cpu_logger.info(f"=>| {char}")

    # Enrich message with additional meta-data
    message['cpu_meta_data'] = '+CPU+'

    return message

def cpu_tasks_handler(cpu_queue: multiprocessing.Queue):
    cpu_logger.info("TH")
    # sleep(1) # delay until event loop
    with ProcessPoolExecutor() as executor:
        cpu_logger.info('PPE')
        while True:
            # cpu_logger.info('... ?')
            if cpu_queue.empty():
                # cpu_logger.info("Z-z-z (empty cpu_queue)")
                sleep(CPU_TH_DELAY)
                continue

            cpu_logger.info(f" get message")
            message = cpu_queue.get()
            if message is None:
                Exception('ugh')

            cpu_logger.info(f"/get message")
            cpu_logger.info(f"qsize: {cpu_queue.qsize()}")

            cpu_logger.info(f"==> calc: {message}")

            future = executor.submit(cpu_bound_task, message)
            result = future.result()

            cpu_logger.info(f"==> /calc: {result}")

            # Push a result to 'outbound' queue
            cpu_logger.info(" push result")
            push_result(result)
            cpu_logger.info("/push result")

async def io_tasks_handler(io_queue: asyncio.Queue, cpu_queue: multiprocessing.Queue):
    io_logger.info("TH")
    with ThreadPoolExecutor() as executor:
        io_logger.info('TPE')
        while True:
            io_logger.info(" get message")
            message = await io_queue.get()
            io_logger.info(f"qsize: {io_queue.qsize()}")
            io_logger.info(f"/get message: {message}")

            io_logger.info(f"==> process message: {message}")
            future = executor.submit(io_bound_task, message)
            result = await future.result()
            io_logger.info("got result")

            cpu_queue.put(result)
            io_logger.info("push result")
            io_logger.info(f"CPU qsize: {cpu_queue.qsize()}")

            io_queue.task_done()
            io_logger.info("task done")

# push a result somewhere
def push_result(result):
    pass

def enqueue_to_cpu(cpu_queue, message):
    mh_logger.info(' await enqueuing to CPU')

    cpu_queue.put(message)
    qsize = cpu_queue.qsize()

    mh_logger.info('/await enqueuing to CPU')
    mh_logger.info(f"CPU qsize: {qsize}")

async def enqueue_to_io(io_queue, message):
    mh_logger.info(' await enqueuing to IO')

    await io_queue.put(message)
    qsize = io_queue.qsize()

    mh_logger.info('/await enqueuing to IO')
    mh_logger.info(f"IO qsize: {qsize}")

async def message_handler(message: object, cpu_queue: multiprocessing.Queue, io_queue: asyncio.Queue):
    mh_logger.info(f"  MH got {message}")

    message_type = message['type']

    if message_type == TYPE_BASIC:
        enqueue_to_cpu(cpu_queue, message)
    elif message_type == TYPE_EXTRA:
        await enqueue_to_io(io_queue, message)

async def event_loop(cpu_queue: multiprocessing.Queue, io_queue: asyncio.Queue):
    while True:
        message = await get_inbound_message()
        el_logger.info(' get_inbound_message')

        el_logger.info('await MH')
        await message_handler(message, cpu_queue, io_queue)
        el_logger.info('/await MH')

async def main():
    cpu_queue = multiprocessing.Queue(maxsize=MAX_CPU_QUEUE_SIZE)
    io_queue = asyncio.Queue(maxsize=MAX_IO_QUEUE_SIZE)

    # Start the CPU-task handler
    cpu_tasks_handler_thread = Thread(target=cpu_tasks_handler, args=(cpu_queue,))
    cpu_tasks_handler_thread.start()

    await asyncio.gather(
        asyncio.create_task(io_tasks_handler(io_queue, cpu_queue)),
        asyncio.create_task(event_loop(cpu_queue, io_queue)),
    )

if __name__ == '__main__':
    asyncio.run(main())
