from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# WhatsApp API Configuration
WHATSAPP_API_URL = "https://graph.facebook.com/v25.0/1202684002920267/messages"
ACCESS_TOKEN = "EAAN1ZCmbhNOYBRb1agjXMP7H4ejZAS77NFjnbjMUEuBLUzIlcBPny4HLyxvKtJIGSOh5CvZCmXIUzqZAfKN2DpyA1lPRUngjZCvF9L3qxnThZACZAdcGRZCVOOGJZAoyXuReKQZCZBceEHtlwK1ojpfabrUjLaKJthMu0codO5pCpam0mlYKHUXKCjiUyeFsxfv0V4LJ7iZBtU7sjIScaBNJ50XVy7tB1WcqWFlmTXLtrGIfQbZBpRy4QmE4lnIPxWLytXdc2m2yq116U8kZC7Nu3MaFopghkGBOR3iNnuhLDqPwZDZD"
YOUR_NUMBER = "919527911804"  # Your verified number (no + sign)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = "mytoken123"
        if request.args.get("hub.verify_token") == verify_token:
            return request.args.get("hub.challenge")
        return "Verification failed"

    if request.method == 'POST':
        data = request.json

        print("="*50)
        print("INCOMING WEBHOOK DATA:")
        print(json.dumps(data, indent=2))
        print("="*50)

        try:
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']

            if 'messages' in value:
                message_data = value['messages'][0]
                from_number = message_data['from']
                message_type = message_data.get('type', '')

                # Handle text messages only
                if message_type == 'text':
                    message_text = message_data['text']['body'].strip().lower()
                    print(f"✅ USER ({from_number}) SAID: {message_text}")

                    # Generate reply based on message
                    reply_text = get_safety_reply(message_text)

                    # In test mode, always send to YOUR verified number
                    send_whatsapp_message(YOUR_NUMBER, reply_text)
                else:
                    print(f"⚠️ Non-text message received: {message_type}")

        except Exception as e:
            print("❌ ERROR:", e)

        return "ok"


