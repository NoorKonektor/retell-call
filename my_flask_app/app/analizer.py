from flask import Blueprint, request, jsonify

analizer_bp = Blueprint('analizer', __name__)

def extract_transcript_and_tools(json_data):
    transcript = []
    for item in json_data["transcript_with_tool_calls"]:
        if item["role"] in ["agent", "user"]:
            speaker = item["role"].capitalize()
            content = item["content"]
            transcript.append(f"{speaker}: {content}")
        elif item["role"] == "tool_call_invocation":
            tool_name = item["name"]
            transcript.append(f"[Agent executes tool: {tool_name}]")
    return "\n\n".join(transcript)

@analizer_bp.route("/extract_advanced_transcript", methods=["POST"])
def handle_webhook():
    json_data = request.json
    transcript = extract_transcript_and_tools(json_data)
    return jsonify({"transcript": transcript}), 200
