import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ─── Credentials from Environment Variables ───────────────────────────────────
WHATSAPP_TOKEN = os.environ.get('WHATSAPP_TOKEN')
VERIFY_TOKEN   = os.environ.get('VERIFY_TOKEN')
PHONE_NUMBER_ID = '1202684002920267'

# ─── Multilingual Messages ────────────────────────────────────────────────────
MESSAGES = {
    'welcome': {
        'en': (
            "👷 *Welcome to Safety Toolbox Talk Bot!*\n\n"
            "Please select your language:\n"
            "1️⃣ English\n"
            "2️⃣ हिंदी (Hindi)\n"
            "3️⃣ मराठी (Marathi)\n\n"
            "Reply with 1, 2 or 3"
        ),
    },
    'main_menu': {
        'en': (
            "🦺 *SAFETY TOOLBOX TALK*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Select work type:\n\n"
            "1️⃣ Excavation Work\n"
            "2️⃣ Welding Work\n"
            "3️⃣ Work at Height\n"
            "4️⃣ Electrical Work\n"
            "5️⃣ Confined Space\n"
            "6️⃣ 🚨 Emergency Numbers\n\n"
            "Reply with a number (1-6)"
        ),
        'hi': (
            "🦺 *सुरक्षा टूलबॉक्स टॉक*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "कार्य प्रकार चुनें:\n\n"
            "1️⃣ खुदाई कार्य\n"
            "2️⃣ वेल्डिंग कार्य\n"
            "3️⃣ ऊंचाई पर कार्य\n"
            "4️⃣ विद्युत कार्य\n"
            "5️⃣ सीमित स्थान\n"
            "6️⃣ 🚨 आपातकालीन नंबर\n\n"
            "1 से 6 के बीच नंबर भेजें"
        ),
        'mr': (
            "🦺 *सुरक्षा टूलबॉक्स टॉक*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "कामाचा प्रकार निवडा:\n\n"
            "1️⃣ खोदाई काम\n"
            "2️⃣ वेल्डिंग काम\n"
            "3️⃣ उंचीवर काम\n"
            "4️⃣ विद्युत काम\n"
            "5️⃣ मर्यादित जागा\n"
            "6️⃣ 🚨 आपत्कालीन क्रमांक\n\n"
            "1 ते 6 मधील क्रमांक पाठवा"
        ),
    },
    'excavation': {
        'en': (
            "⛏️ *EXCAVATION WORK — Safety Tips*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ Check for underground utilities before digging\n"
            "✅ Slope, shore or shield trench walls\n"
            "✅ Keep excavated soil 2 ft away from edge\n"
            "✅ Use ladder for entry/exit (max 25 ft spacing)\n"
            "✅ Inspect trench daily and after rain\n"
            "✅ Wear hard hat, safety boots & hi-vis vest\n"
            "✅ Never work under suspended loads\n\n"
            "⚠️ *Never enter an unprotected trench!*\n\n"
            "Reply *MENU* to go back"
        ),
        'hi': (
            "⛏️ *खुदाई कार्य — सुरक्षा सुझाव*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ खुदाई से पहले भूमिगत लाइनें जांचें\n"
            "✅ खाई की दीवारों को ढलान दें या सहारा दें\n"
            "✅ खोदी गई मिट्टी किनारे से 2 फीट दूर रखें\n"
            "✅ प्रवेश/निकास के लिए सीढ़ी का उपयोग करें\n"
            "✅ खाई की रोज और बारिश के बाद जांच करें\n"
            "✅ हेलमेट, सुरक्षा जूते और हाई-विज़ वेस्ट पहनें\n"
            "✅ लटके हुए भार के नीचे कभी काम न करें\n\n"
            "⚠️ *बिना सुरक्षा के खाई में कभी न उतरें!*\n\n"
            "वापस जाने के लिए *MENU* लिखें"
        ),
        'mr': (
            "⛏️ *खोदाई काम — सुरक्षा टिप्स*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ खोदण्यापूर्वी भूमिगत लाईन तपासा\n"
            "✅ खंदकाच्या भिंतींना उतार द्या किंवा आधार द्या\n"
            "✅ खोदलेली माती काठापासून 2 फूट दूर ठेवा\n"
            "✅ प्रवेश/बाहेर पडण्यासाठी शिडी वापरा\n"
            "✅ खंदक दररोज आणि पावसानंतर तपासा\n"
            "✅ हेल्मेट, सुरक्षा बूट आणि हाय-विज वेस्ट घाला\n"
            "✅ लटकलेल्या भाराखाली कधीही काम करू नका\n\n"
            "⚠️ *असुरक्षित खंदकात कधीही प्रवेश करू नका!*\n\n"
            "परत जाण्यासाठी *MENU* लिहा"
        ),
    },
    'welding': {
        'en': (
            "🔥 *WELDING WORK — Safety Tips*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ Wear welding helmet, gloves & leather apron\n"
            "✅ Ensure proper ventilation / use exhaust fan\n"
            "✅ Keep fire extinguisher nearby\n"
            "✅ Remove flammable materials from work area\n"
            "✅ Never weld near gas cylinders\n"
            "✅ Check cables and connections before use\n"
            "✅ Use welding screens to protect others\n\n"
            "⚠️ *UV rays from welding can cause blindness!*\n\n"
            "Reply *MENU* to go back"
        ),
        'hi': (
            "🔥 *वेल्डिंग कार्य — सुरक्षा सुझाव*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ वेल्डिंग हेलमेट, दस्ताने और चमड़े का एप्रन पहनें\n"
            "✅ उचित वेंटिलेशन सुनिश्चित करें\n"
            "✅ पास में अग्निशामक यंत्र रखें\n"
            "✅ कार्य क्षेत्र से ज्वलनशील सामग्री हटाएं\n"
            "✅ गैस सिलेंडर के पास कभी वेल्डिंग न करें\n"
            "✅ उपयोग से पहले केबल और कनेक्शन जांचें\n"
            "✅ दूसरों की सुरक्षा के लिए वेल्डिंग स्क्रीन लगाएं\n\n"
            "⚠️ *वेल्डिंग की UV किरणें अंधापन कर सकती हैं!*\n\n"
            "वापस जाने के लिए *MENU* लिखें"
        ),
        'mr': (
            "🔥 *वेल्डिंग काम — सुरक्षा टिप्स*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ वेल्डिंग हेल्मेट, हातमोजे आणि चामड्याचा एप्रन घाला\n"
            "✅ योग्य वायुवीजन सुनिश्चित करा\n"
            "✅ जवळ अग्निशामक यंत्र ठेवा\n"
            "✅ कामाच्या ठिकाणाहून ज्वलनशील साहित्य काढा\n"
            "✅ गॅस सिलिंडरजवळ कधीही वेल्डिंग करू नका\n"
            "✅ वापरण्यापूर्वी केबल आणि कनेक्शन तपासा\n"
            "✅ इतरांच्या संरक्षणासाठी वेल्डिंग स्क्रीन लावा\n\n"
            "⚠️ *वेल्डिंगच्या UV किरणांमुळे अंधत्व येऊ शकते!*\n\n"
            "परत जाण्यासाठी *MENU* लिहा"
        ),
    },
    'height': {
        'en': (
            "🪜 *WORK AT HEIGHT — Safety Tips*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ Always use fall arrest harness above 2 metres\n"
            "✅ Inspect harness before every use\n"
            "✅ Secure tools with lanyards — no loose items\n"
            "✅ Never stand on top rung of ladder\n"
            "✅ Maintain 3 points of contact on ladders\n"
            "✅ Use guardrails on all open edges\n"
            "✅ Check weather — no work in strong winds\n\n"
            "⚠️ *Falls are the #1 cause of construction deaths!*\n\n"
            "Reply *MENU* to go back"
        ),
        'hi': (
            "🪜 *ऊंचाई पर कार्य — सुरक्षा सुझाव*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ 2 मीटर से ऊपर हमेशा फॉल अरेस्ट हार्नेस पहनें\n"
            "✅ हर उपयोग से पहले हार्नेस की जांच करें\n"
            "✅ औजारों को लैनयार्ड से बांधें\n"
            "✅ सीढ़ी की सबसे ऊपरी पायदान पर कभी न खड़े हों\n"
            "✅ सीढ़ी पर 3-पॉइंट संपर्क बनाए रखें\n"
            "✅ सभी खुले किनारों पर रेलिंग लगाएं\n"
            "✅ मौसम जांचें — तेज हवा में काम न करें\n\n"
            "⚠️ *ऊंचाई से गिरना निर्माण मृत्यु का #1 कारण है!*\n\n"
            "वापस जाने के लिए *MENU* लिखें"
        ),
        'mr': (
            "🪜 *उंचीवर काम — सुरक्षा टिप्स*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ 2 मीटरपेक्षा जास्त उंचीवर नेहमी फॉल अरेस्ट हार्नेस घाला\n"
            "✅ प्रत्येक वापरापूर्वी हार्नेस तपासा\n"
            "✅ साधने लॅनयार्डने बांधा\n"
            "✅ शिडीच्या सर्वात वरच्या पायरीवर कधीही उभे राहू नका\n"
            "✅ शिडीवर 3-पॉइंट संपर्क ठेवा\n"
            "✅ सर्व उघड्या कडांवर रेलिंग लावा\n"
            "✅ हवामान तपासा — जोरदार वाऱ्यात काम करू नका\n\n"
            "⚠️ *उंचीवरून पडणे हे बांधकाम मृत्यूचे #1 कारण आहे!*\n\n"
            "परत जाण्यासाठी *MENU* लिहा"
        ),
    },
    'electrical': {
        'en': (
            "⚡ *ELECTRICAL WORK — Safety Tips*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ Always use LOTO (Lockout/Tagout) before work\n"
            "✅ Use insulated tools only\n"
            "✅ Wear rubber gloves and safety boots\n"
            "✅ Never work on live circuits alone\n"
            "✅ Keep water away from electrical panels\n"
            "✅ Test with voltage tester before touching\n"
            "✅ Use RCD/ELCB on all portable equipment\n\n"
            "⚠️ *Assume every wire is LIVE until proven safe!*\n\n"
            "Reply *MENU* to go back"
        ),
        'hi': (
            "⚡ *विद्युत कार्य — सुरक्षा सुझाव*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ काम से पहले हमेशा LOTO (लॉकआउट/टैगआउट) करें\n"
            "✅ केवल इंसुलेटेड उपकरणों का उपयोग करें\n"
            "✅ रबर दस्ताने और सुरक्षा जूते पहनें\n"
            "✅ लाइव सर्किट पर अकेले कभी काम न करें\n"
            "✅ विद्युत पैनल से पानी दूर रखें\n"
            "✅ छूने से पहले वोल्टेज टेस्टर से जांचें\n"
            "✅ सभी पोर्टेबल उपकरणों पर RCD/ELCB का उपयोग करें\n\n"
            "⚠️ *हर तार को LIVE समझें जब तक सुरक्षित साबित न हो!*\n\n"
            "वापस जाने के लिए *MENU* लिखें"
        ),
        'mr': (
            "⚡ *विद्युत काम — सुरक्षा टिप्स*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ कामापूर्वी नेहमी LOTO (लॉकआउट/टॅगआउट) करा\n"
            "✅ फक्त इन्सुलेटेड साधने वापरा\n"
            "✅ रबर हातमोजे आणि सुरक्षा बूट घाला\n"
            "✅ लाईव्ह सर्किटवर एकट्याने कधीही काम करू नका\n"
            "✅ विद्युत पॅनेलपासून पाणी दूर ठेवा\n"
            "✅ स्पर्श करण्यापूर्वी व्होल्टेज टेस्टरने तपासा\n"
            "✅ सर्व पोर्टेबल उपकरणांवर RCD/ELCB वापरा\n\n"
            "⚠️ *प्रत्येक तार LIVE समजा जोपर्यंत सुरक्षित सिद्ध होत नाही!*\n\n"
            "परत जाण्यासाठी *MENU* लिहा"
        ),
    },
    'confined': {
        'en': (
            "🕳️ *CONFINED SPACE — Safety Tips*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ Test atmosphere before entry (O2, CO, H2S)\n"
            "✅ Get Permit to Work signed before entering\n"
            "✅ Always have a standby person outside\n"
            "✅ Use continuous gas monitor inside\n"
            "✅ Wear full body harness with retrieval line\n"
            "✅ Never use open flame for lighting\n"
            "✅ Know your emergency rescue plan\n\n"
            "⚠️ *Never enter alone — rescue must be pre-planned!*\n\n"
            "Reply *MENU* to go back"
        ),
        'hi': (
            "🕳️ *सीमित स्थान — सुरक्षा सुझाव*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ प्रवेश से पहले वातावरण जांचें (O2, CO, H2S)\n"
            "✅ प्रवेश से पहले Permit to Work साइन करवाएं\n"
            "✅ हमेशा बाहर एक स्टैंडबाय व्यक्ति रखें\n"
            "✅ अंदर निरंतर गैस मॉनिटर का उपयोग करें\n"
            "✅ रिट्रीवल लाइन के साथ फुल बॉडी हार्नेस पहनें\n"
            "✅ रोशनी के लिए खुली लौ कभी न जलाएं\n"
            "✅ आपातकालीन बचाव योजना जानें\n\n"
            "⚠️ *अकेले कभी प्रवेश न करें — बचाव पहले से योजनाबद्ध हो!*\n\n"
            "वापस जाने के लिए *MENU* लिखें"
        ),
        'mr': (
            "🕳️ *मर्यादित जागा — सुरक्षा टिप्स*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ प्रवेशापूर्वी वातावरण तपासा (O2, CO, H2S)\n"
            "✅ प्रवेशापूर्वी Permit to Work साइन करा\n"
            "✅ नेहमी बाहेर एक स्टँडबाय व्यक्ती ठेवा\n"
            "✅ आत सतत गॅस मॉनिटर वापरा\n"
            "✅ रिट्रीव्हल लाईनसह फुल बॉडी हार्नेस घाला\n"
            "✅ प्रकाशासाठी उघडी ज्योत कधीही पेटवू नका\n"
            "✅ आपत्कालीन बचाव योजना जाणून घ्या\n\n"
            "⚠️ *एकट्याने कधीही प्रवेश करू नका — बचाव आधीच नियोजित असावा!*\n\n"
            "परत जाण्यासाठी *MENU* लिहा"
        ),
    },
    'emergency': {
        'en': (
            "🚨 *EMERGENCY NUMBERS — INDIA*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🏥 Medical Emergency: *108*\n"
            "🚒 Fire Brigade: *101*\n"
            "👮 Police: *100*\n"
            "🚑 Ambulance: *102*\n"
            "⛑️ Disaster Management: *1078*\n\n"
            "📢 *IN CASE OF ACCIDENT:*\n"
            "1. Call 108 immediately\n"
            "2. Don't move injured person\n"
            "3. Inform site supervisor\n"
            "4. Secure the area\n\n"
            "Reply *MENU* to go back"
        ),
        'hi': (
            "🚨 *आपातकालीन नंबर — भारत*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🏥 चिकित्सा आपातकाल: *108*\n"
            "🚒 दमकल: *101*\n"
            "👮 पुलिस: *100*\n"
            "🚑 एम्बुलेंस: *102*\n"
            "⛑️ आपदा प्रबंधन: *1078*\n\n"
            "📢 *दुर्घटना की स्थिति में:*\n"
            "1. तुरंत 108 पर कॉल करें\n"
            "2. घायल व्यक्ति को न हिलाएं\n"
            "3. साइट सुपरवाइजर को सूचित करें\n"
            "4. क्षेत्र को सुरक्षित करें\n\n"
            "वापस जाने के लिए *MENU* लिखें"
        ),
        'mr': (
            "🚨 *आपत्कालीन क्रमांक — भारत*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🏥 वैद्यकीय आपत्काल: *108*\n"
            "🚒 अग्निशमन दल: *101*\n"
            "👮 पोलीस: *100*\n"
            "🚑 रुग्णवाहिका: *102*\n"
            "⛑️ आपत्ती व्यवस्थापन: *1078*\n\n"
            "📢 *अपघाताच्या वेळी:*\n"
            "1. ताबडतोब 108 वर कॉल करा\n"
            "2. जखमी व्यक्तीला हलवू नका\n"
            "3. साइट सुपरवायझरला कळवा\n"
            "4. परिसर सुरक्षित करा\n\n"
            "परत जाण्यासाठी *MENU* लिहा"
        ),
    },
    'unknown': {
        'en': "❓ I didn't understand that.\n\nReply *MENU* to see the main menu or send 1-6 to select a topic.",
        'hi': "❓ मैं यह नहीं समझा।\n\nमुख्य मेनू देखने के लिए *MENU* लिखें या विषय चुनने के लिए 1-6 भेजें।",
        'mr': "❓ मला ते समजले नाही.\n\nमुख्य मेनू पाहण्यासाठी *MENU* लिहा किंवा विषय निवडण्यासाठी 1-6 पाठवा.",
    }
}

