import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json


class SensorsAgent(Agent):

    def __init__(self, *args, room_temps = [], out_temps = [], uv_values = [], **kwargs):
        super().__init__(*args, **kwargs)
        self.temp = room_temps
        self.out_temp = out_temps
        self.uv_values = uv_values
        with open('config.json') as conf:
            conf = json.load(conf)
            self.rooms = conf['rooms']


    class SendTempToWindowsAgent(CyclicBehaviour):
        async def on_start(self):
            self.temp = 0
            self.counter = 0

        async def run(self):

            if self.counter < len(self.agent.temp):
                self.temp = self.agent.temp[self.counter]
            else:
                self.counter -= len(self.agent.temp)
                self.temp = random.randint(18, 22)

            for room in self.agent.rooms:
                msg = Message(to="windows{}@localhost".format(room['id']))       # jid odbiorcy
                # metadata wiadomości (jak w dokumentacji)
                msg.set_metadata("msg_type", "INF")
                msg.set_metadata("sensor_id", room['id'])
                msg.set_metadata("sensor_type", "TERM")
                # pomiar (musi być string)
                msg.body = str(self.temp)

                await self.send(msg)

            self.exit_code = "Job Finished!"

            # stop agent from behaviour
            # await self.agent.stop()
            self.counter += 1
            await asyncio.sleep(1)

    class SendOutdoorTempToWindowsAgent(CyclicBehaviour):
        async def on_start(self):
            self.temp = 0
            self.counter = 0

        async def run(self):

            if self.counter < len(self.agent.out_temp):
                self.temp = self.agent.out_temp[self.counter]
            else:
                self.counter -= len(self.agent.out_temp)
                self.temp = random.randint(18, 22)

            for room in self.agent.rooms:
                msg = Message(to="windows{}@localhost".format(room['id']))       # jid odbiorcy
                # metadata wiadomości (jak w dokumentacji)
                msg.set_metadata("msg_type", "INF")
                msg.set_metadata("sensor_id", room['id'])
                msg.set_metadata("sensor_type", "OUT_TERM")
                # pomiar (musi być string)
                msg.body = str(self.temp)

                await self.send(msg)

            self.exit_code = "Job Finished!"

            # stop agent from behaviour
            # await self.agent.stop()
            self.counter += 1
            await asyncio.sleep(1)

    class SendTempToBlindsAgent(CyclicBehaviour):
        async def on_start(self):
            self.temp = 0
            self.counter = 0

        async def run(self):

            if self.counter < len(self.agent.temp):
                self.temp = self.agent.temp[self.counter]
                # print("---------------- {}".format(self.temp))
                # print("----------------")
            else:
                self.counter -= len(self.agent.temp)
                self.temp = random.randint(18, 22)
            
            for room in self.agent.rooms:
                msg = Message(to="blinds{}@localhost".format(room['id']))       # jid odbiorcy
                msg.set_metadata("msg_type", "INF")
                msg.set_metadata("sensor_id", room['id'])
                msg.set_metadata("sensor_type", "TERM")
                msg.body = str(self.temp)                   # pomiar (musi być string)
                await self.send(msg)
            self.exit_code = "Job Finished!"
            self.counter += 1
            await asyncio.sleep(1)

    class SendUvToBlindsAgent(CyclicBehaviour):
        async def on_start(self):
            self.uv = 0
            self.counter = 0

        async def run(self):

            if self.counter < len(self.agent.uv_values):
                self.uv = self.agent.uv_values[self.counter]
            else:
                self.counter -= len(self.agent.uv_values)
                self.uv = random.randint(0, 100)	#poziom naslonecznienia w % - 0% (pełne zachmurzenie) , 100% (pełne słońce)
            
            for room in self.agent.rooms:
                msg = Message(to="blinds{}@localhost".format(room['id']))       # jid odbiorcy
                msg.set_metadata("msg_type", "INF")         # metadata wiadomości (jak w dokumentacji)
                msg.set_metadata("sensor_id", room['id'])  
                msg.set_metadata("sensor_type", "UV")    
                msg.body = str(self.uv)                   # pomiar (musi być string)

                await self.send(msg)

            self.exit_code = "Job Finished!"
            self.counter += 1
            await asyncio.sleep(1)
    
    class SendTempToHeatingAgent(CyclicBehaviour):
        async def on_start(self):
            self.temp = 0
            self.counter = 0

        async def run(self):

            if self.counter < len(self.agent.temp):
                self.temp = self.agent.temp[self.counter]
                # print(">>>>>>>>>>>>>{}".format(self.temp))
                # print(">>>>>>>>>>>>>")
            else:
                self.counter -= len(self.agent.temp)
                self.temp = random.randint(18, 22)

            for room in self.agent.rooms:
                msg = Message(to="floor_heating{}@localhost".format(room['id']))       # jid odbiorcy
                # metadata wiadomości (jak w dokumentacji)
                msg.set_metadata("msg_type", "INF")
                msg.set_metadata("sensor_id", room['id'])
                msg.set_metadata("sensor_type", "TERM")
                # pomiar (musi być string)
                msg.body = str(self.temp)

                await self.send(msg)

            self.exit_code = "Job Finished!"

            # stop agent from behaviour
            # await self.agent.stop()
            self.counter += 1
            await asyncio.sleep(1)

    async def setup(self):
        self.b = self.SendTempToWindowsAgent()
        self.c = self.SendTempToBlindsAgent()
        self.d = self.SendUvToBlindsAgent()
        self.e = self.SendTempToHeatingAgent()
        self.f = self.SendOutdoorTempToWindowsAgent()
        self.add_behaviour(self.b)
        self.add_behaviour(self.c)
        self.add_behaviour(self.d)
        self.add_behaviour(self.e)
        self.add_behaviour(self.f)
