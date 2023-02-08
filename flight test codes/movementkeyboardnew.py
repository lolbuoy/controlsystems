from pymavlink import mavutil

from sshkeyboard import listen_keyboard


def press(key):
 print(f"'{key}' is pressed")
 control(value=key)

def control(value):
 allowed_keys=['w','a','s','d','q']
 if value in allowed_keys:
  if value == 'w':
   front()
  if value =='s':
   back()
  if value =='a':
   left()
  if value == 'd':
   right()
  if value == 'q':
   the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, 176, 0, 1, 3, 0, 0, 0, 0, 0)
 else:
  print("Enter a valid character")
def front():
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system,
                         the_connection.target_component, 1,3576, 1, 0,0 , 0, 0, 0, 0, 0, 0, 0, 0))
def back():
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system,
                         the_connection.target_component, 1,3576, -1, 0,0 , 0, 0, 0, 0, 0, 0, 0,0)) 
def left():                        
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system,
                         the_connection.target_component, 1,3576, 0, -1,0 , 0, 0, 0, 0, 0, 0, 0, 0))
def right(): 
 the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system,
                         the_connection.target_component, 1,3576, 0, 1,0 , 0, 0, 0, 0, 0, 0, 0, 0))


the_connection = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))
listen_keyboard(on_press=press)

while 1:
   msg = the_connection.recv_match(
        type='LOCAL_POSITION_NED', blocking=True)
   print(msg)



