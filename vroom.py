import pymysql
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Database Configuration
DATABASE_CONFIG = {
    'server': 'sql5.freesqldatabase.com',  # Host from FreeSQLDatabase.com
    'port': 3306,                          # MySQL default port
    'database': 'sql5753696',              # Replace with your database name
    'username': 'sql5753696',              # Replace with your username
    'password': 'eIrM9YvUzm',              # Replace with your password
}

# Function to connect to the database
def get_connection():
    try:
        conn = pymysql.connect(
            host=DATABASE_CONFIG['server'],
            port=DATABASE_CONFIG['port'],
            user=DATABASE_CONFIG['username'],
            password=DATABASE_CONFIG['password'],
            database=DATABASE_CONFIG['database']
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")


# Pydantic model for trip details (excluding driver data)
class TripDetails(BaseModel):
    Distance: float
    Duration: str
    From: str
    To: str
    Money: float
    RiderId: str
    RiderName: str
    RiderLocationLatitude: float
    RiderLocationLongitude: float
    RiderDestinationLatitude: float
    RiderDestinationLongitude: float


# Endpoint to insert trip details with additional driver data
@app.get("/test_connection")
async def test_connection():
    try:
        conn = get_connection()
        conn.close()
        return {"message": "Database connected successfully!"}
    except Exception as e:
        return {"error": str(e)}
@app.post("/insertTripDetails")
async def insert_trip_details(
    trip: TripDetails,
    DriverId: str,
    DriverName: str,
    DriverLocationLatitude: float,
    DriverLocationLongitude: float
):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO trips (
            Distance, Duration, `From`, `To`, Money, RiderId, DriverId, 
            RiderName, DriverName, 
            RiderLocationLatitude, RiderLocationLongitude, 
            RiderDestinationLatitude, RiderDestinationLongitude,
            DriverLocationLatitude, DriverLocationLongitude
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            trip.Distance, trip.Duration, trip.From, trip.To, trip.Money,
            trip.Id, DriverId, trip.Name, DriverName,
            trip.RiderLocationLatitude, trip.RiderLocationLongitude,
            trip.RiderDestinationLatitude, trip.RiderDestinationLongitude,
            DriverLocationLatitude, DriverLocationLongitude
        ))
        conn.commit()
        conn.close()
        return {"message": "Trip details inserted successfully!"}
    except Exception as e:
        return {"error": str(e)}
