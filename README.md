# Event Finder API
The Event Finder API is a Flask-based web service designed to help users find events based on their location and specified date. This API provides two endpoints: /add_event for adding new events and /events/find for finding events based on user-provided latitude, longitude, and date.

## Features
**Add Event**: Allows users to add new events to the system by providing event details such as name, city, date, and time. The /add_event endpoint accepts GET requests for adding events.

**Find Events**: Enables users to search for events happening within the next 14 days based on their location and specified date. The /events/find endpoint accepts GET requests for finding events.

## Installation
1. Clone the repository to your local machine:

#### git clone https://github.com/kartikG-86/Event_assignment.git

2. Install the required dependencies using pip:

pip install -r requirements.txt

## Why Python and CSV?
Python was chosen as the primary technology stack for this project due to its simplicity, versatility, and ease of use in handling data processing tasks. Here's why Python was selected:

**Data Processing**: Python provides robust libraries and tools for handling various data processing tasks efficiently. With libraries like Pandas and NumPy, managing and manipulating data, especially in CSV format, becomes straightforward.

**Ease of Use**: Python's syntax is clean and readable, making it easy for developers to understand and maintain code. Additionally, Python's extensive standard library and rich ecosystem of third-party packages offer solutions for a wide range of development needs.

**Community Support**: Python has a large and active community of developers, which means abundant resources, tutorials, and community support are readily available. This makes it easier to troubleshoot issues and find solutions to problems encountered during development.

As for the choice of using a CSV file instead of a traditional database:

**Simplicity**: For this project, a CSV file was chosen as the data storage solution due to its simplicity and ease of implementation. Unlike setting up and managing a database server, working with CSV files requires minimal configuration and overhead.

**Portability**: CSV files are platform-independent and can be easily shared and transferred between different systems. This makes it convenient for storing and exchanging event data without worrying about compatibility issues.

**Low Overhead**: Since the project involves a relatively small-scale application and does not require complex querying or transactional capabilities, using a CSV file provides a lightweight and low-overhead solution for storing event data.

By leveraging Python and CSV files, the project achieves a balance between simplicity, efficiency, and ease of use, making it suitable for rapid development and deployment of the Event Finder API.

## Usage
Start the Flask server:

#### python main.py

Once the server is running, you can access the API endpoints using tools like Postman or by submitting requests via the provided web interface.

## API Endpoints

### /add_event
####  Request Format:

- **Method**: GET
- **Description**: Adds a new event to the system.
- **Parameters**:
  * `event_name` (string, required): Name of the event.
  * `city_name` (string, required): Name of the city where the event is happening.
  * `date` (string, required): Date of the event in the format "YYYY-MM-DD".
  * `time` (string, required): Time of the event in the format "HH:MM:SS".

#### Response Format:

#### Success Response:

- **Code**: 200 OK
- **Content**: JSON object with details of the added event.

````
{
    "Success": "Your Event Added Successfully",
    "event": {
        "event_name": "Birthday Party",
        "city_name": "New York",
        "date": "2024-12-31",
        "time": "18:00:00"
    }
}
````
#### Error Response:

* **Code**: 400 Bad Request
* **Content**: JSON object with error message.

````
{
    "error_message": "Depend on Type of error",
    "error_type" : "Depend on Particular Error type"
}
 ````
## /events/find
### Request Format:
* **Method**: GET
* **Description**: Finds events happening within the next 14 days based on user-provided location and date.
* **Parameters**:
  * `latitude` (float, required): Latitude of the user's location.
  * `longitude` (float, required): Longitude of the user's location.
  * `date` (string, required): Date of the event in the format "YYYY-MM-DD".

### Response Format:
#### Success Response:

* **Code**: 200 OK
* **Content**: JSON object with details of the found events.
````
[
    {
        "events": [10 items],
        "page": 1,
        "pageSize": 10,
        "totalEvents": 39,
        "totalPages": 4
    },
    {
        "events": [10 items],
        "page": 2,
        "pageSize": 10,
        "totalEvents": 39,
        "totalPages": 4
    },
]
````
### Error Response:

* **Code**: 400 Bad Request
* **Content**: JSON object with error message.
````
{
    "error_message": "Depend on Type of error",
    "error_type" : "Depend on Particular Error type"
}
````
## Web Interface
The project includes a simple web interface where users can interact with the API endpoints by submitting details via a form. The web interface can be accessed by navigating to http://localhost:5000 in a web browser while the Flask server is running.


