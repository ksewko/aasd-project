import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message

class WindowsAgent(Agent):
    class RecvTemp(CyclicBehaviour):

        def recv_plan(self):
            if not self.regulate_temp:
                return
            if self.temp != self.pref_temp:
                if (self.pref_temp - self.temp) * (self.pref_temp - self.out_temp) >= 0:
                    if self.window_state == 'OPEN':
                        self.window_state = 'CLOSED'
                        print("Closed windows in room {}".format(self.room_id))
                else:
                    if self.window_state == 'CLOSED':
                        self.window_state = 'OPEN'
                        print("Opened windows in room {}".format(self.room_id))

        async def on_start(self):
            print("Starting behaviour [WindowsAgent]. . .")
            self.room_id = '01'
            self.window_state = 'CLOSED'
            self.temp = 0 # aktualny pomiar 
            self.out_temp = 0 # aktualny pomiar 

            self.pref_temp = 20 # preferowana z repo
            self.regulate_temp = True # aktualny plan z repo

        async def run(self):
            msg = await self.receive(timeout=10) 
            if msg:
                if msg.metadata["sensor_type"] == "TERM":
                    print("Received temperature [windows]: {}".format(msg.body))
                    self.temp = int(msg.body)
                elif msg.metadata["sensor_type"] == "OUT_TERM":
                    print("Received outdoor temp [windows]: {}".format(msg.body))
                    self.out_temp = int(msg.body)
                else:
                    print("Unknown sensor type {}".format(msg.metadata["sensor_type"]))

                msg = Message(to="repo@localhost")       
                msg.set_metadata("msg_type", "ASK")         
                msg.set_metadata("room_id", self.room_id)  
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
        template.set_metadata("sensor_id", "01")
        self.add_behaviour(self.rcv_temp, template)

        # self.rcv_plan = self.RecvPlan()
        # self.add_behaviour(self.rcv_plan)
