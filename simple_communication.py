import time
import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

class SensorsAgent(Agent):

    class SendTempToWindowsAgent(CyclicBehaviour):
        async def on_start(self):
            print("Starting behaviour [SensorsAgent]. . .")
            self.temp = 0

        async def run(self):
            
            self.temp = random.randint(18, 22)
            print("Temperature: {}".format(self.temp))

            msg = Message(to="windows@localhost")       # jid odbiorcy
            msg.set_metadata("msg_type", "INF")         # metadata wiadomości (jak w dokumentacji)
            msg.set_metadata("sensor_id", "01")  
            msg.set_metadata("sensor_type", "TERM")       
            msg.body = str(self.temp)                   # pomiar (musi być string)

            await self.send(msg)
            print("Message sent!")

            # set exit_code for the behaviour
            self.exit_code = "Job Finished!"

            # stop agent from behaviour
            # await self.agent.stop()

            await asyncio.sleep(1)

    async def setup(self):
        print("Agent starting [SensorsAgent]. . .")
        self.b = self.SendTempToWindowsAgent()
        self.add_behaviour(self.b)


class WindowsAgent(Agent):
    class RecvTemp(CyclicBehaviour):

        async def on_start(self):
            print("Starting behaviour [WindowsAgent]. . .")
            self.temp = 0

        async def run(self):
            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            await asyncio.sleep(1)

    async def setup(self):
        print("WindowsAgent started")
        b = self.RecvTemp()
        template = Template()
        template.set_metadata("msg_type", "INF")
        self.add_behaviour(b, template)


if __name__ == "__main__":
    WindowsAgent = WindowsAgent("windows@localhost", "password")
    future = WindowsAgent.start()
    future.result() # wait for receiver agent to be prepared.

    SensorsAgent = SensorsAgent("sensors@localhost", "password")
    future = SensorsAgent.start()

    print("Wait until user interrupts with ctrl+C")

    while WindowsAgent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            SensorsAgent.stop()
            WindowsAgent.stop()
            break