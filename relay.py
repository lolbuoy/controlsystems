from pymavlink import mavutil

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('/dev/ttyUSB0' , baud=115200)

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))

def do_relay(pin)
      the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                           181, 0, , 1, 0, 0, 0, 0, 0)

      msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
      print(msg)
