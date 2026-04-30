import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PHONE_NUMBER_ID = "1202684002920267"

user_sessions = {}

MESSAGES = {
    "welcome": "Welcome to Safety Toolbox Talk Bot!

Please select your language:
1 - English
2 - Hindi
3 - Marathi

Reply with 1, 2 or 3",
    "menu_en": "SAFETY TOOLBOX TALK

Select work type:
1 - Excavation Work
2 - Welding Work
3 - Work at Height
4 - Electrical Work
5 - Confined Space
6 - Emergency Numbers

Reply with a number 1 to 6",
    "menu_hi": "SURAKSHA TOOLBOX TALK

Karya prakar chunen:
1 - Khudaai
2 - Welding
3 - Unchaai par Karya
4 - Vidyut Karya
5 - Seemit Sthan
6 - Aapatkaaleen Numbers

1 se 6 bhejein",
    "menu_mr": "SURAKSHA TOOLBOX TALK

Kamache prakar nivada:
1 - Khodai Kam
2 - Welding Kam
3 - Unchivare Kam
4 - Vidyut Kam
5 - Maryadit Jaga
6 - Aapatkaaleen Kramank

1 te 6 pathava",
    "excavation_en": "EXCAVATION WORK - Safety Tips

- Check underground utilities before digging
- Slope or shore trench walls
- Keep soil 2 ft away from edge
- Use ladder for entry and exit
- Inspect trench daily and after rain
- Wear hard hat, safety boots and vest
- Never work under suspended loads

WARNING: Never enter unprotected trench!

Reply MENU to go back",
    "excavation_hi": "KHUDAAI KARYA - Suraksha Tips

- Khudaai se pehle lines jaanchein
- Khaai ko dhalan dein
- Mitti 2 feet door rakhein
- Seedhi use karein
- Roz jaanch karein
- Helmet aur joote pehnen

CHETAVNI: Bina suraksha na utarein!

Vaapas ke liye MENU likhein",
    "excavation_mr": "KHODAI KAM - Suraksha Tips

- Khodnyapurvi line tapasa
- Khandakala utar dya
- Mati 2 fut dur theva
- Shidi vapra
- Darroj tapasa
- Helmet ani but ghala

ISHARA: Asurakshit khandakat jaau naka!

Parat janysathi MENU likha",
    "welding_en": "WELDING WORK - Safety Tips

- Wear welding helmet, gloves and apron
- Ensure proper ventilation
- Keep fire extinguisher nearby
- Remove flammable materials
- Never weld near gas cylinders
- Check cables before use
- Use welding screens

WARNING: UV rays can cause blindness!

Reply MENU to go back",
    "welding_hi": "WELDING KARYA - Suraksha Tips

- Helmet aur dastane pehnen
- Ventilation rakhen
- Aghnishamak yantra rakhein
- Gas cylinder ke paas na karein
- Cable jaanchein

CHETAVNI: UV kiranen andhapan kar sakti hain!

Vaapas ke liye MENU likhein",
    "welding_mr": "WELDING KAM - Suraksha Tips

- Helmet ani hatmoje ghala
- Vayuvijan kara
- Aghnishamak theva
- Gas cylinder javaL welding nako
- Cable tapasa

ISHARA: UV kirananmule andhatva yeu shakate!

Parat janysathi MENU likha",
    "height_en": "WORK AT HEIGHT - Safety Tips

- Use fall arrest harness above 2 metres
- Inspect harness before every use
- Secure tools with lanyards
- Never stand on top rung of ladder
- Maintain 3 points of contact
- Use guardrails on open edges
- No work in strong winds

WARNING: Falls are number 1 cause of construction deaths!

Reply MENU to go back",
    "height_hi": "UNCHAAI PAR KARYA - Suraksha Tips

- 2 meter se upar harness pehnen
- Harness jaanchein
- Auzar lanyard se bandhein
- Seedhi par 3 point contact rakhein
- Railing lagaayein
- Tez hawa mein kaam na karein

CHETAVNI: Girana mrityu ka number 1 kaaran!

Vaapas ke liye MENU likhein",
    "height_mr": "UNCHIVARE KAM - Suraksha Tips

- 2 meter var harness ghala
- Harness tapasa
- Sadane lanyard ne bandha
- 3 point contact theva
- Railing lava
- Jordar varyat kam nako

ISHARA: Padane he number 1 kaaran ahe!

Parat janysathi MENU likha",
    "electrical_en": "ELECTRICAL WORK - Safety Tips

- Use Lockout Tagout before work
- Use insulated tools only
- Wear rubber gloves and safety boots
- Never work on live circuits alone
- Keep water away from panels
- Test with voltage tester before touching
- Use RCD on portable equipment

WARNING: Assume every wire is LIVE!

Reply MENU to go back",
    "electrical_hi": "VIDYUT KARYA - Suraksha Tips

- Lockout Tagout karein
- Insulated upkaran use karein
- Rubber dastane pehnen
- Live circuit par akele na karein
- Paani door rakhein
- Voltage tester se jaanchein

CHETAVNI: Har taar LIVE samjhein!

Vaapas ke liye MENU likhein",
    "electrical_mr": "VIDYUT KAM - Suraksha Tips

- Lockout Tagout kara
- Insulated sadane vapra
- Rubber hatmoje ghala
- Live circuit var ekate nako
- Pani dur theva
- Voltage tester vapra

ISHARA: Pratyek tar LIVE samja!

Parat janysathi MENU likha",
    "confined_en": "CONFINED SPACE - Safety Tips

- Test atmosphere before entry
- Get Permit to Work signed
- Have standby person outside
- Use continuous gas monitor
- Wear full body harness
- Never use open flame
- Know emergency rescue plan

WARNING: Never enter alone!

Reply MENU to go back",
    "confined_hi": "SEEMIT STHAN - Suraksha Tips

- Vatavaran jaanchein
- Permit to Work lein
- Standby vyakti rakhein
- Gas monitor use karein
- Harness pehnen
- Khuli lau na jalaayein

CHETAVNI: Akele kabhi na jaayein!

Vaapas ke liye MENU likhein",
    "confined_mr": "MARYADIT JAGA - Suraksha Tips

- Vatavaran tapasa
- Permit to Work ghya
- Standby vyakti theva
- Gas monitor vapra
- Harness ghala
- Ughadi jyot nako

ISHARA: Ekate jaau naka!

Parat janysathi MENU likha",
    "emergency_en": "EMERGENCY NUMBERS - INDIA

Medical: 108
Fire: 101
Police: 100
Ambulance: 102
Disaster: 1078

IF ACCIDENT HAPPENS:
1. Call 108 immediately
2. Do not move injured person
3. Inform site supervisor
4. Secure the area

Reply MENU to go back",
    "emergency_hi": "AAPATKAALEEN NUMBERS - INDIA

Chikitsa: 108
Damkal: 101
Pulis: 100
Ambulance: 102
Aapda: 1078

DURGHATNA MEIN:
1. 108 par call karein
2. Ghaayal ko na hilaayein
3. Supervisor ko batayein
4. Jagah surakshit karein

Vaapas ke liye MENU likhein",
    "emergency_mr": "AAPATKAALEEN KRAMANK - INDIA

Vaidyakiya: 108
Agnishamak: 101
Police: 100
Rughnavahika: 102
Aapatti: 1078

APGHATACHYA VELI:
1. 108 var call kara
2. Jakhami la halavu naka
3. Supervisor la kalava
4. Parisara surakshit kara

Parat janysathi MENU likha",
    "unknown_en": "I did not understand that.

Reply MENU to see the main menu or send 1 to 6.",
    "unknown_hi": "Samajh nahi aaya.

MENU likhein ya 1 se 6 bhejein.",
    "unknown_mr": "Samajale nahi.

MENU likha kiva 1 te 6 pathava.",
}


