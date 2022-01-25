import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
import json

class FloorHeatingAgent(Agent):

    def __init__(self, *args, room_id, regulate_temp, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = room_id 
        self.regulate_temp = regulate_temp
        with open('config.json') as conf:
            conf = json.load(conf)
            self.pref_temp = conf['preferred_temp']


    class RecvTemp(CyclicBehaviour):
        def recv_plan(self):
            if self.agent.regulate_temp:
                self.is_heating_on = self.temp < self.agent.pref_temp
                print("Heating in room {} is set to {}".format(self.agent.room_id, self.is_heating_on))
        
        async def on_start(self) -> None:
            print("Starting behavior [FloorHeatingAgent{}]. . .".format(self.agent.room_id))
            # self.room_id = '01'
            self.is_heating_on = False
            self.temp = 0
            # self.pref_temp = 20
            # self.regulate_temp = True

        async def run(self) -> None:
            msg = await self.receive(timeout=10)
            if msg:
                print("Received temperature [floor_heating{}]: {}".format(self.agent.room_id, msg.body))
                self.temp = int(msg.body)
                
                msg = Message(to="repo@localhost")
                msg.set_metadata("msg_type", "ASK")         
                msg.set_metadata("room_id", self.agent.room_id)  
                msg.body = ''                  
                await self.send(msg)

                self.recv_plan() # zamiast odpalania RecvPlan(OneShotBehaviour)
            else:
                print("Did not receive any message after 10 seconds")

            await asyncio.sleep(1)

    class RecvPlan(OneShotBehaviour): # odpala się kiedy dotrze wiadomość z planem
        pass

    async def setup(self):
        self.rcv_temp = self.RecvTemp()
        template = Template() 
        template.set_metadata("msg_type", "INF")    # otrzymana wiadomość powinna pasować do templatki
        template.set_metadata("sensor_id", self.room_id) 
        template.set_metadata("sensor_type", "TERM")
        self.add_behaviour(self.rcv_temp, template)