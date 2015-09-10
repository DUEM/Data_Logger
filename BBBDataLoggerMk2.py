import can

can_interface = 'can0'
can_interface_type = 'socketcan_ctypes'

bus = can.interface.Bus(can_interface, can_interface_type)

while 1:
  """ message = bus.recv() """
  
  msg = can.Message(arbitration_id=0xc0ffee, data=[2, 0, 0, 1, 3, 1, 4, 1], extended_id=False)
  bus.send(msg)
