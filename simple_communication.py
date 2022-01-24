import time
from agents.floor_heating import FloorHeatingAgent
from agents.sensors import SensorsAgent
from agents.windows import WindowsAgent
from agents.blinds import BlindsAgent


if __name__ == "__main__":
    windows_agent = WindowsAgent("windows@localhost", "password")
    future = windows_agent.start()
    future.result() # wait for receiver agent to be prepared.
    
    blinds_agent = BlindsAgent("blinds@localhost", "password")
    future = blinds_agent.start()
    future.result() # wait for receiver agent to be prepared.

    floor_heating_agent = FloorHeatingAgent("floor_heating@localhost", "password")
    future = floor_heating_agent.start()
    future.result() # wait for receiver agent to be prepared.

    sensors_agent = SensorsAgent(
        "sensors@localhost",
        "password",
        room_temps=[x for x in range(12, 24)],
        out_temps=[x for x in range(0, 12)],
        uv_values=[x for x in range(48, 60)]
    )
    future = sensors_agent.start()

    print("Wait until user interrupts with ctrl+C")

    alive_agents = [windows_agent, blinds_agent, floor_heating_agent]

    while all(agent.is_alive() for agent in alive_agents):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sensors_agent.stop()
            for agent in alive_agents:
                agent.stop()
            break
