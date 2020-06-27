# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from polled_camera/GetPolledImageRequest.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import genpy
import sensor_msgs.msg

class GetPolledImageRequest(genpy.Message):
  _md5sum = "c77ed43e530fd48e9e7a2a93845e154c"
  _type = "polled_camera/GetPolledImageRequest"
  _has_header = False  # flag to mark the presence of a Header object
  _full_text = """# Namespace to publish response topics in. A polled camera driver node
# should publish:
#   <response_namespace>/image_raw
#   <response_namespace>/camera_info
string response_namespace

# Timeout for attempting to capture data from the device. This does not
# include latency from ROS communication, post-processing of raw camera
# data, etc. A zero duration indicates no time limit.
duration timeout

# Binning settings, if supported by the camera.
uint32 binning_x
uint32 binning_y

# Region of interest, if supported by the camera.
sensor_msgs/RegionOfInterest roi

================================================================================
MSG: sensor_msgs/RegionOfInterest
# This message is used to specify a region of interest within an image.
#
# When used to specify the ROI setting of the camera when the image was
# taken, the height and width fields should either match the height and
# width fields for the associated image; or height = width = 0
# indicates that the full resolution image was captured.

uint32 x_offset  # Leftmost pixel of the ROI
                 # (0 if the ROI includes the left edge of the image)
uint32 y_offset  # Topmost pixel of the ROI
                 # (0 if the ROI includes the top edge of the image)
uint32 height    # Height of ROI
uint32 width     # Width of ROI

# True if a distinct rectified ROI should be calculated from the "raw"
# ROI in this message. Typically this should be False if the full image
# is captured (ROI not used), and True if a subwindow is captured (ROI
# used).
bool do_rectify
"""
  __slots__ = ['response_namespace','timeout','binning_x','binning_y','roi']
  _slot_types = ['string','duration','uint32','uint32','sensor_msgs/RegionOfInterest']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       response_namespace,timeout,binning_x,binning_y,roi

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(GetPolledImageRequest, self).__init__(*args, **kwds)
      # message fields cannot be None, assign default values for those that are
      if self.response_namespace is None:
        self.response_namespace = ''
      if self.timeout is None:
        self.timeout = genpy.Duration()
      if self.binning_x is None:
        self.binning_x = 0
      if self.binning_y is None:
        self.binning_y = 0
      if self.roi is None:
        self.roi = sensor_msgs.msg.RegionOfInterest()
    else:
      self.response_namespace = ''
      self.timeout = genpy.Duration()
      self.binning_x = 0
      self.binning_y = 0
      self.roi = sensor_msgs.msg.RegionOfInterest()

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self.response_namespace
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_get_struct_2i6IB().pack(_x.timeout.secs, _x.timeout.nsecs, _x.binning_x, _x.binning_y, _x.roi.x_offset, _x.roi.y_offset, _x.roi.height, _x.roi.width, _x.roi.do_rectify))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      if self.timeout is None:
        self.timeout = genpy.Duration()
      if self.roi is None:
        self.roi = sensor_msgs.msg.RegionOfInterest()
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.response_namespace = str[start:end].decode('utf-8')
      else:
        self.response_namespace = str[start:end]
      _x = self
      start = end
      end += 33
      (_x.timeout.secs, _x.timeout.nsecs, _x.binning_x, _x.binning_y, _x.roi.x_offset, _x.roi.y_offset, _x.roi.height, _x.roi.width, _x.roi.do_rectify,) = _get_struct_2i6IB().unpack(str[start:end])
      self.roi.do_rectify = bool(self.roi.do_rectify)
      self.timeout.canon()
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self.response_namespace
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_get_struct_2i6IB().pack(_x.timeout.secs, _x.timeout.nsecs, _x.binning_x, _x.binning_y, _x.roi.x_offset, _x.roi.y_offset, _x.roi.height, _x.roi.width, _x.roi.do_rectify))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      if self.timeout is None:
        self.timeout = genpy.Duration()
      if self.roi is None:
        self.roi = sensor_msgs.msg.RegionOfInterest()
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.response_namespace = str[start:end].decode('utf-8')
      else:
        self.response_namespace = str[start:end]
      _x = self
      start = end
      end += 33
      (_x.timeout.secs, _x.timeout.nsecs, _x.binning_x, _x.binning_y, _x.roi.x_offset, _x.roi.y_offset, _x.roi.height, _x.roi.width, _x.roi.do_rectify,) = _get_struct_2i6IB().unpack(str[start:end])
      self.roi.do_rectify = bool(self.roi.do_rectify)
      self.timeout.canon()
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_2i6IB = None
def _get_struct_2i6IB():
    global _struct_2i6IB
    if _struct_2i6IB is None:
        _struct_2i6IB = struct.Struct("<2i6IB")
    return _struct_2i6IB
# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from polled_camera/GetPolledImageResponse.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import genpy

class GetPolledImageResponse(genpy.Message):
  _md5sum = "dbf1f851bc511800e6129ccd5a3542ab"
  _type = "polled_camera/GetPolledImageResponse"
  _has_header = False  # flag to mark the presence of a Header object
  _full_text = """bool success          # Could the image be captured?
string status_message # Error message in case of failure
time stamp            # Timestamp of the captured image. Can be matched
                      # against incoming sensor_msgs/Image header.

"""
  __slots__ = ['success','status_message','stamp']
  _slot_types = ['bool','string','time']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       success,status_message,stamp

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(GetPolledImageResponse, self).__init__(*args, **kwds)
      # message fields cannot be None, assign default values for those that are
      if self.success is None:
        self.success = False
      if self.status_message is None:
        self.status_message = ''
      if self.stamp is None:
        self.stamp = genpy.Time()
    else:
      self.success = False
      self.status_message = ''
      self.stamp = genpy.Time()

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self.success
      buff.write(_get_struct_B().pack(_x))
      _x = self.status_message
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_get_struct_2I().pack(_x.stamp.secs, _x.stamp.nsecs))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      if self.stamp is None:
        self.stamp = genpy.Time()
      end = 0
      start = end
      end += 1
      (self.success,) = _get_struct_B().unpack(str[start:end])
      self.success = bool(self.success)
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.status_message = str[start:end].decode('utf-8')
      else:
        self.status_message = str[start:end]
      _x = self
      start = end
      end += 8
      (_x.stamp.secs, _x.stamp.nsecs,) = _get_struct_2I().unpack(str[start:end])
      self.stamp.canon()
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self.success
      buff.write(_get_struct_B().pack(_x))
      _x = self.status_message
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_get_struct_2I().pack(_x.stamp.secs, _x.stamp.nsecs))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      if self.stamp is None:
        self.stamp = genpy.Time()
      end = 0
      start = end
      end += 1
      (self.success,) = _get_struct_B().unpack(str[start:end])
      self.success = bool(self.success)
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.status_message = str[start:end].decode('utf-8')
      else:
        self.status_message = str[start:end]
      _x = self
      start = end
      end += 8
      (_x.stamp.secs, _x.stamp.nsecs,) = _get_struct_2I().unpack(str[start:end])
      self.stamp.canon()
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_2I = None
def _get_struct_2I():
    global _struct_2I
    if _struct_2I is None:
        _struct_2I = struct.Struct("<2I")
    return _struct_2I
_struct_B = None
def _get_struct_B():
    global _struct_B
    if _struct_B is None:
        _struct_B = struct.Struct("<B")
    return _struct_B
class GetPolledImage(object):
  _type          = 'polled_camera/GetPolledImage'
  _md5sum = '1f3fb0d09d6e1c72d4a7eeb9822d9030'
  _request_class  = GetPolledImageRequest
  _response_class = GetPolledImageResponse
