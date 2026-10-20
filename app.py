import os, json, urllib.request
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "-1001226098245"
DEVOTION_THREAD = 6736
PRAYER_THREAD = 6761

DECLARATIONS = [
    {
        "title": "I AM MORE THAN A CONQUEROR",
        "body": "You were not created to be defeated. The same Christ who conquered death, hell, and the grave lives in you. Every challenge you face today is already under your feet — not because of your strength, but because of His. Walk as the conqueror you already are.",
        "ref": "Romans 8:37",
        "verse": "Nay, in all these things we are more than conquerors through him that loved us."
    },
    {
        "title": "NO WEAPON FORMED AGAINST ME SHALL PROSPER",
        "body": "This is not a wish — it is a covenant promise. No plan of the enemy against your life, your family, your career, or your calling shall succeed. God has already ruled on the matter. What the enemy meant for evil, God has already turned for good. Rest in that verdict today.",
        "ref": "Isaiah 54:17",
        "verse": "No weapon that is formed against thee shall prosper."
    },
    {
        "title": "GOD HAS A PLAN FOR MY LIFE",
        "body": "Before a single day of your life was written, God had already written every one of them. You are not an accident and your life is not without direction. Even in uncertainty, His plan remains good, purposeful, and unshakeable. Trust the Author of your story.",
        "ref": "Jeremiah 29:11",
        "verse": "For I know the plans I have for you — plans to prosper you and not to harm you."
    },
    {
        "title": "I CAN DO ALL THINGS THROUGH CHRIST",
        "body": "This verse is not about pushing harder — it is about drawing deeper. You are not doing life by your own strength. Christ is your source. Every assignment He has called you to, He has already equipped you for. Step forward today knowing you are not alone.",
        "ref": "Philippians 4:13",
        "verse": "I can do all things through Christ which strengtheneth me."
    },
    {
        "title": "I DWELL IN THE SECRET PLACE",
        "body": "The secret place is not a location — it is a posture of the heart. When you begin your day in His presence, you carry that presence into every room you walk into. His shadow covers you: from fear, from danger, from the plans of the enemy. Dwell there, and nothing can touch what He covers.",
        "ref": "Psalm 91:1",
        "verse": "He that dwelleth in the secret place of the Most High shall abide under the shadow of the Almighty."
    },
    {
        "title": "MY STRENGTH IS RENEWED DAILY",
        "body": "Waiting on God is not passive — it is one of the most powerful acts of faith. When you choose stillness over striving, you position yourself to receive what only He can give. He renews what is depleted, restores what is weary, and lifts you to places your own effort never could. Be still and let Him fill you again.",
        "ref": "Isaiah 40:31",
        "verse": "They that wait upon the Lord shall renew their strength; they shall mount up with wings as eagles."
    },
    {
        "title": "THE KINGDOM OF GOD IS WITHIN ME",
        "body": "The Kingdom is not something you are waiting for — it has already come and taken up residence inside you. Righteousness, peace, and joy in the Holy Spirit are your daily inheritance. You are a carrier of the Kingdom. Everywhere you go today, bring it.",
        "ref": "Romans 14:17",
        "verse": "The kingdom of God is not meat and drink; but righteousness, and peace, and joy in the Holy Ghost."
    },
    {
        "title": "THE FIRE OF GOD BURNS IN ME",
        "body": "God's Word does not sit quietly in a heart that receives it — it burns. It consumes compromise, burns off fear, and ignites purpose. If the fire feels low today, return to His Word. Read it, speak it, pray it. The fire is not gone — it just needs fresh fuel.",
        "ref": "Jeremiah 23:29",
        "verse": "Is not my word like as a fire? saith the Lord."
    },
    {
        "title": "THE CHURCH SHALL PREVAIL",
        "body": "Jesus did not say the gates of hell might not prevail — He said they shall not. The Church is not on the defensive; she is on the offensive. The Kingdom is advancing and no power in hell, no political system, no cultural tide can stop what God has ordained to prevail. Stand firm. The Church wins.",
        "ref": "Matthew 16:18",
        "verse": "Upon this rock I will build my church; and the gates of hell shall not prevail against it."
    },
    {
        "title": "GREATER IS HE THAT IS IN ME",
        "body": "Whatever you are facing today — the Spirit inside you is greater. Greater than your fears. Greater than the obstacles. Greater than what the enemy has assembled against you. You do not face anything today that the Greater One has not already overcome. Walk in that confidence.",
        "ref": "1 John 4:4",
        "verse": "Greater is he that is in you, than he that is in the world."
    },
    {
        "title": "THE EARTH SHALL BE FILLED WITH HIS GLORY",
        "body": "This is not a possibility — it is a prophecy. The earth will be full of the knowledge of His glory. You are part of how that happens. Through your prayer, your obedience, your witness. Every time you carry His presence into a room, His glory fills more of the earth. Do it today.",
        "ref": "Habakkuk 2:14",
        "verse": "The earth shall be filled with the knowledge of the glory of the Lord, as the waters cover the sea."
    },
    {
        "title": "I AM COVERED BY THE BLOOD OF JESUS",
        "body": "The blood of Jesus is not just a doctrine — it is your daily covering. It speaks on your behalf before the throne of God. It silences every accusation of the enemy. It opens doors that no human key can unlock. Plead it over your life today. Over your family. Over every assignment God has placed in your hands.",
        "ref": "Revelation 12:11",
        "verse": "They overcame him by the blood of the Lamb, and by the word of their testimony."
    },
    {
        "title": "I AM FILLED WITH THE SPIRIT OF GOD",
        "body": "The Spirit of God is not a feeling — He is a Person. When you declare that you are filled with the Spirit, you are aligning yourself with the truth of Ephesians 5:18. You are not asking for something you do not have. You are activating what already lives inside you.\n\nWalk today knowing that the same Spirit that raised Christ from the dead dwells in you. Let Him direct your words, your steps, and your decisions.",
        "ref": "Ephesians 5:18",
        "verse": "And do not be drunk with wine, in which is dissipation; but be filled with the Spirit."
    },
]

