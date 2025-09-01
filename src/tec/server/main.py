import asyncio
from contextlib import suppress

from tec.server.net import JsonServer
from tec.server.sim import Simulation


async def sim_loop(sim: Simulation) -> None:
    try:
        while True:
            sim.tick()
            await asyncio.sleep(sim.tick_len)
    except asyncio.CancelledError:
        # graceful exit on shutdown
        return


async def main() -> None:
    sim = Simulation()
    server = JsonServer(sim)

    # start the simulation ticking
    tick_task = asyncio.create_task(sim_loop(sim))

    # start the TCP server (serve_forever inside)
    # this call will block until cancelled (Ctrl-C)
    with suppress(asyncio.CancelledError):
        await server.start()

    # on shutdown, stop the tick loop
    tick_task.cancel()
    with suppress(asyncio.CancelledError):
        await tick_task


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # allow clean Ctrl-C without noisy traceback
        pass
