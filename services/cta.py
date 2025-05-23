import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
CTA_API_KEY = os.getenv("CTA_TRAIN_API_KEY")

# --- Station Map ---
STATION_OPTIONS = {
    "Adams/Wabash": "40540",
    "Clark/Lake": "40380",
    "Roosevelt": "41320",
    "Fullerton": "41220",
    "Belmont": "41330",
    "Ashland (Green/Pink)": "40170",
    "Harold Washington Library": "40850",
    "Ashland/Lake": "40010",
    "Cermak-McCormick Place": "41690",
    "Midway (Orange)": "40930",
    "Kimball (Brown)": "41290",
    "54th/Cermak (Pink)": "40580",
    "O'Hare (Blue)": "40890",
    "Howard (Red/Purple/Yellow)": "40900",
    "95th/Dan Ryan (Red)": "40450"
}

LINE_COLORS = {
    "Red": "#C0392B",       # Medium-dark red
    "Blue": "#3B5998",      # Medium navy-blue
    "Brn": "#6E4B3A",       # Medium-dark earthy brown
    "G": "#6BAE75",         # Muted leafy green
    "Org": "#E08E45",       # Soft, light but grounded orange
    "Pink": "#D28A94",         # Medium-light rose pink
    "Purple": "#5E4A82",    # Muted medium-dark purple
    "Yellow": "#D6B84B"     # Soft golden yellow
}

# --- Get Train Arrivals ---
def get_train_arrivals(stop_id, line_code=None):
    url = "https://lapi.transitchicago.com/api/1.0/ttarrivals.aspx"
    params = {
        "key": CTA_API_KEY,
        "mapid": stop_id,
        "max": 10,
        "outputType": "JSON"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "ctatt" not in data or "eta" not in data["ctatt"]:
            return [{"destination": "No trains found", "arrival_time": "N/A", "line": "—"}]

        arrivals = []
        for train in data["ctatt"]["eta"]:
            if line_code is None or train.get("rt") == line_code:
                arrival_time_raw = train.get("arrT")
                arrival_time = (
                    datetime.strptime(arrival_time_raw, "%Y-%m-%dT%H:%M:%S").strftime("%I:%M %p")
                    if arrival_time_raw else "Unknown"
                )
                arrivals.append({
                    "destination": train.get("destNm", "Unknown"),
                    "arrival_time": arrival_time,
                    "line": train.get("rt", "Unknown")
                })

        return arrivals if arrivals else [{"destination": "No scheduled trains", "arrival_time": "—", "line": "—"}]

    except Exception as e:
        return [{"destination": "Error", "arrival_time": str(e), "line": "—"}]

#Update the function to handle errors more gracefully