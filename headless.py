import asyncio
import math
from pymavlink import mavutil

from sshkeyboard import listen_keyboard
#udpin:localhost:14551
connectionString = 'udpin:localhost:14551'
move_forward  = False
move_bak = False
move_left = False 
move_right = False
baud1 = 57600
wpalt = 5
dist = 2
takeoffalti = 5
lati = None 
longi = None
the_connection = mavutil.mavlink_connection(connectionString , baud = 921600)
# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

def press(key):
 print(f"'{key}' is pressed")
 control(value=key)

def control(value):
 global move_forward , move_bak , move_left , move_right 
 allowed_keys=['w','a','s','d','q','g','t','1','2','z','x','l']
 if value in allowed_keys:
  if value == 'z':
   arm()
  elif value == 'x':
   disarm()
  elif value == 'g':
   guided()
  elif value == 't':
   takeoff()
  elif value == 'w':
     move_forward = True
     print("beforekall")
     print(move_forward)
     front()
  elif value == 'l':
   land()
  elif value =='s':
   move_bak = True
   back()
  elif value =='a':
    move_left = True
    left()
  elif value == 'd':
   move_right = True
   right()
  elif value == 'q':
   auto()
  elif value == '1':
   servo1()
 else:
   print("Enter a valid character")

def auto():
	the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,176, 0, 1, 3, 0, 0, 0, 0, 0)
def newlatlon (lat , lon , hdg , movementHead):
 lati=math.radians((lat)/1e7)
 longi=math.radians((lon)/1e7)
 na = (6378137*6378137*math.cos(lati))
 nb = (6356753*6356753*math.sin(lati))
 da = (6378137*math.cos(lati))
 db = (6356753*math.sin(lati))
 rade = math.sqrt(((na*na)+(nb*nb))/((da*da)+(db*db)))
 AD = dist/rade
 sumofangles = (hdg/100) + movementHead
 if sumofangles >= 360 :
     sumofangles = sumofangles - 360
     newheading = math.radians(sumofangles)
 else:
     newheading = math.radians(sumofangles)
 newlati =math.asin(math.sin(lati)*math.cos(AD) + math.cos(lati)*math.sin(AD)*math.cos(newheading))
 newlongi = longi + math.atan2(math.sin(newheading)*math.sin(AD)*math.cos(lati), math.cos(AD)-math.sin(lati)*math.sin(newlati))
 return int(round(math.degrees(newlati*1e7))),int(round(math.degrees(newlongi*1e7))) , sumofangles
def takeoff():
 the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
 the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, takeoffalti)
 

def land():
 the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 0, 0)

def GPS():
    gps = None
    gps = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking = True)
    return gps.lat , gps.lon , gps.hdg

def guided():
  the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,176, 0, 1, 4, 0, 0, 0, 0, 0)
s = GPS()
def front():
 gps = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking = True)
 print(gps)
 global lati
 global longi
 lat1 = lati
 lon1 = longi
 i = 0
 print(lat1 , lon1)
 global move_forward
 print(move_forward)
 lat , lon , hdg = s 
 angle =  0
 if lat1 is None or lon1 is None :
    print(hdg)
    value = newlatlon(lat , lon , hdg ,angle)
    print(value)
    lati = value[0]
    longi = value[1]
    lat1 = lati
    lon1 = longi
 else :
   value = newlatlon(lat1 , lon1 , hdg, angle)
   print(value)
   lati = value[0]
   longi = value[1]
   lat1 = lati
   lon1 = longi
 print(value[2])
 kurrentalti = wpalt
 print(lati ,longi)
 print(kurrentalti)
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,the_connection.target_component, 6, 1024, int(lat1), int(lon1),kurrentalti , 0, 0, 0, 0, 0, 0, 0,0))
 print(i)  
def left():
 global move_left
 global lati
 global longi
 lat1 = lati
 lon1 = longi
 i = 0
 s = GPS()
 print(s)
 print(lat1 , lon1)
 global move_forward
 print(move_forward)
 lat , lon , hdg = s 
 angle =  -90
 if lat1 is None or lon1 is None :
    print(hdg)
    value = newlatlon(lat , lon , hdg ,angle)
    print(value)
    lati = value[0]
    longi = value[1]
    lat1 = lati
    lon1 = longi
 else :
   value = newlatlon(lat1 , lon1 , hdg, angle)
   print(value)
   lati = value[0]
   longi = value[1]
   lat1 = lati
   lon1 = longi
 print(value[2])
 kurrentalti = wpalt
 print(lati , longi)
 print(kurrentalti)
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,the_connection.target_component, 6, 1024, int(lati), int(longi),kurrentalti , 0, 0, 0, 0, 0, 0, 0,0))
 i = 1 
def right():
 global move_right
 global lati
 global longi
 lat1 = lati
 lon1 = longi
 i = 0
 s = GPS()
 print(s)
 print(lat1 , lon1)
 global move_forward
 print(move_forward)
 lat , lon , hdg = s 
 angle =  90
 if lat1 is None or lon1 is None :
    print(hdg)
    value = newlatlon(lat , lon , hdg ,angle)
    print(value)
    lati = value[0]
    longi = value[1]
    lat1 = lati
    lon1 = longi
 else :
   value = newlatlon(lat1 , lon1 , hdg, angle)
   print(value)
   lati = value[0]
   longi = value[1]
   lat1 = lati
   lon1 = longi
 print(value[2])
 kurrentalti = wpalt
 print(lati , longi)
 print(kurrentalti)
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,the_connection.target_component, 6, 1024, int(lati), int(longi),kurrentalti , 0, 0, 0, 0, 0, 0, 0,0))
 i = 1
 i = 0
def back():
 global move_bak
 global lati
 global longi
 lat1 = lati
 lon1 = longi
 i=0
 print(lat1 , lon1)
 global move_forward
 print(move_forward)
 lat , lon , hdg = s 
 angle =  180
 if lat1 is None or lon1 is None :
    print(hdg)
    value = newlatlon(lat , lon , hdg ,angle)
    print(value)
    lati = value[0]
    longi = value[1]
    lat1 = lati
    lon1 = longi
 else :
   value = newlatlon(lat1 , lon1 , hdg, angle)
   print(value)
   lati = value[0]
   longi = value[1]
   lat1 = lati
   lon1 = longi
 print(value[2])
 kurrentalti = wpalt
 print(lati , longi)
 print(kurrentalti)
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,the_connection.target_component, 6, 1024, int(lati), int(longi),kurrentalti , 0, 0, 0, 0, 0, 0, 0,0))
 i = 1

s = GPS()
print(s)
listen_keyboard(on_press=press)