def get_safety_reply(message_text):
    """Generate safety toolbox talk reply based on user input"""

    # Main menu
    if message_text in ['hi', 'hello', 'start', 'menu', 'help']:
        return (
            "👷 *Welcome to Safety Toolbox Talk Bot!* 🛡️\n\n"
            "Please select your work type:\n\n"
            "1️⃣ Excavation\n"
            "2️⃣ Welding\n"
            "3️⃣ Working at Height\n"
            "4️⃣ Electrical Work\n"
            "5️⃣ Confined Space\n"
            "🆘 Type *emergency* for Emergency Help\n\n"
            "Reply with a number (1-5) or keyword."
        )

    # Excavation
    elif message_text in ['1', 'excavation']:
        return (
            "⛏️ *EXCAVATION SAFETY*\n\n"
            "⚠️ *Hazards:*\n"
            "• Cave-in / soil collapse\n"
            "• Underground utilities (gas, electric)\n"
            "• Falling objects\n"
            "• Water accumulation\n\n"
            "🦺 *PPE Required:*\n"
            "• Hard hat\n"
            "• Safety boots\n"
            "• High-visibility vest\n"
            "• Gloves\n\n"
            "✅ *Do's:*\n"
            "• Always check for underground utilities before digging\n"
            "• Shore up walls for excavations deeper than 1.2m\n"
            "• Keep spoil away from edges\n\n"
            "❌ *Don'ts:*\n"
            "• Never work alone in deep excavations\n"
            "• Don't ignore cracks in soil walls\n"
            "• Never store heavy material near edge\n\n"
            "Type *menu* to go back."
        )

    # Welding
    elif message_text in ['2', 'welding']:
        return (
            "🔥 *WELDING SAFETY*\n\n"
            "⚠️ *Hazards:*\n"
            "• Fire and explosion\n"
            "• Electric shock\n"
            "• Toxic fumes\n"
            "• UV radiation / eye damage\n\n"
            "🦺 *PPE Required:*\n"
            "• Welding helmet/shield\n"
            "• Fire-resistant gloves\n"
            "• Leather apron\n"
            "• Safety boots\n"
            "• Respirator mask\n\n"
            "✅ *Do's:*\n"
            "• Ensure good ventilation\n"
            "• Keep fire extinguisher nearby\n"
            "• Inspect cables and equipment before use\n\n"
            "❌ *Don'ts:*\n"
            "• Never weld near flammable materials\n"
            "• Don't weld in wet conditions\n"
            "• Never look at arc without proper shield\n\n"
            "Type *menu* to go back."
        )

    # Working at Height
    elif message_text in ['3', 'height', 'working at height']:
        return (
            "🪜 *WORKING AT HEIGHT SAFETY*\n\n"
            "⚠️ *Hazards:*\n"
            "• Falls from ladders/scaffolding\n"
            "• Falling objects hitting workers below\n"
            "• Unstable platforms\n\n"
            "🦺 *PPE Required:*\n"
            "• Full body harness\n"
            "• Hard hat\n"
            "• Safety boots with grip\n"
            "• Lanyard / lifeline\n\n"
            "✅ *Do's:*\n"
            "• Always use 3-point contact on ladders\n"
            "• Secure all tools with lanyards\n"
            "• Inspect harness before each use\n"
            "• Use barricades below work area\n\n"
            "❌ *Don'ts:*\n"
            "• Never work at height without harness\n"
            "• Don't work in strong winds\n"
            "• Never overload scaffolding\n\n"
            "Type *menu* to go back."
        )

    # Electrical
    elif message_text in ['4', 'electrical', 'electric']:
        return (
            "⚡ *ELECTRICAL SAFETY*\n\n"
            "⚠️ *Hazards:*\n"
            "• Electric shock / electrocution\n"
            "• Arc flash burns\n"
            "• Fire from short circuit\n\n"
            "🦺 *PPE Required:*\n"
            "• Insulated gloves\n"
            "• Safety goggles\n"
            "• Arc flash suit (if needed)\n"
            "• Insulated tools\n\n"
            "✅ *Do's:*\n"
            "• Always use LOTO (Lockout/Tagout)\n"
            "• Test before touch - verify power is OFF\n"
            "• Work with a buddy\n\n"
            "❌ *Don'ts:*\n"
            "• Never work on live circuits alone\n"
            "• Don't use damaged cables\n"
            "• Never bypass safety switches\n\n"
            "Type *menu* to go back."
        )

    # Confined Space
    elif message_text in ['5', 'confined', 'confined space']:
        return (
            "🕳️ *CONFINED SPACE SAFETY*\n\n"
            "⚠️ *Hazards:*\n"
            "• Oxygen deficiency / toxic gases\n"
            "• Engulfment\n"
            "• Entrapment\n"
            "• Heat stress\n\n"
            "🦺 *PPE Required:*\n"
            "• Gas detector / monitor\n"
            "• SCBA or airline respirator\n"
            "• Harness with retrieval line\n"
            "• Communication device\n\n"
            "✅ *Do's:*\n"
            "• Always get a Confined Space Entry Permit\n"
            "• Test atmosphere before entry\n"
            "• Always have a standby person outside\n\n"
            "❌ *Don'ts:*\n"
            "• Never enter without permit\n"
            "• Don't enter if gas levels are unsafe\n"
            "• Never work alone in confined space\n\n"
            "Type *menu* to go back."
        )

    # Emergency
    elif message_text in ['emergency', 'sos', 'accident', 'fire']:
        return (
            "🆘 *EMERGENCY RESPONSE* 🆘\n\n"
            "🔥 *FIRE:*\n"
            "1. Raise alarm immediately\n"
            "2. Call: 101 (Fire)\n"
            "3. Evacuate - don't use lifts\n"
            "4. Assemble at muster point\n\n"
            "🤕 *ACCIDENT/INJURY:*\n"
            "1. Don't move injured person\n"
            "2. Call: 108 (Ambulance)\n"
            "3. Apply first aid if trained\n"
            "4. Inform supervisor immediately\n\n"
            "☠️ *GAS LEAK:*\n"
            "1. Don't operate any switches\n"
            "2. Evacuate immediately\n"
            "3. Call: 101\n\n"
            "📞 *Emergency Numbers:*\n"
            "• Ambulance: 108\n"
            "• Fire: 101\n"
            "• Police: 100\n"
            "• Disaster: 1078\n\n"
            "Stay safe! Type *menu* to return."
        )

    # Default / unknown input
    else:
        return (
            "❓ I didn't understand that.\n\n"
            "Type *menu* or *hi* to see the main menu.\n"
            "Type *emergency* for emergency help. 🆘"
        )


def send_whatsapp_message(to_number, message_text):
    """Send a WhatsApp message using the Graph API"""

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"✅ Message sent successfully to {to_number}")
        else:
            print(f"❌ Failed to send message: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error sending message: {e}")


if __name__ == '__main__':
    app.run(port=5000, debug=True)