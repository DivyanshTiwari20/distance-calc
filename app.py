from flask import Flask, request, render_template
import requests
from geopy.distance import great_circle

app = Flask(__name__)

api_key = "9ee7f8a559a346bc92149ca16d17bd70"

def get_coordinates(address):
    url = f"https://api.geoapify.com/v1/geocode/search?text={address}&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'features' in data and len(data['features']) > 0:
            first_result = data['features'][0]
            geometry = first_result.get('geometry', {})
            coordinates = geometry.get('coordinates', [])
            if coordinates:
                lng, lat = coordinates
                return lat, lng
    return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    distance = None
    source_address = ""
    destination_address = ""
    error = None

    if request.method == "POST":
        source_address = request.form['source_address']
        destination_address = request.form['destination_address']
        
        source_lat, source_lng = get_coordinates(source_address)
        dest_lat, dest_lng = get_coordinates(destination_address)
        
        if source_lat is not None and dest_lat is not None:
            source_coords = (source_lat, source_lng)
            dest_coords = (dest_lat, dest_lng)
            distance = great_circle(source_coords, dest_coords).kilometers
        else:
            error = "Unable to geocode one or both addresses. Please check and try again."
    
    return render_template('index.html', distance=distance, source_address=source_address, 
                           destination_address=destination_address, error=error)

