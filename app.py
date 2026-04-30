import os
from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# WhatsApp API Configuration
WHATSAPP_API_URL = "https://graph.facebook.com/v25.0/1202684002920267/messages"
ACCESS_TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "mytoken123")
YOUR_NUMBER = "919527911804"

@app.route('/')
def home():
    return "Safety Toolbox Talk Bot is running!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed"

    if request.method == 'POST':
        data = request.json
        print("INCOMING:", json.dumps(data, indent=2))

        try:
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']

            if 'messages' in value:
                message_data = value['messages'][0]
                from_number = message_data['from']
                message_type = message_data.get('type', '')

                if message_type == 'text':
                    message_text = message_data['text']['body'].strip().lower()
                    print(f"USER ({from_number}) SAID: {message_text}")

                    reply_text = get_safety_reply(message_text)

                    if from_number == YOUR_NUMBER:
                        reply_to = YOUR_NUMBER
                    else:
                        reply_to = YOUR_NUMBER

                    send_whatsapp_message(reply_to, reply_text)

        except Exception as e:
            print("ERROR:", e)

        return "ok"


def get_safety_reply(message_text):

    if message_text in ['hi', 'hello', 'start', 'menu', 'help']:
        return (
            "👷 *Welcome to Safety Toolbox Talk Bot!* 🛡️\n\n"
            "Please select your work type:\n\n"
            "1️⃣ Excavation\n"
            "2️⃣ Welding\n"
            "3️⃣ Working at Height\n"
            "4️⃣ Electrical Work\n"
            "5️⃣ Confined Space\n\n"
            "🌐 Language / भाषा / भाषा निवडा:\n"
            "Type *hindi* for Hindi 🇮🇳\n"
            "Type *marathi* for Marathi\n\n"
            "🆘 Type *emergency* for Emergency Help"
        )

    elif message_text in ['1', 'excavation']:
        return (
            "⛏️ *EXCAVATION SAFETY*\n\n"
            "⚠️ *Hazards:*\n"
            "• Cave-in / soil collapse\n"
            "• Underground utilities\n"
            "• Falling objects\n"
            "• Water accumulation\n\n"
            "🦺 *PPE Required:*\n"
            "• Hard hat\n"
            "• Safety boots\n"
            "• High-visibility vest\n"
            "• Gloves\n\n"
            "✅ *Do's:*\n"
            "• Check underground utilities before digging\n"
            "• Shore up walls deeper than 1.2m\n"
            "• Keep spoil away from edges\n\n"
            "❌ *Don'ts:*\n"
            "• Never work alone in deep excavations\n"
            "• Don't ignore cracks in soil walls\n"
            "• Never store heavy material near edge\n\n"
            "Type *menu* to go back."
        )

    elif message_text in ['2', 'welding']:
        return (
            "🔥 *WELDING SAFETY*\n\n"
            "⚠️ *Hazards:*\n"
            "• Fire and explosion\n"
            "• Electric shock\n"
            "• Toxic fumes\n"
            "• UV radiation\n\n"
            "🦺 *PPE Required:*\n"
            "• Welding helmet\n"
            "• Fire-resistant gloves\n"
            "• Leather apron\n"
            "• Respirator mask\n\n"
            "✅ *Do's:*\n"
            "• Ensure good ventilation\n"
            "• Keep fire extinguisher nearby\n"
            "• Inspect equipment before use\n\n"
            "❌ *Don'ts:*\n"
            "• Never weld near flammable materials\n"
            "• Don't weld in wet conditions\n"
            "• Never look at arc without shield\n\n"
            "Type *menu* to go back."
        )

    elif message_text in ['3', 'height', 'working at height']:
        return (
            "🪜 *WORKING AT HEIGHT SAFETY*\n\n"
            "⚠️ *Hazards:*\n"
            "• Falls from ladders/scaffolding\n"
            "• Falling objects\n"
            "• Unstable platforms\n\n"
            "🦺 *PPE Required:*\n"
            "• Full body harness\n"
            "• Hard hat\n"
            "• Safety boots with grip\n"
            "• Lanyard / lifeline\n\n"
            "✅ *Do's:*\n"
            "• Use 3-point contact on ladders\n"
            "• Secure all tools with lanyards\n"
            "• Inspect harness before each use\n\n"
            "❌ *Don'ts:*\n"
            "• Never work at height without harness\n"
            "• Don't work in strong winds\n"
            "• Never overload scaffolding\n\n"
            "Type *menu* to go back."
        )

    elif message_text in ['4', 'electrical', 'electric']:
        return (
            "⚡ *ELECTRICAL SAFETY*\n\n"
            "⚠️ *Hazards:*\n"
            "• Electric shock\n"
            "• Arc flash burns\n"
            "• Fire from short circuit\n\n"
            "🦺 *PPE Required:*\n"
            "• Insulated gloves\n"
            "• Safety goggles\n"
            "• Arc flash suit\n"
            "• Insulated tools\n\n"
            "✅ *Do's:*\n"
            "• Always use LOTO (Lockout/Tagout)\n"
            "• Test before touch - verify power OFF\n"
            "• Work with a buddy\n\n"
            "❌ *Don'ts:*\n"
            "• Never work on live circuits alone\n"
            "• Don't use damaged cables\n"
            "• Never bypass safety switches\n\n"
            "Type *menu* to go back."
        )

    elif message_text in ['5', 'confined', 'confined space']:
        return (
            "🕳️ *CONFINED SPACE SAFETY*\n\n"
            "⚠️ *Hazards:*\n"
            "• Oxygen deficiency\n"
            "• Toxic gases\n"
            "• Engulfment\n"
            "• Heat stress\n\n"
            "🦺 *PPE Required:*\n"
            "• Gas detector\n"
            "• SCBA respirator\n"
            "• Harness with retrieval line\n"
            "• Communication device\n\n"
            "✅ *Do's:*\n"
            "• Always get Entry Permit\n"
            "• Test atmosphere before entry\n"
            "• Always have standby person outside\n\n"
            "❌ *Don'ts:*\n"
            "• Never enter without permit\n"
            "• Don't enter if gas levels unsafe\n"
            "• Never work alone inside\n\n"
            "Type *menu* to go back."
        )

    elif message_text in ['emergency', 'sos', 'accident', 'fire']:
        return (
            "🆘 *EMERGENCY RESPONSE* 🆘\n\n"
            "🔥 *FIRE:*\n"
            "1. Raise alarm immediately\n"
            "2. Call: 101 (Fire)\n"
            "3. Evacuate - don't use lifts\n"
            "4. Go to muster point\n\n"
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
            "Type *menu* to return."
        )

    elif message_text == 'hindi':
        return (
            "👷 *सेफ्टी टूलबॉक्स टॉक बॉट में आपका स्वागत है!* 🛡️\n\n"
            "अपना काम चुनें:\n\n"
            "1️⃣ खुदाई (Excavation)\n"
            "2️⃣ वेल्डिंग (Welding)\n"
            "3️⃣ ऊंचाई पर काम (Height)\n"
            "4️⃣ बिजली का काम (Electrical)\n"
            "5️⃣ बंद जगह (Confined Space)\n\n"
            "🆘 *आपातकाल* के लिए emergency टाइप करें\n\n"
            "नंबर 1-5 में से चुनें।"
        )

    elif message_text == 'marathi':
        return (
            "👷 *सेफ्टी टूलबॉक्स टॉक बॉटमध्ये आपले स्वागत आहे!* 🛡️\n\n"
            "तुमचे काम निवडा:\n\n"
            "1️⃣ खोदकाम (Excavation)\n"
            "2️⃣ वेल्डिंग (Welding)\n"
            "3️⃣ उंचावर काम (Height)\n"
            "4️⃣ विद्युत काम (Electrical)\n"
            "5️⃣ बंद जागा (Confined Space)\n\n"
            "🆘 आणीबाणीसाठी emergency टाइप करा\n\n"
            "1-5 मधून निवडा।"
        )

    else:
        return (
            "❓ I didn't understand that.\n\n"
            "Type *menu* or *hi* to see the main menu.\n"
            "Type *emergency* for emergency help. 🆘\n\n"
            "हिंदी के लिए *hindi* टाइप करें\n"
            "मराठीसाठी *marathi* टाइप करा"
        )


def send_whatsapp_message(to_number, message_text):
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
            print(f"Message sent successfully to {to_number}")
        else:
            print(f"Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)
