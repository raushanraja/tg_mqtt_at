import uuid

# MQTT Packet Types
RESERVED = 0
CONNECT = 0x10
CONNACK = 0x20
PUBLISH = 0x30
PUBACK = 0x40
PUBREC = 0x50
PUBREL = 0x60
PUBCOMP = 0x70
SUBSCRIBE = 0x82
SUBACK = 0x90
UNSUBSCRIBE = 0xA0
UNSUBACK = 0xB0
PINGREQ = 0xC0
PINGRESP = 0xD0
DISCONNECT = 0xE0

# MQTT QoS Levels
AT_MOST_ONCE = 0
AT_LEAST_ONCE = 1
EXACTLY_ONCE = 2

# MQTT Connect Return Codes
CONNECTION_ACCEPTED = 0
UNACCEPTABLE_PROTOCOL_VERSION = 1
IDENTIFIER_REJECTED = 2
SERVER_UNAVAILABLE = 3
BAD_USERNAME_OR_PASSWORD = 4
NOT_AUTHORIZED = 5

# MQTT Connect Flags
USERNAME_FLAG = 0x80
PASSWORD_FLAG = 0x40
WILL_RETAIN_FLAG = 0x20
WILL_QOS_FLAG = 0x18
WILL_QOS_FLAG_SHIFT = 3
WILL_FLAG = 0x04
CLEAN_SESSION_FLAG = 0x02

# MQTT Subscribe Return Codes
SUBACK_FAILURE = 0x80

# MQTT Unsubscribe Return Codes
UNSUBACK_FAILURE = 0x80

# MQTT Disconnect Reason Codes
NORMAL_DISCONNECTION = 0
DISCONNECT_WITH_WILL_MESSAGE = 4

# MQTT Publish Reason Codes
SUCCESS = 0
NO_MATCHING_SUBSCRIBERS = 16
NO_SUBSCRIPTION_EXISTED = 17
PAYLOAD_FORMAT_INVALID = 18
# ... and many more

# MQTT Properties
PAYLOAD_FORMAT_INDICATOR = 0x01
MESSAGE_EXPIRY_INTERVAL = 0x02
CONTENT_TYPE = 0x03
RESPONSE_TOPIC = 0x08
CORRELATION_DATA = 0x09
SUBSCRIPTION_IDENTIFIER = 0x0B
SESSION_EXPIRY_INTERVAL = 0x11
ASSIGNED_CLIENT_IDENTIFIER = 0x12
SERVER_KEEP_ALIVE = 0x13
AUTHENTICATION_METHOD = 0x15
AUTHENTICATION_DATA = 0x16
REQUEST_PROBLEM_INFORMATION = 0x17
WILL_DELAY_INTERVAL = 0x18
REQUEST_RESPONSE_INFORMATION = 0x19
RESPONSE_INFORMATION = 0x1A
SERVER_REFERENCE = 0x1C
REASON_STRING = 0x1F
RECEIVE_MAXIMUM = 0x21
TOPIC_ALIAS_MAXIMUM = 0x22
TOPIC_ALIAS = 0x23
MAXIMUM_QOS = 0x24
RETAIN_AVAILABLE = 0x25
USER_PROPERTY = 0x26
MAXIMUM_PACKET_SIZE = 0x27
WILDCARD_SUBSCRIPTION_AVAILABLE = 0x28
SUBSCRIPTION_IDENTIFIER_AVAILABLE = 0x29
SHARED_SUBSCRIPTION_AVAILABLE = 0x2A

# MQTT Reason Strings
REASON_STRINGS = {
    SUCCESS: "Success",
    NO_MATCHING_SUBSCRIBERS: "No matching subscribers",
    NO_SUBSCRIPTION_EXISTED: "No subscription existed",
    PAYLOAD_FORMAT_INVALID: "Payload format invalid",
    # UNSPECIFIED_ERROR: "Unspecified error",
    # IMPLEMENTATION_SPECIFIC_ERROR: "Implementation specific error",
    NOT_AUTHORIZED: "Not authorized",
    # TOPIC_NAME_INVALID: "Topic name invalid",
    # PACKET_IDENTIFIER_IN_USE: "Packet identifier in use",
    # QUOTA_EXCEEDED: "Quota exceeded",
    PAYLOAD_FORMAT_INVALID: "Payload format invalid",
    # RETAIN_NOT_SUPPORTED: "Retain not supported",
    # QOS_NOT_SUPPORTED: "QoS not supported",
}

