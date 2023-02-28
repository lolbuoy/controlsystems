import asyncio
import math
from pymavlink import mavutil

from sshkeyboard import listen_keyboard

gsd = 0.2
connectionString = 'udpin:localhost:14551'

async def press(key):
 print(f"'{key}' is pressed")
 await control(value=key)

async def control(value):
 allowed_keys=['w','a','s','d','q','g','t','1','2','z','x','l']
 if value in allowed_keys:
  if value == 'z':
   await arm()
  if value == 'x':
   await disarm()
  if value == 'g':
   await guided()
  if value == 't':
   await takeoff()
  if value == 'w':
   await front()
  if value == 'l':
   await land()
  if value =='s':
   await back()
  if value =='a':
   await left()
  if value == 'd':
   await right()
  if value == 'q':
   await auto()
 else:
   print("Enter a valid character")

async def arm():
 the_connection = mavutil.mavlink_connection(connectionString)
 the_connection.wait_heartbeat()
 the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

async def disarm():
 the_connection = mavutil.mavlink_connection(connectionString)
 the_connection.wait_heartbeat()
 the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0 0, 0, 0, 0, 0, 0)
async def takeoff():
 the_connection = mavutil.mavlink_connection(connectionString)
 the_connection.wait_heartbeat()
 the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
 the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 10)
 

async def land():
 the_connection = mavutil.mavlink_connection(connectionString)
 the_connection.wait_heartbeat()
 the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 0, 0)
 
def connection():
 the_connection = mavutil.mavlink_connection(connectionString)
# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
 the_connection.wait_heartbeat()
 print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
 the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,176, 0, 1, 4, 0, 0, 0, 0, 0)
 listen_keyboard(on_press=press)
 while 1:
  msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)

async def newlatlon (msg , movementHead):
 heading=(msg.hdg)/100
 lati=math.radians((msg.lat)/10000000)
 longi=math.radians((msg.lon)/10000000)
 na = (6378137*6378137*math.cos(lati)) #numerator
 nb = (6356753*6356753*math.sin(lati)) #numerator
 da = (6378137*math.cos(lati))#denominator
 db = (6356753*math.sin(lati))#denominator 
 rade = math.sqrt(((na*na)+(nb*nb))/((da*da)+(db*db))) #calculates earths radius
 AD = 1/rade #angular distance
 newheading = math.radians (heading + movementHead)
 newlati =math.asin(math.sin(lati)*math.cos(AD) + math.cos(lati)*math.sin(AD)*math.cos(newheading))
 newlongi = longi + math.atan2(math.sin(newheading)*math.sin(AD)*math.cos(lati), math.cos(AD)-math.sin(lati)*math.sin(newlati))
 return math.degrees(newlati*10000000),math.degrees(newlongi*10000000)

async def front():
 the_connection = mavutil.mavlink_connection(connectionString)
 msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
 angle = 0
 value = await newlatlon(msg,angle)
 newlati = value[0]
 longi = value[1]
 print(newlati)
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,the_connection.target_component, 6, 3576, int(newlati), int(longi),10 , 0, 0, 0, 0, 0, 0, 0,0))
async def back():
 the_connection = mavutil.mavlink_connection(connectionString)
 msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
 angle = 180
 value = await newlatlon(msg,angle)
 newlati = value[0]
 longi = value[1]
 print(newlati)
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,the_connection.target_component, 6, 3576, int(newlati), int(longi),10 , 0, 0, 0, 0, 0, 0, 0,0)) 
async def left():
 the_connection = mavutil.mavlink_connection(connectionString)
 msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
 angle = 270
 value = await newlatlon(msg,angle)
 newlati = value[0]
 longi = value[1]
 print(newlati)
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,the_connection.target_component, 6, 3576, int(newlati), int(longi),10 , 0, 0, 0, 0, 0, 0, 0,0))
async def right():
 the_connection = mavutil.mavlink_connection(connectionString)
 msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
 angle = 90
 value = await newlatlon(msg,angle)
 newlati = value[0]
 longi = value[1]
 print(newlati)
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,the_connection.target_component, 6, 3576, int(newlati), int(longi),10 , 0, 0, 0, 0, 0, 0, 0,0)) 
      
asyncio.run(connection())      
