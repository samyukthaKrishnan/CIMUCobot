from xarm.wrapper import XArmAPI
import time

arm = XArmAPI('127.0.0.1')

# 1. Reset the simulator state
arm.clean_error()
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)
time.sleep(1)

print("Starting maintenance motion for Joint 4...")

# The 4th number (index 3) controls the part you circled.
# 90 degrees bends it down like a hook.
arm.set_servo_angle(angle=[0, 0, 0, -90, 0], speed=30, wait=True)
print("Joint 4 is now DOWN.")
time.sleep(1)


arm.disconnect()