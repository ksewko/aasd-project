import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
import json

class WindowsAgent(Agent):

    def __init__(self, *args, room_id, regulate_temp, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = room_id 
        self.regulate_temp = regulate_temp
        with open('config.json') as conf:
            conf = json.load(conf)
            self.pref_temp = conf['preferred_temp']
        

    class RecvTemp(CyclicBehaviour):

        def recv_plan(self):
            if not self.agent.regulate_temp:
                return
            if self.temp != self.agent.pref_temp:
                if (self.agent.pref_temp - self.temp) * (self.agent.pref_temp - self.out_temp) >= 0:
                    if self.window_state == 'OPEN':
                        self.window_state = 'CLOSED'
                        print("Closed windows in room {}".format(self.agent.room_id))
                else:
                    if self.window_state == 'CLOSED':
                        self.window_state = 'OPEN'
                        print("Opened windows in room {}".format(self.agent.room_id))

        async def on_start(self):
            print("Starting behaviour [WindowsAgent {}]. . .".format(self.agent.room_id))
            self.window_state = 'OPEN'
            self.temp = 0 # aktualny pomiar 
            self.out_temp = 0 # aktualny pomiar 


        async def run(self):
            msg = await self.receive(timeout=10) 
            if msg:
                if msg.metadata["sensor_type"] == "TERM":
                    self.temp = int(msg.body)
                elif msg.metadata["sensor_type"] == "OUT_TERM":
                    self.out_temp = int(msg.body)
                else:
                    print("Unknown sensor type {}".format(msg.metadata["sensor_type"]))
                print("Windows agent for room {}: inside temp {}, outside temp {}".format(self.agent.room_id, self.temp, self.out_temp))

                msg = Message(to="repo@localhost")       
                msg.set_metadata("msg_type", "ASK")         
                msg.set_metadata("room_id", self.agent.room_id)  
                msg.body = ''                  
                await self.send(msg)

                self.recv_plan() # zamiast odpalania RecvPlan(OneShotBehaviour)

            else:
                print("Did not receive any message after 10 seconds")

            await asyncio.sleep(0.5)

    class RecvPlan(OneShotBehaviour): # odpala się kiedy dotrze wiadomość z planem
        pass

    async def setup(self):
        self.rcv_temp = self.RecvTemp()
        template = Template() 
        template.set_metadata("msg_type", "INF")    # otrzymana wiadomość powinna pasować do templatki
        template.set_metadata("sensor_id", self.room_id)
        self.add_behaviour(self.rcv_temp, template)

        # self.rcv_plan = self.RecvPlan()
        # self.add_behaviour(self.rcv_plan)