PRAYERS = {
    "church": [
        {"icon": "⛪", "title": "PRAYER FOR UNITY", "prayer": "Father, we cry out for the unity of Your Church. Remove every wall of division, denominational pride, and strife. Let us be one as You and the Father are one, so the world may believe. Knit our hearts together in love — the perfect bond of peace.", "scripture": "📖 John 17:21 · Colossians 3:14"},
        {"icon": "🔥", "title": "PRAYER FOR REVIVAL", "prayer": "Lord, pour out Your Spirit upon Your Church! Awaken every sleeping saint. Restore the backslidden. Let this generation see the greatest move of God the earth has ever witnessed. Let Your glory fill every sanctuary as waters cover the sea.", "scripture": "📖 Habakkuk 2:14 · Acts 2:17"},
        {"icon": "🛡️", "title": "PRAYER AGAINST FALSE DOCTRINE", "prayer": "Holy Spirit, guard Your Church from every spirit of deception, heresy, and compromise. Let the love of truth prevail. May Your people discern between what is holy and profane. Anchor every believer firmly to Your unchanging Word.", "scripture": "📖 2 Timothy 4:3 · John 16:13"},
        {"icon": "🌍", "title": "PRAYER FOR THE GREAT COMMISSION", "prayer": "Father, set Your Church ablaze with missionary zeal. Let every believer walk in their calling to make disciples of all nations. Open doors no man can shut. Fund the harvest. Send labourers into every field. Let the ends of the earth hear of Your salvation.", "scripture": "📖 Matthew 28:19 · Isaiah 22:22"},
        {"icon": "🕊️", "title": "PRAYER FOR THE PERSECUTED CHURCH", "prayer": "God of all comfort, stand with every believer suffering persecution for Your Name today. Strengthen them, sustain them, and let their testimony shake nations. Turn every prison into a prayer meeting and every trial into a testimony of Your faithfulness.", "scripture": "📖 Acts 16:25 · Romans 8:18"},
    ],
    "ministers": [
        {"icon": "✝️", "title": "PRAYER FOR FRESH ANOINTING", "prayer": "Lord Jesus, anoint every pastor, apostle, prophet, evangelist, and teacher with fresh fire. Let their words carry weight in the spirit. May their preaching not be in words of wisdom alone, but in demonstration of the Spirit and of power. Let signs and wonders follow.", "scripture": "📖 1 Corinthians 2:4 · Mark 16:17"},
        {"icon": "💪", "title": "PRAYER FOR STRENGTH", "prayer": "Father, renew the strength of every minister who is weary. In seasons of discouragement, rejection, and fatigue — be their portion. Let them mount up with wings like eagles. Remind them that their labour in You is never in vain. You are their reward.", "scripture": "📖 Isaiah 40:31 · 1 Corinthians 15:58"},
        {"icon": "🧭", "title": "PRAYER FOR INTEGRITY", "prayer": "Holy Spirit, keep every minister in a place of holiness and humility. Guard them from pride, the love of money, and moral failure. Let what they preach publicly match who they are privately. May they finish well and hear 'Well done, good and faithful servant.'", "scripture": "📖 1 Timothy 3:2 · Matthew 25:21"},
        {"icon": "👨‍👩‍👧", "title": "PRAYER FOR MINISTERS' FAMILIES", "prayer": "Lord, protect and bless the families of every minister of the Gospel. Let their homes be sanctuaries of peace and love. Guard their children from the enemy. Strengthen their marriages. Let their households be living testimonies of Your grace, not casualties of ministry.", "scripture": "📖 Joshua 24:15 · Psalm 128:3"},
        {"icon": "🌱", "title": "PRAYER FOR YOUNG MINISTERS", "prayer": "Father, raise up a generation of young ministers who will not compromise. Let no one despise their youth. Give them boldness, wisdom, and mentors who will pour into them. Let them carry the torch of the Gospel into every dark corner of this generation.", "scripture": "📖 1 Timothy 4:12 · Joel 2:28"},
    ],
    "believers": [
        {"icon": "🌿", "title": "PRAYER FOR SPIRITUAL GROWTH", "prayer": "Father, cause every believer to grow in grace and knowledge of Jesus Christ. Stir a hunger for Your Word that cannot be satisfied by earthly things. Root them deep, establish them firm. May they not remain spiritual infants but grow into the full stature of Christ.", "scripture": "📖 Ephesians 4:15 · 2 Peter 3:18"},
        {"icon": "⚔️", "title": "PRAYER FOR VICTORY", "prayer": "In the name of Jesus, we declare victory over every believer today! Break every chain of addiction, fear, shame, and oppression. Let them walk in the authority they have been given — trampling serpents and scorpions, and over all the power of the enemy. Greater is He that is in them!", "scripture": "📖 Luke 10:19 · 1 John 4:4"},
        {"icon": "🕊️", "title": "PRAYER FOR PEACE AND PURPOSE", "prayer": "Lord, let Your peace — which surpasses all understanding — garrison the hearts and minds of every believer. In confusion and uncertainty, be their anchor. Reveal the plans You have for each one. Let them walk fully in their God-given purpose and Kingdom assignment.", "scripture": "📖 Philippians 4:7 · Jeremiah 29:11"},
        {"icon": "💼", "title": "PRAYER FOR BELIEVERS IN THE MARKETPLACE", "prayer": "Father, anoint every believer in their workplace, business, and career. Let them be the head and not the tail. Give them wisdom, favour, and supernatural ideas. Let their light so shine before men in every boardroom, classroom, and marketplace that men may glorify You.", "scripture": "📖 Deuteronomy 28:13 · Matthew 5:16"},
        {"icon": "❤️", "title": "PRAYER FOR PRODIGALS AND BACKSLIDERS", "prayer": "Father of mercies, today we stand in the gap for every prodigal son and daughter. Draw them back with cords of love. Let the memory of Your goodness arrest them. Remove every veil from their eyes. Let today be the day they arise and return to the Father's house.", "scripture": "📖 Luke 15:20 · Jeremiah 31:3"},
    ],
}

