from pymavlink import mavutil
import math

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('udpin:localhost:14551')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %      (the_connection.target_system, the_connection.target_component))
msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
heading=(msg.hdg)/100
lati=(msg.lat)/10000000
longi=(msg.lon)/10000000
na = (6378.137*6378.137*math.cos(lati))
nb = (6356.753*6356.753*math.sin(lati))
da = (6378.137*math.cos(lati))
db = (6356.753*math.sin(lati))
rade = math.sqrt(((na*na)+(nb*nb))/((da*da)+(db*db)))
AD = 1/rade
newheading = heading - 90
newlati =lati + math.asin(math.sin(lati)*math.cos(AD) + math.cos(lati)*math.sin(AD)*math.cos(newheading))
print(newlati,newheading)




