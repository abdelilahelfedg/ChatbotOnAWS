import json
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


class MyBot(ActivityHandler):
   
    def _init_(self):
        super(MyBot, self)._init_()
       
    def load_responses(self):
        """Load responses from a JSON file."""
        try:
            
            with open('data.json', "r") as file:
                 
                return json.load(file)
                
            
        except (FileNotFoundError) as e:
            
            print(f"Error loading responses.json: {e}")
            return {
                "default": "I'm sorry, I didn't quite understand. Can you clarify?"
            }

    async def on_message_activity(self, turn_context: TurnContext):

        responses = self.load_responses()
        
        user_message = turn_context.activity.text

        # Basic response logic
        reply = responses.get(user_message, responses.get("default"))
        
        # Send the reply
        await turn_context.send_activity(reply)
        

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
