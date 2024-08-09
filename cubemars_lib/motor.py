import struct
import can

class Motor:
    CAN_ID_BITS = {
        "Control_mode": slice(8, 16),
        "Source_node_ID": slice(0, 8)
    }

    CONTROL_MODES = {
        "Duty_cycle_mode": 0,
        "Current_loop_mode": 1,
        "Current_brake_mode": 2,
        "Velocity_mode": 3,
        "Position_mode": 4,
        "Set_origin_mode": 5,
        "Position_velocity_loop_mode": 6
    }

    CAN_PACKET_ID = {
        "CAN_PACKET_SET_DUTY": 0,
        "CAN_PACKET_SET_CURRENT": 1,
        "CAN_PACKET_SET_CURRENT_BRAKE": 2,
        "CAN_PACKET_SET_RPM": 3,
        "CAN_PACKET_SET_POS": 4,
        "CAN_PACKET_SET_ORIGIN_HERE": 5,
        "CAN_PACKET_SET_POS_SPD": 6
    }

    COMM_PACKET_ID = {
        "COMM_FW_VERSION": 0,
        "COMM_JUMP_TO_BOOTLOADER": 1,
        "COMM_ERASE_NEW_APP": 2,
        "COMM_WRITE_NEW_APP_DATA": 3,
        "COMM_GET_VALUES": 4,
        "COMM_SET_DUTY": 5,
        "COMM_SET_CURRENT": 6,
        "COMM_SET_CURRENT_BRAKE": 7,
        "COMM_SET_RPM": 8,
        "COMM_SET_POS": 9,
        "COMM_SET_HANDBRAKE": 10,
        "COMM_SET_DETECT": 11,
        "COMM_ROTOR_POSITION": 22,
        "COMM_GET_VALUES_SETUP": 50,
        "COMM_SET_POS_SPD": 91,
        "COMM_SET_POS_MULTI": 92,
        "COMM_SET_POS_SINGLE": 93,
        "COMM_SET_POS_UNLIMITED": 94,
        "COMM_SET_POS_ORIGIN": 95
    }

    def __init__(self, arbitration_id):
        self.arbitration_id = arbitration_id

    def buffer_append_int32(self, buffer: bytearray, number):
        buffer.extend(struct.pack('>I', number))

    def buffer_append_int16(self, buffer: bytearray, number):
        buffer.extend(struct.pack('>H', number))

    def set_duty(self, duty, control_mode="Duty_cycle_mode"):
        buffer = bytearray()
        self.buffer_append_int32(buffer, int(duty * 100000.0))
        arbitration_id = (self.arbitration_id | (self.CONTROL_MODES[control_mode] << (self.CAN_ID_BITS["Control_mode"].start * 8)))
        return can.Message(
            arbitration_id=arbitration_id,
            data=buffer,
            is_extended_id=True
        )

    def set_current(self, current, control_mode="Current_loop_mode"):
        buffer = bytearray()
        self.buffer_append_int32(buffer, int(current * 1000.0))
        arbitration_id = (self.arbitration_id | (self.CONTROL_MODES[control_mode] << (self.CAN_ID_BITS["Control_mode"].start * 8)))
        return can.Message(
            arbitration_id=arbitration_id,
            data=buffer,
            is_extended_id=True
        )

    def set_cb(self, current, control_mode="Current_brake_mode"):
        buffer = bytearray()
        self.buffer_append_int32(buffer, int(current * 1000.0))
        arbitration_id = (self.arbitration_id | (self.CONTROL_MODES[control_mode] << (self.CAN_ID_BITS["Control_mode"].start * 8)))
        return can.Message(
            arbitration_id=arbitration_id,
            data=buffer,
            is_extended_id=True
        )

    def set_rpm(self, rpm, control_mode="Velocity_mode"):
        buffer = bytearray()
        self.buffer_append_int32(buffer, int(rpm))
        arbitration_id = (self.arbitration_id | (self.CONTROL_MODES[control_mode] << (self.CAN_ID_BITS["Control_mode"].start * 8)))
        return can.Message(
            arbitration_id=arbitration_id,
            data=buffer,
            is_extended_id=True
        )

    def set_pos(self, pos_degrees, control_mode="Position_mode"):
        buffer = bytearray()
        self.buffer_append_int32(buffer, int(pos_degrees * 1000000.0))
        arbitration_id = (self.arbitration_id | (self.CONTROL_MODES[control_mode] << (self.CAN_ID_BITS["Control_mode"].start * 8)))
        return can.Message(
            arbitration_id=arbitration_id,
            data=buffer,
            is_extended_id=True
        )

    def set_origin(self, set_origin_mode, control_mode="Set_origin_mode"):
        buffer = bytearray()
        self.buffer_append_int32(buffer, set_origin_mode)
        arbitration_id = (self.arbitration_id | (self.CONTROL_MODES[control_mode] << (self.CAN_ID_BITS["Control_mode"].start * 8)))
        return can.Message(
            arbitration_id=arbitration_id,
            data=buffer,
            is_extended_id=True
        )

    def set_pos_spd(self, pos, spd, RPA, control_mode="Position_velocity_loop_mode"):
        buffer = bytearray()
        self.buffer_append_int32(buffer, int(pos * 10000.0))
        self.buffer_append_int16(buffer, spd)
        self.buffer_append_int16(buffer, RPA)
        arbitration_id = (self.arbitration_id | (self.CONTROL_MODES[control_mode] << (self.CAN_ID_BITS["Control_mode"].start * 8)))
        return can.Message(
            arbitration_id=arbitration_id,
            data=buffer,
            is_extended_id=True
        )

    def parse_received_message(self, rx_message: can.Message):
        control_mode = (rx_message.arbitration_id >> (self.CAN_ID_BITS["Control_mode"].start * 8)) & 0xFF
        pos_int = (rx_message.data[0] << 24) | (rx_message.data[1] << 16) | (rx_message.data[2] << 8) | rx_message.data[3]
        spd_int = (rx_message.data[4] << 8) | rx_message.data[5]
        cur_int = (rx_message.data[6] << 8) | rx_message.data[7]

        return {
            'control_mode': control_mode,
            'motor_pos': float(pos_int * 0.0001),
            'motor_spd': float(spd_int * 10.0),
            'motor_cur': float(cur_int * 0.01),
            'motor_temp': rx_message.data[8],
            'motor_error': rx_message.data[9],
        }
    
