import time
from agents.floor_heating import FloorHeatingAgent
from agents.sensors import SensorsAgent
from agents.windows import WindowsAgent
from agents.blinds import BlindsAgent
import json
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run a test scenario')
    parser.add_argument('test', type=int, 
                    help='number of the test to run')

    args = parser.parse_args()

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
        future.result() 
        blinds.append(blinds_agent)

        floor_heating_agent = FloorHeatingAgent("floor_heating{}@localhost".format(room['id']), "password", room_id=room['id'], regulate_temp=room['regulated'])
        future = floor_heating_agent.start()
        future.result() 
        floor_heating.append(floor_heating_agent)


    if args.test == 0:
        sensors_agent = SensorsAgent(
            "sensors@localhost",
            "password",
            room_temps=[x for x in range(12, 24)],
            out_temps=[x for x in range(0, 12)],
            uv_values=[x for x in range(48, 60)]
        )
    elif args.test == 1:
        sensors_agent = SensorsAgent(
            "sensors@localhost",
            "password",
            room_temps=[x for x in range(23, 13, -1)],
            out_temps=[x for x in range(25, -15, -2)],
            uv_values=[x for x in range(70, 40, -3)]
        )
    elif args.test == 2:
        sensors_agent = SensorsAgent(
            "sensors@localhost",
            "password",
            room_temps=[10] * 50,
            out_temps=[19, 21] * 50,
            uv_values=[10] * 50
        )
    else: 
        raise ValueError('Test scenario not specified')

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