def send_message(to, message):
    url = "https://graph.facebook.com/v18.0/" + PHONE_NUMBER_ID + "/messages"
    headers = {
        "Authorization": "Bearer " + str(WHATSAPP_TOKEN),
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def handle_message(from_number, text):
    text = text.strip().lower()
    lang = user_sessions.get(from_number, None)

    if lang is None:
        if text in ["1", "english"]:
            user_sessions[from_number] = "en"
            send_message(from_number, MESSAGES["menu_en"])
        elif text in ["2", "hindi"]:
            user_sessions[from_number] = "hi"
            send_message(from_number, MESSAGES["menu_hi"])
        elif text in ["3", "marathi"]:
            user_sessions[from_number] = "mr"
            send_message(from_number, MESSAGES["menu_mr"])
        else:
            send_message(from_number, MESSAGES["welcome"])
        return

    if text in ["menu", "hi", "hello", "start", "help"]:
        user_sessions.pop(from_number, None)
        send_message(from_number, MESSAGES["welcome"])
        return

    topic_map = {
        "1": "excavation",
        "2": "welding",
        "3": "height",
        "4": "electrical",
        "5": "confined",
        "6": "emergency",
    }

    if text in topic_map:
        key = topic_map[text] + "_" + lang
        send_message(from_number, MESSAGES.get(key, MESSAGES["unknown_" + lang]))
    else:
        send_message(from_number, MESSAGES["unknown_" + lang])


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    try:
        entries = data.get("entry", [])
        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for message in messages:
                    if message.get("type") == "text":
                        from_number = message["from"]
                        text = message["text"]["body"]
                        handle_message(from_number, text)
    except Exception as e:
        print("Error: " + str(e))
    return jsonify({"status": "ok"}), 200


@app.route("/", methods=["GET"])
def home():
    return "Safety Toolbox Talk Bot is running!", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)