# MQTT Return Codes
RETURN_CODES = {
    CONNECTION_ACCEPTED: "Connection accepted",
    UNACCEPTABLE_PROTOCOL_VERSION: "Unacceptable protocol version",
    IDENTIFIER_REJECTED: "Identifier rejected",
    SERVER_UNAVAILABLE: "Server unavailable",
    BAD_USERNAME_OR_PASSWORD: "Bad username or password",
    NOT_AUTHORIZED: "Not authorized",
}


def connect_flags_to_str(flags: hex) -> str:
    flags = int(flags, 16)
    s = ""
    if flags & USERNAME_FLAG:
        s += "USERNAME "
    if flags & PASSWORD_FLAG:
        s += "PASSWORD "
    if flags & WILL_RETAIN_FLAG:
        s += "WILL_RETAIN "
    if flags & WILL_FLAG:
        s += "WILL "
    if flags & CLEAN_SESSION_FLAG:
        s += "CLEAN_SESSION "
    return s


# def control_field_to_str(control_field: hex) -> str:
#     s = ""
#     if control_field & 0xF0 == CONNECT:
#         s += "CONNECT"
#     elif control_field & 0xF0 == CONNACK:
#         s += "CONNACK"
#     elif control_field & 0xF0 == PUBLISH:
#         s += "PUBLISH"
#     elif control_field & 0xF0 == PUBACK:
#         s += "PUBACK"
#     elif control_field & 0xF0 == PUBREC:
#         s += "PUBREC"
#     elif control_field & 0xF0 == PUBREL:
#         s += "PUBREL"
#     elif control_field & 0xF0 == PUBCOMP:
#         s += "PUBCOMP"
#     elif control_field & 0xF0 == SUBSCRIBE:
#         s += "SUBSCRIBE"
#     elif control_field & 0xF0 == SUBACK:
#         s += "SUBACK"
#     elif control_field & 0xF0 == UNSUBSCRIBE:
#         s += "UNSUBSCRIBE"
#     elif control_field & 0xF0 == UNSUBACK:
#         s += "UNSUBACK"
#     elif control_field & 0xF0 == PINGREQ:
#         s += "PINGREQ"
#     elif control_field & 0xF0 == PINGRESP:
#         s += "PINGRESP"
#     elif control_field & 0xF0 == DISCONNECT:
#         s += "DISCONNECT"
#     else:
#         s += "RESERVED"
#     return s

def control_field_to_str(control_field: int) -> str:
    control_field_mapping = {
        0x10: "CONNECT",
        0x20: "CONNACK",
        0x30: "PUBLISH",
        0x40: "PUBACK",
        0x50: "PUBREC",
        0x60: "PUBREL",
        0x70: "PUBCOMP",
        0x80: "SUBSCRIBE",
        0x90: "SUBACK",
        0xA0: "UNSUBSCRIBE",
        0xB0: "UNSUBACK",
        0xC0: "PINGREQ",
        0xD0: "PINGRESP",
        0xE0: "DISCONNECT",
    }

    control_type = control_field & 0xF0  # Extract the high 4 bits

    if control_type in control_field_mapping:
        return control_field_mapping[control_type]
    else:
        return "RESERVED"

