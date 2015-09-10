import can

can_interface = 'can0'
can_interface_type = 'socketcan_ctypes'

bus = can.interface.Bus(can_interface, can_interface_type)

while 1:
  message = bus.recv()
