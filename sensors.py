import time
import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message

class Sensors(Agent):

    class SendTempToWindows(CyclicBehaviour):
        async def on_start(self):
            print("Starting behaviour [sensors]. . .")
            self.temp = 0

        async def run(self):
            
            self.temp = random.randint(18, 22)
            print("Temperature: {}".format(self.temp))

            msg = Message(to="windows@localhost")       # jid odbiorcy
            msg.set_metadata("msg_type", "INF")         # metadata wiadomości (jak w dokumentacji)
            msg.set_metadata("sensor_id", "01")  
            msg.set_metadata("sensor_type", "TERM")       
            msg.body = {"value": self.temp}             # pomiar 

            await self.send(msg)
            print("Message sent!")

            # set exit_code for the behaviour
            self.exit_code = "Job Finished!"

            # stop agent from behaviour
            # await self.agent.stop()

            await asyncio.sleep(1)

    async def setup(self):
        print("Agent starting [sensors]. . .")
        self.b = self.SendTempToWindows()
        self.add_behaviour(self.b)

if __name__ == "__main__":
    sensors = Sensors("sensors@localhost", "password")
    future = sensors.start()
    future.result()

    print("Wait until user interrupts with ctrl+C")

    while sensors.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sensors.stop()
            break
    print("Agent finished with exit code: {}".format(sensors.b.exit_code))