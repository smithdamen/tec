from tec.server.sim import Simulation
from tec.shared.components import Position


def test_move_consumes_energy_and_moves_one_tile() -> None:
    sim = Simulation()
    eid = sim.spawn_player()
    pos = sim.world.get(Position)[eid]
    start = (pos.x, pos.y)

    # Queue a move up; the sim uses energy accumulation per tick.
    sim.enqueue_move(eid, 0, -1)

    # Tick until the actor has paid the move cost. We don’t assert exact tick count here,
    # just that *eventually* a single move resolves to exactly 1 tile.
    for _ in range(10):
        sim.tick()

    assert (pos.x, pos.y) == (start[0], start[1] - 1)
