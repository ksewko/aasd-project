import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message

class BlindsAgent(Agent):
    class RecvTemp(CyclicBehaviour):

        def recv_plan(self):
            if self.temp < self.pref_temp:
                if self.regulate_temp:
                    if self.blinds_state == 'DOWN':
                        self.blinds_state = 'UP'
                        print("Blinds drawn in room {}".format(self.room_id))
            else:
                if self.regulate_temp:
                    if self.blinds_state == 'DOWN':
                        self.blinds_state = 'UP'
                        print("Blinds exposed in room {}".format(self.room_id))

        async def on_start(self):
            print("Starting behaviour [BlindsAgent]. . .")
            self.room_id = '01'
            self.blinds_state = 'UP'
            self.temp = 0 # aktualny pomiar 

            self.pref_temp = 20 # preferowana z repo
            self.regulate_temp = True # aktualny plan z repo

        async def run(self):
            msg = await self.receive(timeout=10) 
            if msg:
                print("Received temperature: {}".format(msg.body))
                self.temp = int(msg.body)

                msg = Message(to="repo@localhost")       
                msg.set_metadata("msg_type", "ASK")         
                msg.set_metadata("room_id", self.room_id)  
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
        template.set_metadata("sensor_id", "01") 
        self.add_behaviour(self.rcv_temp, template)

        # self.rcv_plan = self.RecvPlan()
        # self.add_behaviour(self.rcv_plan)
