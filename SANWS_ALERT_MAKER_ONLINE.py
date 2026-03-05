import os
from flask import Flask, request, render_template_string
import requests

# =========================
# CONFIG
# =========================
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Discord webhook from Railway env
PORT = int(os.environ.get("PORT", 5000))     # Railway assigns this automatically
SECRET_KEY = os.environ.get("SECRET_KEY", "12321Nb12321")  # Optional secret key

# =========================
# ALERT VARIANTS (full)
# =========================
alert_variants = {
"Title": [
        "Test Alert",
        "Service Statement",
        "Special Weather Statement",
        "Flood Watch",
        "Tropical Storm Watch",
        "Hurricane Watch",
        "Severe Thunderstorm Watch",
        "Tornado Watch",
        "Severe Thunderstorm Warning",
        "Tornado Warning",
        "Flood Warning",
        "Tropical Storm Warning",
        "Hurricane Warning",
        "PDS Flood Warning",
        "PDS Tornado Watch",
        "PDS Severe Thunderstorm Warning",
        "PDS Tornado Warning",
        "Tornado Emergency",
        "Civil Danger Alert",
        "Civil Danger Emergency"
    ],
    "Severity": [
        "No Severity",
        "Expired",
        "Problematic",
        "Severe",
        "Dangerous",
        "Violent",
        "Deadly",
        "Mass Casualty"
    ],
    "Summary": [
        "Testing Summary",
        "Alert Service Offline.",
        "Radio Service Currently Offline.",
        "Service or Services, Are back online and active!",
        "S A S P C, Service Unavailable.",
        "S A N W S And S A W D M, Radar Service Offline."
        "This alert has expired early!",
        "Dopplar Radar was tracking a Strong to Severe Thunderstorm in the warned area!",
        "Dopplar Radar was tracking a Strong to Severe Thunderstorms capable of causing damage, in the warned area!",
        "Dopplar Radar was tracking a line of Strong to Severe Thunderstorms in the warned area!",
        "Dopplar Radar was tracking a line of Strong to Severe Thunderstorms capable of causing damage, in the warned area!",
        "Dopplar Radar was tracking a line of Strong to Severe Thunderstorms causing damage in the warned area!",
        "Dopplar Radar was tracking a Severe Thunderstorm Causing Damage in the warned area!",
        "Dopplar Radar was tracking a Strong to Severe Thunderstorm capable of producing a tornado in the warned area!",
        "Dopplar Radar was tracking a Strong to Severe Thunderstorm producing a damagaing tornado in the warned area!",
        "Dopplar Radar confirmed a deadly tornado in the warned area!",
        "Multiple severe storms expected from this watch!",
        "Multiple severe storms capable of producing tornadoes, expected from this watch!",
        "Multiple Tornadoes expected from this watch!",
        "Multiple Strong to Violent Tornadoes Expected from this watch!",
        "This tropical storm could produce heavy wind, heavy rain, and or a tornado, in the warned area!",
        "This hurricane could produce life-threatening wind, major flooding, and a few tornadoes, in the warned area!",
        "These storms or cluster of storms could cause flooding in the warned area!",
        "These storms or cluster of storms will cause flooding in the warned area!",
        "These storms or cluster of storms will cause life-threatening flooding in the warned area!",
        "A mass casualty event has occoured, we are sorry. If you are trapped or injurged, do not attempt to fall asleep. call for help. help is on the way.",
    ],
    "Hazard": [
        "No Hazards",
        "30 MPH Wind Gust",
        "45 MPH Wind Gust",
        "60 MPH Wind Gust",
        "70 MPH Wind Gust",
        "80 MPH Wind Gust",
        "90 MPH Wind Gust",
        "30 MPH Wind Gust Quarter Inch Sized Hail",
        "30 MPH Wind Gust Half Inch Sized Hail",
        "30 MPH Wind Gust Inch Sized Hail",
        "30 MPH Wind Gust Inch and a Half Sized Hail",
        "30 MPH Wind Gust Two Inch Sized Hail",
        "30 MPH Wind Gust Two Inch and a Half Sized Hail",
        "45 MPH Wind Gust Quarter Inch Sized Hail",
        "45 MPH Wind Gust Half Inch Sized Hail",
        "45 MPH Wind Gust Inch Sized Hail",
        "45 MPH Wind Gust Inch and a Half Sized Hail",
        "45 MPH Wind Gust Two Inch Sized Hail",
        "45 MPH Wind Gust Two Inch and a Half Sized Hail",
        "60 MPH Wind Gust Quarter Inch Sized Hail",
        "60 MPH Wind Gust Half Inch Sized Hail",
        "60 MPH Wind Gust Inch Sized Hail",
        "60 MPH Wind Gust Inch and a Half Sized Hail",
        "60 MPH Wind Gust Two Inch Sized Hail",
        "60 MPH Wind Gust Two Inch and a Half Sized Hail",
        "70 MPH Wind Gust Quarter Inch Sized Hail",
        "70 MPH Wind Gust Half Inch Sized Hail",
        "70 MPH Wind Gust Inch Sized Hail",
        "70 MPH Wind Gust Inch and a Half Sized Hail",
        "70 MPH Wind Gust Two Inch Sized Hail",
        "70 MPH Wind Gust Two Inch and a Half Sized Hail",
        "80 MPH Wind Gust Quarter Inch Sized Hail",
        "80 MPH Wind Gust Half Inch Sized Hail",
        "80 MPH Wind Gust Inch Sized Hail",
        "80 MPH Wind Gust Inch and a Half Sized Hail",
        "80 MPH Wind Gust Two Inch Sized Hail",
        "80 MPH Wind Gust Two Inch and a Half Sized Hail",
        "90 MPH Wind Gust Quarter Inch Sized Hail",
        "90 MPH Wind Gust Half Inch Sized Hail",
        "90 MPH Wind Gust Inch Sized Hail",
        "90 MPH Wind Gust Inch and a Half Sized Hail",
        "90 MPH Wind Gust Two Inch Sized Hail",
        "90 MPH Wind Gust Two Inch and a Half Sized Hail",
        "Quarter Inch Sized Hail",
        "Half Inch Sized Hail",
        "Inch Sized Hail",
        "Inch and a Half Sized Hail",
        "Two Inch Sized Hail",
        "Two Inch and a Half Sized Hail",
        "Radar Indincated Rotation",
        "Radar Indincated Tornado",
        "Radar Confirmed Rotation",
        "Radar Confirmed Tornado",
        "Radar Confirmed Strong Tornado",
        "Radar Confirmed Deadly Tornado",
        "Spotters Confirmed Tornado",
        "Spotters Confirmed Violent Tornado",
        "Spotters Confirmed Deadly Tornado",
        "Media Sources Confirmed Tornado",
        "Media Sources Confirmed Violent Tornado",
        "Media Sources Confirmed Deadly Tornado",
        "Multiple severe storms expected from this watch!",
        "Multiple severe storms capable of producing tornadoes, expected from this watch!",
        "Multiple Tornadoes expected from this watch!",
        "Multiple Strong to Violent Tornadoes Expected from this watch!",
        "Tropical storm to cause damage to life and property in the warned area!",
        "Hurricane to cause damage to life and property in the warned area!",
        "Flooding to cause damage to life and property in the warned area!",
        "Flooding to cause life-threatening damage to life and property in the warned area!",
    ],
    "Direction": [
        "No Direction",
        "North",
        "South",
        "East",
        "West",
        "North East",
        "South East",
        "North West",
        "South West"
    ],
    "Expires": [
        "Until Further Notice",
        "1",
        "15",
        "30",
        "45",
        "60",
        "75",
        "90",
        "120",
        "480",
        "720",
        "960",
        "1440",
        "2160",
    ],
    "Extra": [
        "This is a mass casualty event, we are sorry for any losses you may be reciving. A civil danger emergency is in effect.",
        "This is a Particularly Dangerous Situation, This watch should not be taken lightly!",
        "This is a Particularly Dangerous Situation, This watch should not be taken lightly! Remember a watch means conditions are favourable for severe weather and or tornadoes.",
        "Remember a watch means conditions are favourable for severe weather and or tornadoes.",
        "THIS IS NOT A TEST TAKE COVER NOW! If you see or hear a tornado go at once into a basement or sturdy most interior place in your home, and report the tornado to the National Weather Service, Law Enforcement, and NDC Discord, if safe to do so.",
        "YOU ARE IN A LIFE-THREATENING SITUATION! Mobile Homes will be damaged or destroyed. Remember this is a Particularly Dangerous and Life-Threatening Situation. If you see or hear a tornado go at once into a basement or sturdy most interior place in your home, and report the tornado to the National Weather Service, Law Enforcement, and NDC Discord, if safe to do so.",
        "YOU ARE IN A LIFE-THREATENING SITUATION! Mobile Homes will be destroyed. Poorly built homes will be destroyed. Cars will be lofted. Remember this is a Particularly Dangerous and Life-Threatening Emergency Situation. If you see or hear a tornado go at once into a basement or sturdy most interior place in your home, and report the tornado to the National Weather Service, Law Enforcement, and NDC Discord, if safe to do so.",
        "Damage to vegitation, windshields, and shingles may occour.",
        "Damage to vegitation, windshields, and shingles may occour. Remain Alert for a Possible Tornado from this storm!",
        "The storm that prompted this warning has weakedned below severe limits. Therefore this warning is cancelled.",
        "This Alert and previous Service Alerts Have been Cancelled.",
        "No extra information at this time.",
        "Extra Testing Summary."
    ]
}

