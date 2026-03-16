# IMPORTS: Load requests for API calls and utility modules
import requests
import os
import urllib.parse

# LOCATION RESOLVER: Fetch GPS coordinates or use IP-based fallback if GPS is unavailable
def get_real_location(lat=None, lon=None):
    if lat is not None and lon is not None:
        # User provided actual GPS coordinates, let's reverse geocode it to an address
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
            headers = {"User-Agent": "EmergencyMedicalBot/1.0"}
            r = requests.get(url, headers=headers, timeout=5)
            data = r.json()
            address = data.get("display_name", "Unknown Address")
            loc = f"{lat},{lon}"
            return f"{loc} ({address})", loc
        except Exception:
            # Fallback if reverse geocoding fails
            return f"{lat},{lon} (GPS Location)", f"{lat},{lon}"
            
    # Fallback: IP-based location if no browser GPS was provided
    try:
        r = requests.get("https://ipinfo.io/json", timeout=3)
        data = r.json()
        city = data.get("city", "Unknown City")
        region = data.get("region", "Unknown Region")
        loc = data.get("loc", "0.0,0.0")  # lat,lng
        return f"{loc} ({city}, {region})", loc
    except Exception:
        return "Unknown Location", "0.0,0.0"

# HOSPITAL FINDER: Search for nearby hospitals using Overpass API based on location
def find_nearby_hospitals(lat=None, lon=None):
    location_str, loc = get_real_location(lat, lon)
    hospitals = []
    
    try:
        query_lat, query_lon = loc.split(",")
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        node["amenity"="hospital"](around:5000,{query_lat},{query_lon});
        out 5;
        """
        response = requests.get(overpass_url, params={'data': overpass_query}, timeout=5)
        data = response.json()
        
        for element in data.get('elements', []):
            name = element.get('tags', {}).get('name')
            if name:
                hospitals.append(name)
        
        # fallback if no named hospitals found
        if not hospitals and data.get('elements'):
            hospitals.append("Unnamed Hospital/Clinic found nearby")
            
    except Exception as e:
        print("Error fetching hospitals from Overpass API:", e)
    
    return hospitals[:1], location_str