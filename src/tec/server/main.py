import asyncio

from tec.server.net import JsonServer
from tec.server.sim import Simulation


async def main() -> None:
    sim = Simulation()
    server = JsonServer(sim)
    loop = asyncio.get_event_loop()
    loop.create_task(sim_loop(sim))
    await server.start()


async def sim_loop(sim: Simulation) -> None:
    sim.run_forever()


if __name__ == "__main__":
    asyncio.run(main())