# =========================
# GENERATE HTML
# =========================
def generate_html():
    html_dropdowns = ""
    html_dropdowns += "<label>Area</label><br>"
    html_dropdowns += "<input type='text' name='area' placeholder='Enter area...' style='width:90%; padding:8px; margin:5px; font-size:16px;'><br><br>"

    for category, options in alert_variants.items():
        html_dropdowns += f"<label>{category}</label><br>"
        html_dropdowns += f"<select name='{category.lower()}'>"
        for o in options:
            html_dropdowns += f"<option>{o}</option>"
        html_dropdowns += "</select><br><br>"

    html_dropdowns += f"<input type='hidden' name='key' value='{SECRET_KEY}'>"

    html = f"""
<html>
<head>
<title>NDC Alert Creator</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {{background:#111; color:white; font-family:Arial; text-align:center;}}
select, input {{width:90%; padding:8px; margin:5px; font-size:16px;}}
button {{background:red; color:white; border:none; padding:10px; font-size:18px; cursor:pointer;}}
button:hover {{background:#ff3333;}}
form {{max-width:600px; margin:auto;}}
</style>
</head>
<body>
<h1>NDC Alert Creator</h1>
<form action="/send" method="post">
{html_dropdowns}
<button type="submit">SEND ALERT</button>
</form>
</body>
</html>
"""
    return html

HTML_PAGE = generate_html()

# =========================
# FLASK SERVER
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/send", methods=["POST"])
def send_alert():
    key = request.form.get("key")
    if key != SECRET_KEY:
        return "❌ Unauthorized", 401

    fields = ["title","severity","summary","hazard","area","direction","expires","extra"]
    data = {f: request.form.get(f) for f in fields}

    message = f"""[ALERT]
Title: {data['title']}
Severity: {data['severity']}
Summary: {data['summary']}
Hazard: {data['hazard']}
Area: {data['area']}
Direction: {data['direction']}
Expires: {data['expires']}
Extra: {data['extra']}
"""
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        return f"❌ Failed to send alert: {e}"

    return "✅ Alert sent successfully!"

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    print("\n✅ NDC Alert Creator Running on Railway!\n")
    app.run(host="0.0.0.0", port=PORT, debug=False)