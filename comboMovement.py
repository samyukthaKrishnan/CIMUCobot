from xarm.wrapper import XArmAPI
import time

arm = XArmAPI('127.0.0.1')

WIRE_SAFE_POSE = [0, -30.0, 0, -10.0, 175.0]

def prepare_arm():
    arm.clean_error()
    arm.motion_enable(True)
    arm.set_mode(0)
    arm.set_state(0)
    time.sleep(0.5)

def move_whole_arm_forward_then_touch(j2_move, j3_move, j4_move, j4_touch, hold_time=3.0):
    prepare_arm()

    print("Moving to safe home...")
    code = arm.set_servo_angle(angle=WIRE_SAFE_POSE, speed=20, wait=True)
    if code != 0:
        print(f"Safe home failed, code={code}")
        return

    home_pose = WIRE_SAFE_POSE[:]

    # STEP 1: move the whole arm forward using J2 + J3 + J4
    forward_pose = home_pose[:]
    forward_pose[1] = home_pose[1] + 7 * j2_move   # J2
    forward_pose[2] = home_pose[2] + 10 * j3_move   # J3
    forward_pose[3] = home_pose[3] + j4_move   # J4

    print(f"J2: {home_pose[1]:.1f} -> {forward_pose[1]:.1f}")
    print(f"J3: {home_pose[2]:.1f} -> {forward_pose[2]:.1f}")
    print(f"J4: {home_pose[3]:.1f} -> {forward_pose[3]:.1f}")

    code = arm.set_servo_angle(angle=forward_pose, speed=15, wait=True)
    if code != 0:
        print(f"Whole-arm forward move failed, code={code}")
        return

    # STEP 2: do the final touch using more J4
    touch_pose = forward_pose[:]
    touch_pose[3] = forward_pose[3] + j4_touch

    print(f"Touch with J4: {forward_pose[3]:.1f} -> {touch_pose[3]:.1f}")
    code = arm.set_servo_angle(angle=touch_pose, speed=12, wait=True)
    if code != 0:
        print(f"Touch move failed, code={code}")
        return

    print(f"Holding for {hold_time} seconds...")
    time.sleep(hold_time)

    # STEP 3: back out of touch
    print("Returning from touch...")
    code = arm.set_servo_angle(angle=forward_pose, speed=12, wait=True)
    if code != 0:
        print(f"Touch return failed, code={code}")
        return

    # STEP 4: return home
    print("Returning to safe home...")
    code = arm.set_servo_angle(angle=home_pose, speed=15, wait=True)
    if code != 0:
        print(f"Return home failed, code={code}")
        return

    print("Done.")

move_whole_arm_forward_then_touch(
    j2_move=8,
    j3_move=-8,
    j4_move=6,
    j4_touch=6,
    hold_time=3.0
)

arm.disconnect()

arm.disconnect()