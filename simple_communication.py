import time
from agents.floor_heating import FloorHeatingAgent
from agents.sensors import SensorsAgent
from agents.windows import WindowsAgent
from agents.blinds import BlindsAgent
import json


if __name__ == "__main__":
    with open('config.json') as conf:
        conf = json.load(conf)

    windows = []
    blinds = []
    floor_heating = []

    for room in conf['rooms']:
        windows_agent = WindowsAgent("windows{}@localhost".format(room['id']), "password", room_id=room['id'], regulate_temp=room['regulated'])
        future = windows_agent.start()
        future.result() # wait for receiver agent to be prepared.
        windows.append(windows_agent)
        
        blinds_agent = BlindsAgent("blinds{}@localhost".format(room['id']), "password", room_id=room['id'], regulate_temp=room['regulated'])
        future = blinds_agent.start()
        future.result() # wait for receiver agent to be prepared.
        blinds.append(blinds_agent)

        floor_heating_agent = FloorHeatingAgent("floor_heating{}@localhost".format(room['id']), "password", room_id=room['id'], regulate_temp=room['regulated'])
        future = floor_heating_agent.start()
        future.result() # wait for receiver agent to be prepared.
        floor_heating.append(floor_heating_agent)


    sensors_agent = SensorsAgent(
        "sensors@localhost",
        "password",
        room_temps=[x for x in range(12, 24)],
        out_temps=[x for x in range(0, 12)],
        uv_values=[x for x in range(48, 60)]
    )
    future = sensors_agent.start()

    print("Wait until user interrupts with ctrl+C")

    alive_agents = windows + blinds + floor_heating

    while all(agent.is_alive() for agent in alive_agents):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sensors_agent.stop()
            for agent in alive_agents:
                agent.stop()
            break
