import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
from twilio.rest import Client
import urllib

class TwilioClient:
    def __init__(self):
        load_dotenv()
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"]
        )

    def end_call(self, sid):
        try:
            call = self.client.calls(sid).update(
                twiml="<Response><Hangup></Hangup></Response>",
            )
            print(f"Ended call: ", vars(call))
        except Exception as err:
            print(err)

    def register_phone_agent(self, phone_number, agent_id):
        try:
            phone_number_objects = self.client.incoming_phone_numbers.list(limit=200)
            number_sid = None
            for phone_number_object in phone_number_objects:
                if phone_number_object.phone_number == phone_number:
                    number_sid = phone_number_object.sid
            if number_sid is None:
                print("Unable to locate this number in your Twilio account.")
                return
            self.client.incoming_phone_numbers(number_sid).update(
                voice_url=f"{os.environ['NGROK_IP_ADDRESS']}/twilio-voice-webhook/{agent_id}"
            )
        except Exception as err:
            print(err)

    def create_phone_call(self, from_number, to_number, agent_id, custom_variables):
        if not isinstance(custom_variables, dict):
            custom_variables = {}

        query_string = urllib.parse.urlencode(custom_variables)
        try:
            call = self.client.calls.create(
                machine_detection="Enable",
                url=f"{os.environ['NGROK_IP_ADDRESS']}/twilio-voice-webhook/{agent_id}?{query_string}",
                to=to_number,
                from_=from_number,
                status_callback=f"{os.environ['STATUS_URL']}",
                status_callback_event=["completed"]
            )
            print(f"Call from: {from_number} to: {to_number}")
            return call
        except Exception as err:
            print(err)

    def get_call_status(self, call_id):
        return self.client.calls(call_id).fetch()

    def update_call(self, call_id, item):
        updated_call = self.client.calls(call_id).update(twiml=item)
        return updated_call

    def fetch(self, call_sid):
        return self.client.calls(call_sid).fetch()