# def control_field_to_str(control_field: hex) -> str:
#     s = ""
#     if control_field & 0xF0 == CONNECT:
#         s += "CONNECT"
#     elif control_field & 0xF0 == CONNACK:
#         s += "CONNACK"
#     elif control_field & 0xF0 == PUBLISH:
#         s += "PUBLISH"
#     elif control_field & 0xF0 == PUBACK:
#         s += "PUBACK"
#     elif control_field & 0xF0 == PUBREC:
#         s += "PUBREC"
#     elif control_field & 0xF0 == PUBREL:
#         s += "PUBREL"
#     elif control_field & 0xF0 == PUBCOMP:
#         s += "PUBCOMP"
#     elif control_field & 0xF0 == SUBSCRIBE:
#         s += "SUBSCRIBE"
#     elif control_field & 0xF0 == SUBACK:
#         s += "SUBACK"
#     elif control_field & 0xF0 == UNSUBSCRIBE:
#         s += "UNSUBSCRIBE"
#     elif control_field & 0xF0 == UNSUBACK:
#         s += "UNSUBACK"
#     elif control_field & 0xF0 == PINGREQ:
#         s += "PINGREQ"
#     elif control_field & 0xF0 == PINGRESP:
#         s += "PINGRESP"
#     elif control_field & 0xF0 == DISCONNECT:
#         s += "DISCONNECT"
#     else:
#         s += "RESERVED"
#     return s


class ControlField:
    def __init__(self, packet_type, dup=0, qos=1, retain=0):
        self.packet_type = packet_type
        self.dup = dup
        self.qos = qos
        self.retain = retain
        self.control_field = hex(packet_type | (
            dup << 3) | (qos << 1) | retain)

    @classmethod
    def parse(cls, control_field: hex):
        control_field = control_field
        packet_type = control_field & 0xF0
        dup = (control_field & 0x08) >> 3
        qos = (control_field & 0x06) >> 1
        retain = control_field & 0x01
        self = cls(packet_type, dup, qos, retain)
        return self

    def __str__(self):
        return "ControlField(%s, %s, %s, %s)" % (control_field_to_str(self.packet_type), self.dup, self.qos, self.retain)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.control_field == other.control_field

    def __ne__(self, other):
        return self.control_field != other.control_field

    def binstr(self):
        binary = bin(int(self.control_field, 16))[2:].zfill(8)
        return binary[:4] + '(PacketType)-' + binary[4:5] + '(DUP)-' + binary[5:7] + '(QOS)-' + binary[7:] + '(RETAIN)'


class ConnectFlag:

    def __init__(self, username=0, password=0, will_retain=0, will_qos=0, will=0, clean_session=0) -> None:
        self.username = username
        self.password = password
        self.will_retain = will_retain
        self.will_qos = will_qos
        self.will = will
        self.clean_session = clean_session

    def to_bytes(self):
        flags = 0
        if self.username:
            flags |= USERNAME_FLAG
        if self.password:
            flags |= PASSWORD_FLAG
        if self.will_retain:
            flags |= WILL_RETAIN_FLAG
        if self.will:
            flags |= WILL_FLAG
        if self.clean_session:
            flags |= CLEAN_SESSION_FLAG
        if self.will_qos > 2 or self.will_qos < 0:
            raise ValueError("Invalid QoS %s" % self.will_qos)
        flags |= self.will_qos << WILL_QOS_FLAG_SHIFT

        return hex(flags)


class ConnectPacket:

    def __init__(self, version, keepalive, client_id, username = None, password = None) -> None:
        self.packet_type = CONNECT
        self.version = version
        self.keepalive = keepalive
        self.client_id = client_id
        self.flags = 0
        self.will_topic = None
        self.will_message = None
        self.username = username
        self.password = password
        self.properties = {}

    @classmethod
    def parse(cls, packet: bytes):
        packet = packet
        # Parse the variable header
        protocol_name = packet[0:6]
        version = packet[6]
        flags = packet[7]
        keepalive = packet[8:10]
        properties = packet[10:]
        # Parse the payload
        client_id = packet[10:]
        self = cls(version, keepalive, client_id)
        self.flags = flags
        self.properties = properties
        return self

    def to_bytes(self):
        connect_flag = ConnectFlag(clean_session=1)
        if self.username:
            connect_flag.username = 1
        if self.password:
            connect_flag.password = 1
        connect_flag = connect_flag.to_bytes()
        packet = b''
        packet += bytes([self.packet_type])
        protocal_name_length = bytes([0, 4])
        protocol_name = b'MQTT'
        protocol_level = bytes([self.version])
        connect_flags = bytes([int(connect_flag, 16)])
        keepalive = bytes([0, self.keepalive])
        property_length = bytes([5])
        property_id = bytes([17])
        property_value = bytes([0,0, 0, 10])
        client_id = self.client_id.encode()
        client_id_length = bytes([0, len(client_id)])
        variable_header = protocal_name_length +  protocol_name + protocol_level + connect_flags + keepalive + property_length + property_id + property_value + client_id_length + client_id 
        if self.username:
            username = self.username.encode()
            username_length = bytes([0, len(username)])
            variable_header += username_length + username
        if self.password:
            password = self.password.encode()
            password_length = bytes([0, len(password)])
            variable_header += password_length + password
        packet += bytes([len(variable_header)])
        packet += variable_header
        # Variable header
        return packet


