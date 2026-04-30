import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

WHATSAPP_TOKEN = os.environ.get('WHATSAPP_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
PHONE_NUMBER_ID = '1202684002920267'

user_sessions = {}

MESSAGES = {
    'welcome': "Welcome to Safety Toolbox Talk Bot!\n\nPlease select your language:\n1 - English\n2 - Hindi\n3 - Marathi\n\nReply with 1, 2 or 3",
    'main_menu_en': "SAFETY TOOLBOX TALK\n\nSelect work type:\n1 - Excavation Work\n2 - Welding Work\n3 - Work at Height\n4 - Electrical Work\n5 - Confined Space\n6 - Emergency Numbers\n\nReply with a number 1 to 6",
    'main_menu_hi': "SURAKSHA TOOLBOX TALK\n\nKarya prakar chunen:\n1 - Khudaai Karya\n2 - Welding Karya\n3 - Unchaai par Karya\n4 - Vidyut Karya\n5 - Seemit Sthan\n6 - Aapatkaaleen Numbers\n\n1 se 6 ke beech number bhejein",
    'main_menu_mr': "SURAKSHA TOOLBOX TALK\n\nKamache prakar nivada:\n1 - Khodai Kam\n2 - Welding Kam\n3 - Unchivare Kam\n4 - Vidyut Kam\n5 - Maryadit Jaga\n6 - Aapatkaaleen Kramank\n\n1 te 6 madhil kramank pathava",
    'excavation_en': "EXCAVATION WORK - Safety Tips\n\n- Check for underground utilities before digging\n- Slope or shore trench walls\n- Keep excavated soil 2 ft away from edge\n- Use ladder for entry and exit\n- Inspect trench daily and after rain\n- Wear hard hat, safety boots and hi-vis vest\n- Never work under suspended loads\n\nWARNING: Never enter an unprotected trench!\n\nReply MENU to go back",
    'excavation_hi': "KHUDAAI KARYA - Suraksha Sujhaav\n\n- Khudaai se pehle bhumiget lines jaanchein\n- Khaai ki diwaaron ko dhalan dein\n- Khodi gayi mitti 2 feet door rakhein\n- Pravesh ke liye seedhi ka upyog karein\n- Khaai ki roz jaanch karein\n- Helmet aur joote pehnen\n\nCHETAVNI: Bina suraksha khaai mein na utarein!\n\nVaapas ke liye MENU likhein",
    'excavation_mr': "KHODAI KAM - Suraksha Tips\n\n- Khodnyapurvi bhumiget line tapasa\n- Khandakachya bhintianna utar dya\n- Mati 2 fut dur theva\n- Shidi vapra\n- Khandak darroj tapasa\n- Helmet ani but ghala\n\nISHARA: Asurakshit khandakat pravesh karu naka!\n\nParat janysathi MENU likha",
    'welding_en': "WELDING WORK - Safety Tips\n\n- Wear welding helmet, gloves and leather apron\n- Ensure proper ventilation\n- Keep fire extinguisher nearby\n- Remove flammable materials from work area\n- Never weld near gas cylinders\n- Check cables before use\n- Use welding screens to protect others\n\nWARNING: UV rays from welding can cause blindness!\n\nReply MENU to go back",
    'welding_hi': "WELDING KARYA - Suraksha Sujhaav\n\n- Welding helmet aur dastane pehnen\n- Ventilation sunischit karein\n- Aghnishamak yantra rakhein\n- Gas cylinder ke paas welding na karein\n- Cable jaanchein\n\nCHETAVNI: UV kiranen andhapan kar sakti hain!\n\nVaapas ke liye MENU likhein",
    'welding_mr': "WELDING KAM - Suraksha Tips\n\n- Welding helmet ani hatmoje ghala\n- Vayuvijan kara\n- Aghnishamak yantra theva\n- Gas cylinder javaḷ welding karu naka\n- Cable tapasa\n\nISHARA: UV kirananche andhatva yeu shakate!\n\nParat janysathi MENU likha",
    'height_en': "WORK AT HEIGHT - Safety Tips\n\n- Always use fall arrest harness above 2 metres\n- Inspect harness before every use\n- Secure tools with lanyards\n- Never stand on top rung of ladder\n- Maintain 3 points of contact on ladders\n- Use guardrails on all open edges\n- No work in strong winds\n\nWARNING: Falls are the number 1 cause of construction deaths!\n\nReply MENU to go back",
    'height_hi': "UNCHAAI PAR KARYA - Suraksha Sujhaav\n\n- 2 meter se upar harness pehnen\n- Harness jaanchein\n- Auzaron ko lanyard se bandhein\n- Seedhi par 3 point contact rakhein\n- Railing lagaayein\n- Tez hawa mein kaam na karein\n\nCHETAVNI: Girana nirmaan mrityu ka number 1 kaaran hai!\n\nVaapas ke liye MENU likhein",
    'height_mr': "UNCHIVARE KAM - Suraksha Tips\n\n- 2 meter var harness ghala\n- Harness tapasa\n- Sadane lanyard ne bandha\n- Shidiver 3 point contact theva\n- Railing lava\n- Jordar varyat kam karu naka\n\nISHARA: Padane he bandhakam mrityu karananche number 1 kaaran ahe!\n\nParat janysathi MENU likha",
    'electrical_en': "ELECTRICAL WORK - Safety Tips\n\n- Always use Lockout Tagout before work\n- Use insulated tools only\n- Wear rubber gloves and safety boots\n- Never work on live circuits alone\n- Keep water away from electrical panels\n- Test with voltage tester before touching\n- Use RCD on all portable equipment\n\nWARNING: Assume every wire is LIVE until proven safe!\n\nReply MENU to go back",
    'electrical_hi': "VIDYUT KARYA - Suraksha Sujhaav\n\n- Lockout Tagout karein\n- Insulated upkaran upyog karein\n- Rubber dastane pehnen\n- Live circuit par akele kaam na karein\n- Panel se paani door rakhein\n- Voltage tester se jaanchein\n\nCHETAVNI: Har taar ko LIVE samjhein!\n\nVaapas ke liye MENU likhein",
    'electrical_mr': "VIDYUT KAM - Suraksha Tips\n\n- Lockout Tagout kara\n- Insulated sadane vapra\n- Rubber hatmoje ghala\n- Live circuit var ekate kam karu naka\n- Panel pasun pani dur theva\n- Voltage tester ne tapasa\n\nISHARA: Pratyek tar LIVE samja!\n\nParat janysathi MENU likha",
    'confined_en': "CONFINED SPACE - Safety Tips\n\n- Test atmosphere before entry\n- Get Permit to Work signed\n- Always have a standby person outside\n- Use continuous gas monitor inside\n- Wear full body harness with retrieval line\n- Never use open flame for lighting\n- Know your emergency rescue plan\n\nWARNING: Never enter alone - rescue must be pre-planned!\n\nReply MENU to go back",
    'confined_hi': "SEEMIT STHAN - Suraksha Sujhaav\n\n- Pravesh se pehle vatavaran jaanchein\n- Permit to Work sign karvaayein\n- Standby vyakti rakhein\n- Gas monitor upyog karein\n- Harness pehnen\n- Khuli lau na jalaayein\n\nCHETAVNI: Akele kabhi pravesh na karein!\n\nVaapas ke liye MENU likhein",
    'confined_mr': "MARYADIT JAGA - Suraksha Tips\n\n- Praveshapurvi vatavaran tapasa\n- Permit to Work sign kara\n- Standby vyakti theva\n- Gas monitor vapra\n- Harness ghala\n- Ughadi jyot petavu naka\n\nISHARA: Ekate kadhi pravesh karu naka!\n\nParat janysathi MENU likha",
    'emergency_en': "EMERGENCY NUMBERS - INDIA\n\nMedical Emergency: 108\nFire Brigade: 101\nPolice: 100\nAmbulance: 102\nDisaster Management: 1078\n\nIN CASE OF ACCIDENT:\n1. Call 108 immediately\n2. Do not move injured person\n3. Inform site supervisor\n4. Secure the area\n\nReply MENU to go back",
    'emergency_hi': "AAPATKAALEEN NUMBERS - INDIA\n\nChikitsa: 108\nDamkal: 101\nPulis: 100\nAmbulance: 102\nAapda: 1078\n\nDURGHATNA MEIN:\n1. 108 par call karein\n2. Ghaayal ko na hilaayein\n3. Supervisor ko soochit karein\n4. Kshetra surakshit karein\n\nVaapas ke liye MENU likhein",
    'emergency_mr': "AAPATKAALEEN KRAMANK - INDIA\n\nVaidyakiya: 108\nAgnishamak: 101\nPolice: 100\nRughnavahika: 102\nAapatti: 1078\n\nAPGHATACHYA VELI:\n1. 108 var call kara\n2. Jakhami la halavu naka\n3. Supervisor la kalava\n4. Parisara surakshit kara\n\nParat janysathi MENU likha",
    'unknown_en': "I did not understand that.\n\nReply MENU to see the main menu or send 1 to 6 to select a topic.",
    'unknown_hi': "Main yah nahin samjha.\n\nMukhya menu ke liye MENU likhein ya 1 se 6 bhejein.",
    'unknown_mr': "Mala te samajale nahi.\n\nMukhya menu sathi MENU likha kiva 1 te 6 pathava.",
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
        if text in ['1', 'english']:
            user_sessions[from_number] = 'en'
            send_message(from_number, MESSAGES['main_menu_en'])
        elif text in ['2', 'hindi']:
            user_sessions[from_number] = 'hi'
            send_message(from_number, MESSAGES['main_menu_hi'])
        elif text in ['3', 'marathi']:
            user_sessions[from_number] = 'mr'
            send_message(from_number, MESSAGES['main_menu_mr'])
        else:
            send_message(from_number, MESSAGES['welcome'])
        return

    if text in ['menu', 'hi', 'hello', 'start', 'help']:
        user_sessions.pop(from_number, None)
        send_message(from_number, MESSAGES['welcome'])
        return

    topic_map = {
        '1': 'excavation',
        '2': 'welding',
        '3': 'height',
        '4': 'electrical',
        '5': 'confined',
        '6': 'emergency',
    }

    if text in topic_map:
        key = topic_map[text] + '_' + lang
        send_message(from_number, MESSAGES.get(key, MESSAGES['unknown_' + lang]))
    else:
        send_message(from_number, MESSAGES['unknown_' + lang])


@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403


@app.route('/webhook', methods=['POST'])
def receive_message():
    data = request.get_json()
    try:
        entries = data.get('entry', [])
        for entry in entries:
            for change in entry.get('changes', []):
                value = change.get('value', {})
                messages = value.get('messages', [])
                for message in messages:
                    if message.get('type') == 'text':
                        from_number = message['from']
                        text = message['text']['body']
                        handle_message(from_number, text)
    except Exception as e:
        print("Error: " + str(e))
    return jsonify({"status": "ok"}), 200


@app.route('/', methods=['GET'])
def home():
    return "Safety Toolbox Talk Bot is running!", 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=False, host='0.0.0.0', port=port)