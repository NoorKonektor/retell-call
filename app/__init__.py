from flask import Flask
from .twilio_server import TwilioClient
from .webhook import webhook_bp
from .analizer import analizer_bp

app = Flask(__name__)

# Initialize Twilio Client
twilio_client = TwilioClient()

# Register Blueprints
app.register_blueprint(webhook_bp)
app.register_blueprint(analizer_bp)

# Modify the phone number for inbound calls
twilio_client.register_phone_agent(os.getenv("PHONE_NUMBER"), os.getenv("RETELL_AGENT_ID"))