# ─── User Session Store (in-memory) ──────────────────────────────────────────
user_sessions = {}  # { phone_number: 'en' / 'hi' / 'mr' }

# ─── Send WhatsApp Message ────────────────────────────────────────────────────
def send_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
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

# ─── Get message for user's language ─────────────────────────────────────────
def get_msg(key, lang):
    msg = MESSAGES.get(key, {})
    return msg.get(lang) or msg.get('en', "Sorry, message not available.")

# ─── Handle Incoming Message ──────────────────────────────────────────────────
def handle_message(from_number, text):
    text = text.strip().lower()
    lang  = user_sessions.get(from_number, None)

    # Language not selected yet
    if lang is None:
        if text in ['1', 'english']:
            user_sessions[from_number] = 'en'
            send_message(from_number, get_msg('main_menu', 'en'))
        elif text in ['2', 'hindi', 'हिंदी']:
            user_sessions[from_number] = 'hi'
            send_message(from_number, get_msg('main_menu', 'hi'))
        elif text in ['3', 'marathi', 'मराठी']:
            user_sessions[from_number] = 'mr'
            send_message(from_number, get_msg('main_menu', 'mr'))
        else:
            send_message(from_number, MESSAGES['welcome']['en'])
        return

    # Main menu navigation
    if text in ['menu', 'hi', 'hello', 'start', 'help', 'नमस्ते', 'नमस्कार']:
        user_sessions.pop(from_number, None)  # reset language on MENU
        send_message(from_number, MESSAGES['welcome']['en'])
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
        send_message(from_number, get_msg(topic_map[text], lang))
    else:
        send_message(from_number, get_msg('unknown', lang))

# ─── Webhook Routes ───────────────────────────────────────────────────────────
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode      = request.args.get('hub.mode')
    token     = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("✅ Webhook verified!")
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
                        text        = message['text']['body']
                        print(f"📩 Message from {from_number}: {text}")
                        handle_message(from_number, text)
    except Exception as e:
        print(f"❌ Error: {e}")
    return jsonify({"status": "ok"}), 200


@app.route('/', methods=['GET'])
def home():
    return "🦺 Safety Toolbox Talk Bot is running!", 200


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)