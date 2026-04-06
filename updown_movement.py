from xarm.wrapper import XArmAPI
import time

arm = XArmAPI('127.0.0.1')

# --- CONFIGURATION ---
TARGET_OBJECTS = [300.0, 600.0, 900.0] # Known Y-coordinates of objects
ONE_FOOT = 304.8   
TOUCH_DEPTH = 60.0 
STEP_SIZE = 50.0   
SAFE_HEIGHT = 200.0 
SCAN_END_LIMIT = 1100.0 # This is the "Very End"

def move_to_safe_home():
    """Retracts arm to the vertical 'Lens Up' position"""
    print("!!! Returning to Safe Home State !!!")
    arm.clean_error()
    arm.set_state(0)
    # Straight up, Joint 5 flipped to ceiling
    safe_joints = [0, 0, 0, 0, 175.0]
    arm.set_servo_angle(angle=safe_joints, speed=50, wait=True)

def setup():
    arm.clean_error()
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)
    # Start at Y=0
    arm.set_position(x=300, y=0, z=SAFE_HEIGHT, roll=180, pitch=0, yaw=0, wait=True)

def scan_and_move():
    # Loop from start to the SCAN_END_LIMIT
    for y_pos in range(0, int(SCAN_END_LIMIT) + int(STEP_SIZE), int(STEP_SIZE)):
        # 1. Move to next scan point
        arm.set_position(y=y_pos, wait=True)
        
        # 2. Virtual Sensor Check
        found_near_object = False
        for obj_y in TARGET_OBJECTS[:]: # Use [:] to allow removing items while looping
            distance = obj_y - y_pos
            
            if 0 < distance <= ONE_FOOT:
                print(f"Object detected {distance:.1f}mm ahead. Performing touch.")
                # Perform Touch
                code, pos = arm.get_position()
                arm.set_position(z=pos[2]-TOUCH_DEPTH, speed=20, wait=True)
                arm.set_position(z=SAFE_HEIGHT, speed=20, wait=True)
                TARGET_OBJECTS.remove(obj_y)
                found_near_object = True
                break 

    # --- THE "VERY END" LOGIC ---
    print("Reached the end of the scan area.")
    # If the list is empty (all detected) OR we simply reached the limit
    move_to_safe_home()

# Execute
setup()
scan_and_move()
arm.disconnect()