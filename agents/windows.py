import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template

class WindowsAgent(Agent):
    class RecvTemp(CyclicBehaviour):

        async def on_start(self):
            print("Starting behaviour [WindowsAgent]. . .")
            self.temp = 0

        async def run(self):
            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
                self.temp = msg.body
            else:
                print("Did not receive any message after 10 seconds")

            # stop agent from behaviour
            await asyncio.sleep(1)

    async def setup(self):
        print("WindowsAgent started")
        b = self.RecvTemp()
        template = Template() 
        template.set_metadata("msg_type", "INF")    # otrzymana wiadomość powinna pasować do templatki
        template.set_metadata("sensor_id", "01") 
        self.add_behaviour(b, template)