class SubsribePacket:
    
        def __init__(self, packet_id, topic, qos) -> None:
            self.packet_type = SUBSCRIBE
            self.packet_id = packet_id
            self.topic = topic
            self.qos = qos
    
        @classmethod
        def parse(cls, packet: bytes):
            packet = packet
            # Parse the variable header
            packet_id = packet[0:2]
            properties = packet[2:]
            # Parse the payload
            topic = packet[2:]
            qos = packet[2:]
            self = cls(packet_id, topic, qos)
            self.properties = properties
            return self
    
        def to_bytes(self):
            packet = b''
            packet += bytes([self.packet_type])
            packet_id = bytes([0, self.packet_id])
            property_length = bytes([2])
            property_id = bytes([11])
            property_value = bytes([38])
            topic = self.topic.encode()
            topic_length = bytes([0, len(topic)])
            qos = bytes([self.qos])
            payload = packet_id + property_length + property_id + property_value + topic_length + topic + qos
            packet += bytes([len(payload)])
            packet += payload
            return packet



class PingPacket:
    
        def __init__(self) -> None:
            self.packet_type = PINGREQ
    
        @classmethod
        def parse(cls, packet: bytes):
            packet = packet
            self = cls()
            return self
    
        def to_bytes(self):
            packet = b''
            packet += bytes([self.packet_type])
            packet += bytes([0])
            return packet


class PublishPacket:

    def __init__(self, topic, payload, qos=0, retain=0, dup=0, packet_id=None) -> None:
        self.packet_type = PUBLISH
        self.topic = topic
        self.payload = payload
        self.qos = qos
        self.retain = retain
        self.dup = dup
        self.packet_id = packet_id
        self.properties = {}

    @classmethod
    def parse(cls, packet: bytes, qos=0):
        # Parse the variable header
        topic_length = packet[0:2]
        print(f"topic_length: {topic_length}")
        topic = packet[2:2 + int.from_bytes(topic_length, byteorder='big')]
        packet_id = None
        if qos > 0:
            packet_id = packet[2 + int.from_bytes(topic_length, byteorder='big'):2 + int.from_bytes(topic_length, byteorder='big') + 2]
        topic_length_int = int.from_bytes(topic_length, byteorder='big')
        property_length = packet[2 + topic_length_int : topic_length_int + 3 ]
        properties = packet[3 + topic_length_int : 3 + topic_length_int + int.from_bytes(property_length, byteorder='big')] 
        # Parse the payload
        payload = packet[3+ topic_length_int + int.from_bytes(property_length, byteorder='big'):].decode()
        self = cls(topic, payload, qos)
        self.packet_id = packet_id
        self.properties = properties
        self.topic = topic
        return self

    def to_bytes(self):
        packet = b''
        packet += bytes([self.packet_type])
        topic = self.topic.encode('utf-8')
        topic_length = bytes([0, len(topic)])
        property_length = bytes([0])
        variable_header = topic_length + topic + property_length
        if self.qos > 0:
            if self.packet_id is None:
                self.packet_id = uuid.uuid4().int & 0xFFFF 
            packet_id = bytes([0, self.packet_id])
            variable_header += packet_id
        packet += bytes([len(variable_header) + len(self.payload.encode('utf-8'))])
        packet += variable_header
        # Variable header
        packet += self.payload.encode('utf-8')
        return packet
    
    def __str__(self):
        return "PublishPacket(%s, %s, %s, %s, %s, %s)" % (self.topic, self.payload, self.qos, self.retain, self.dup, self.packet_id)

class MQTTException(Exception):
    pass
