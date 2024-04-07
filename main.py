from flask import Flask,render_template,request,jsonify
from flask_bootstrap import Bootstrap5
from geopy.geocoders import Nominatim
import pandas as pd
from datetime import datetime, timedelta
import math
import asyncio
import aiohttp

app = Flask(__name__)
bootstrap = Bootstrap5(app)
geolocator = Nominatim(user_agent="MyApp")

def get_events_page(events, page_number, page_size):
    # Calculate the total number of pages
    total_pages = math.ceil(len(events) / page_size)

    # Determine the start and end index of entries for the specified page number
    start_index = (page_number - 1) * page_size
    end_index = min(start_index + page_size, len(events))

    # Get events for the specified page
    events_page = events[start_index:end_index]

    # Construct the page JSON
    page_json = {
        "events": events_page,
        "page": page_number,
        "pageSize": page_size,
        "totalEvents": len(events),
        "totalPages": total_pages
    }

    return page_json

def get_all_events(events, page_size):
    total_events = len(events)
    total_pages = math.ceil(total_events / page_size)
    all_events = []
    for page_number in range(1, total_pages + 1):
        events_page = get_events_page(events, page_number, page_size)
        all_events.append(events_page)
    return all_events

async def fetch_weather(session, city, date):
    async with session.get(f"https://gg-backend-assignment.azurewebsites.net/api/Weather?code=KfQnTWHJbg1giyB_Q9Ih3Xu3L9QOBDTuU5zwqVikZepCAzFut3rqsg==&city={city}&date={date}") as response:
        return await response.json()

async def fetch_distance(session, latitude1, longitude1, latitude2, longitude2):
    async with session.get(f"https://gg-backend-assignment.azurewebsites.net/api/Distance?code=IAKvV2EvJa6Z6dEIUqqd7yGAu7IZ8gaH-a0QO6btjRc1AzFu8Y3IcQ==&latitude1={latitude1}&longitude1={longitude1}&latitude2={latitude2}&longitude2={longitude2}") as response:
        return await response.json()

async def process_event(session, event, latitude, longitude):
    weather = await fetch_weather(session, event['city_name'], event['date'])
    distance = await fetch_distance(session, latitude, longitude, event['latitude'], event['longitude'])
    return {
        'event_name': event['event_name'],
        'city_name': event['city_name'],
        'date': event['date'].strftime('%Y-%m-%d'),
        'weather': weather['weather'],
        'distance_km': distance['distance']
    }



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_event',methods=["POST","GET"])
def add_event():
    if len(request.args) > 0:
        try:
            print(request.args)
            event_name = request.args.get('event_name')
            city_name = request.args.get('city_name')
            date = request.args.get('date')
            time = request.args.get('time')
            print(event_name,city_name,date,time)
            location = geolocator.geocode(city_name)
            print(location)
            new_data = {"event_name":[event_name],"city_name":[city_name],"date":[date],"time":[time],"latitude":[location.latitude],"longitude":[location.longitude]}

            file = pd.read_csv("Backend_assignment_gg_dataset - dataset.csv")

            new_df = pd.DataFrame(new_data)

            df = pd.concat([file,new_df],ignore_index=True)

            df.to_csv("Backend_assignment_gg_dataset - dataset.csv",index=False)
            return jsonify({"Success":"Your Event Added Successfully", "event": {
                "event_name": event_name,
                "city_name": city_name,
                "date": date,
                "time": time
    }})
        except Exception as e:
            # Convert the exception to a dictionary
            exception_data = {
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
            # Return the JSON response
            return jsonify(exception_data), 500
    return render_template('addevent.html')




@app.route('/events/find', methods=["POST", "GET"])
async def find_event():
    if len(request.args) > 0:
        try:
            date = request.args.get('date')
            latitude = request.args.get('latitude')
            longitude = request.args.get('longitude')
            file = pd.read_csv('Backend_assignment_gg_dataset - dataset.csv')
            file['date'] = pd.to_datetime(file['date'])
            start_date = datetime.strptime(date, '%Y-%m-%d')

            end_date = start_date + timedelta(days=14)
            filtered_data = file[(file['date'] >= start_date) & (file['date'] < end_date)]
            filtered_data = filtered_data.to_dict(orient='records')
            filtered_data = sorted(filtered_data, key=lambda x: x['date'])

            tasks = []
            async with aiohttp.ClientSession() as session:
                for entry in filtered_data:
                    tasks.append(process_event(session, entry, latitude, longitude))
                results = await asyncio.gather(*tasks)

            page_size = 10
            all_events = get_all_events(results, page_size)
            return jsonify(all_events)
        except Exception as e:
                exception_data = {
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }

                return jsonify(exception_data), 500
    return render_template('find_event.html')


if __name__ == "__main__":
    app.run(debug=True)
