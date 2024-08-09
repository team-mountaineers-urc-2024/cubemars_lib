# cubemars_lib

# This was planned, we didn't end up using cubemars motors

Message [Nate Adkins](mailto:npa00003@mix.wvu.edu) on Slack with any questions or suggestions

## Overview

This Python library facilitates the control of Cube Mars motors. The library consists of one `Motor` class. 

## Classes

### Motor Class

The `Motor` class defines methods for creating can messages to a cubemars motor. It also includes a method for parsing received messages.

#### Attributes
- `CAN_ID_BITS`: Dictionary containing bit slices for various CAN ID fields.
- `CONTROL_MODES`: Dictionary mapping control mode names to their respective values.
- `CAN_PACKET_ID`: Dictionary mapping CAN packet names to their respective values.
- `COMM_PACKET_ID`: Dictionary mapping communication packet names to their respective values.

## Installation 

### 1. Clone this repository
- ```bash
  git clone git@github.com:wvu-urc/cubemars_lib.git
  ```
### 2. Navigate to the repository directory 
- ```bash
  cd cubemars_lib
  ```
### 3. Install the pip package
- ```bash 
  pip install . 
  ```

## Usage
```python
from cubemars_lib import Motor
motor_instance = Motor(arbitration_id=1)
message = motor_instance.set_duty(duty=0.5)
# (now send can message over interface of your choice)
# See can_interface_pkg for ROS implementation
```

## Known Limitations
This package was never used on the system as CubeMars motors were not used. As a result, most of the code here has only recieved minimal testing and may not work. The general ideas presented should, but the current implementation may have some issues