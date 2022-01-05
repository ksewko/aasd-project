import time
import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

class Sensors(Agent):
    class SendMeasurements(CyclicBehaviour):
        async def on_start(self):
            print("Starting behaviour [sensors]. . .")
            self.temp = 0

        async def run(self):
            print("Temperature: {}".format(self.temp))
            self.temp = random.randint(18, 22)
            await asyncio.sleep(1)

    async def setup(self):
        print("Agent starting [sensors]. . .")
        sm = self.SendMeasurements()
        self.add_behaviour(sm)

if __name__ == "__main__":
    sensors = Sensors("sensors@localhost", "password")
    future = sensors.start()
    future.result()

    print("Wait until user interrupts with ctrl+C")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    sensors.stop()