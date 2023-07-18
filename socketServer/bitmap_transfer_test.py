import matplotlib.pyplot as plt
import zmq
from gabriel_protocol import gabriel_pb2
import openrtist_pb2
import numpy as np
import cv2

address = "tcp://localhost:5559"
COMPRESSION_PARAMS = [cv2.IMWRITE_JPEG_QUALITY, 67]

# zeroMQ socket initialization
context = zmq.Context()
sender = context.socket(zmq.REQ)
sender.connect(address)

# zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"
# sender.setsockopt_string(zmq.SUBSCRIBE, zip_filter)
def grab_frame(sender):
    sender.send_string("0")
    raw_msg = sender.recv()
    input_frame = gabriel_pb2.InputFrame()
    input_frame.ParseFromString(raw_msg)
    np_data = np.frombuffer(input_frame.payloads[0], dtype=np.uint8)
    # orig_img = np_data.reshape((640,480,4))[:,:,(2,1,0)]
    orig_img = np_data.reshape((640,480,4))
    # orig_img = cv2.imdecode(orig_img, cv2.IMREAD_COLOR)
    orig_img = cv2.cvtColor(orig_img, cv2.COLOR_BGRA2BGR)
    # _, jpeg_img = cv2.imencode(".jpg", orig_img, COMPRESSION_PARAMS)
    return orig_img


#create axes
ax1 = plt.subplot(111)

#create image plot
im1 = ax1.imshow(grab_frame(sender), origin='lower')

plt.ion()
while True:
    im1.set_data(grab_frame(sender))
    plt.pause(0.01)


plt.ioff()  # due to infinite loop, this gets never called.
plt.show()

context.destroy()
