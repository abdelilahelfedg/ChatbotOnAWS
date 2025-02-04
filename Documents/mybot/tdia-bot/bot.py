# from botbuilder.core import ActivityHandler, TurnContext
# from botbuilder.schema import ChannelAccount
# import json


# class MyBot(ActivityHandler):
    
#     def __init__(self):
#         # super().__init__()
#         super(MyBot, self).__init__()

#     def load_responses(self):
#         """Load responses from a JSON file."""
#         try:
            
#             with open('data.json', "r", encoding="utf-8") as file:
                 
#                 return json.load(file)
                
            
#         except (FileNotFoundError) as e:
            
#             print(f"Error loading responses.json: {e}")
#             return {
#                 "default": "I'm sorry, I didn't quite understand. Can you clarify?"
#             }
        
#     async def get_response(self, user_message: str):
#         """Generate a response for the given user message."""
#         responses = self.load_responses()
#         reply = responses.get(user_message, responses.get("default"))
#         return reply

#     async def on_message_activity(self, turn_context: TurnContext):

#         responses = self.load_responses()
        
#         user_message = turn_context.activity.text

#         # Basic response logic
#         reply = responses.get(user_message, responses.get("default"))
        
#         # Send the reply
#         await turn_context.send_activity(reply)

#     async def on_members_added_activity(
#         self,
#         members_added: ChannelAccount,
#         turn_context: TurnContext
#     ):
#         for member_added in members_added:
#             if member_added.id != turn_context.activity.recipient.id:
#                 await turn_context.send_activity("Hello and welcome!")

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import json
import aiohttp
from config import DefaultConfig  # Import des configurations CLU


class MyBot(ActivityHandler):
    def __init__(self, config):
        super(MyBot, self).__init__()
        # self.config = DefaultConfig()
        self.endpoint = config.CLU_ENDPOINT
        self.key = config.CLU_KEY
        self.project_name = config.CLU_PROJECT_NAME
        self.deployment_name = config.CLU_DEPLOYMENT_NAME
        self.api_version = config.CLU_API_VERSION

    def load_responses(self):
        """Load responses from a JSON file."""
        try:
            with open('data.json', "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError as e:
            print(f"Error loading responses.json: {e}")
            return {
                "default": "I'm sorry, I didn't quite understand. Can you clarify?"
            }

    async def call_clu(self, user_message: str):
        """Call the CLU endpoint with the user message."""
        print("dddd")
        url = f"{self.endpoint}/language/:analyze-conversations?api-version={self.api_version}"
        print(self.endpoint)
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json"
        }
        payload = {
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "id": "1",
                    "text": user_message,
                    "modality": "text",
                    "language": "en",
                    "participantId": "user"
                }
            },
            "parameters": {
                "projectName": self.project_name,
                "deploymentName": self.deployment_name,
                "stringIndexType": "Utf16CodeUnit"
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    error_details = await response.text()
                    print(error_details)
                    print(f"CLU request failed with status {response.status}")
                    return None

    async def process_clu_response(self, clu_result):
        """Process the response from CLU and extract the relevant information."""
        # print(clu_result)
        if not clu_result:
            return "I'm sorry, something went wrong while processing your request."

        # Extract the top intent from CLU response
        top_intent = clu_result.get("result", {}).get("prediction", {}).get("topIntent", "")
        intents = clu_result.get("result", {}).get("prediction", {}).get("intents", {})
        entities = clu_result.get("result", {}).get("prediction", {}).get("entities", [])
        # print("Intents :", intents)
        # print("\n entities :", entities)
        print("\n top intent :", top_intent)

        # Handle intents and entities (customize this logic as needed)
        if top_intent and any(intent.get("category") == top_intent for intent in intents):
            return top_intent
        else:
            return "I'm not sure how to help with that."

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text

        # Step 1: Call CLU for intent and entity extraction
        clu_result = await self.call_clu(user_message)

        # Step 2: Process CLU result to generate a response
        clu_response = await self.process_clu_response(clu_result)

        responses = self.load_responses()
        print("clu :", clu_response)
        reply = responses.get(clu_response, responses.get("default"))
        print("reply :", reply)

        # Step 3: Send the response to the user
        await turn_context.send_activity(reply)

    async def on_members_added_activity(self, members_added: ChannelAccount, turn_context: TurnContext):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
