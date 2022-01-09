import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class SensorsAgent(Agent):

    class SendTempToWindowsAgent(CyclicBehaviour):
        async def on_start(self):
            self.temp = 0

        async def run(self):

            self.temp = random.randint(18, 22)

            msg = Message(to="windows@localhost")       # jid odbiorcy
            # metadata wiadomości (jak w dokumentacji)
            msg.set_metadata("msg_type", "INF")
            msg.set_metadata("sensor_id", "01")
            msg.set_metadata("sensor_type", "TERM")
            # pomiar (musi być string)
            msg.body = str(self.temp)

            await self.send(msg)

            self.exit_code = "Job Finished!"

            # stop agent from behaviour
            # await self.agent.stop()

            await asyncio.sleep(1)

    class SendTempToBlindsAgent(CyclicBehaviour):
        async def on_start(self):
            self.temp = 0

        async def run(self):
            self.temp = random.randint(18, 22)
            msg = Message(to="blinds@localhost")       # jid odbiorcy
            msg.set_metadata("msg_type", "INF")
            msg.set_metadata("sensor_id", "01")
            msg.set_metadata("sensor_type", "TERM")
            msg.body = str(self.temp)                   # pomiar (musi być string)
            await self.send(msg)
            self.exit_code = "Job Finished!"
            await asyncio.sleep(1)

    class SendUvToBlindsAgent(CyclicBehaviour):
        async def on_start(self):
            self.uv = 0

        async def run(self):
            self.uv = random.randint(0, 100)	#poziom naslonecznienia w % - 0% (pełne zachmurzenie) , 100% (pełne słońce)
            msg = Message(to="blinds@localhost")       # jid odbiorcy
            msg.set_metadata("msg_type", "INF")         # metadata wiadomości (jak w dokumentacji)
            msg.set_metadata("sensor_id", "01")  
            msg.set_metadata("sensor_type", "UV")    
            msg.body = str(self.uv)                   # pomiar (musi być string)

            await self.send(msg)

            self.exit_code = "Job Finished!"

            await asyncio.sleep(1)

    async def setup(self):
        self.b = self.SendTempToWindowsAgent()
        self.c = self.SendTempToBlindsAgent()
        self.d = self.SendUvToBlindsAgent()
        self.add_behaviour(self.b)
        self.add_behaviour(self.c)
        self.add_behaviour(self.d)
