import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

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

            self.exit_code = "Job Finished!"

            # stop agent from behaviour 
            # await self.agent.stop()

            await asyncio.sleep(1)

    async def setup(self):
        print("Agent starting [SensorsAgent]. . .")
        self.b = self.SendTempToWindowsAgent()
        self.add_behaviour(self.b)