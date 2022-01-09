import time
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

    sensors_agent = SensorsAgent("sensors@localhost", "password")
    future = sensors_agent.start()

    print("Wait until user interrupts with ctrl+C")

    while windows_agent.is_alive() and blinds_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sensors_agent.stop()
            windows_agent.stop()
            blinds_agent.stop()
            break