def ordinal(n):
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    return f"{n}{['th','st','nd','rd','th','th','th','th','th','th'][n % 10]}"

def date_label():
    now = datetime.utcnow()
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    return f"{ordinal(now.day)} {months[now.month - 1]}", now.day

def send_telegram(text, thread_id):
    payload = json.dumps({
        "chat_id": CHAT_ID,
        "text": text,
        "message_thread_id": thread_id
    }).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read())

@app.route("/devotion", methods=["POST"])
def devotion():
    label, day = date_label()
    d = DECLARATIONS[(day - 1) % 13]
    msg = (
        f"🔥 WE PRAY DAILY · {label}\n\n"
        f"✨ {d['title']}\n\n"
        f"{d['body']}\n\n"
        f"📖 {d['ref']} — \"{d['verse']}\"\n\n"
        f"Declare this over your life today.\n\n"
        f"@kingdomaddicts | t.me/kingdomaddicts\n\n"
        f"#KingdomAddicts #DailyDeclaration #Scripture #WePrayDaily"
    )
    result = send_telegram(msg, DEVOTION_THREAD)
    return jsonify(result)

@app.route("/prayer", methods=["POST"])
def prayer():
    label, day = date_label()
    cats = ["church", "ministers", "believers"]
    cat = cats[day % 3]
    idx = ((day - 1) // 3) % 5
    p = PRAYERS[cat][idx]
    msg = (
        f"🔥 WE PRAY DAILY · {label}\n\n"
        f"{p['icon']} {p['title']}\n\n"
        f"{p['prayer']}\n\n"
        f"{p['scripture']}\n\n"
        f"@kingdomaddicts | t.me/kingdomaddicts\n\n"
        f"#KingdomAddicts #WePrayDaily #DailyPrayer #BodyOfChrist #TheKingdomComes"
    )
    result = send_telegram(msg, PRAYER_THREAD)
    return jsonify(result)

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    result = send_telegram(data["text"], data["message_thread_id"])
    return jsonify(result)

@app.route("/")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
