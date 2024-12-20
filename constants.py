import math

##Motor Configs
PEAK_MOTOR_AMPS = 7
LENGTH_AT_PEAK = 0
MAINTAIN_AMPS = 30
CONFIG_TIMEOUT = 0
CURRENTLIMITINGENABLED = True
RAMP_RATE = 0.5
CLIMBER_MOTOR_SPEED = 1.0
 
#Motor Numbers
LEFT_DRIVE_MOTOR_LEADER_CAN_ID = 3
LEFT_DRIVE_MOTOR_FOLLOWER1_CAN_ID = 1


RIGHT_DRIVE_MOTOR_LEADER_CAN_ID = 7
RIGHT_DRIVE_MOTOR_FOLLOWER1_CAN_ID = 5


#Inverted Booleans
LEFT_INVERTED = True
RIGHT_INVERTED = False


#Auto Drive PID coefficients
DRIVE_PID_P = 0.1
DRIVE_PID_I = 0.0
DRIVE_PID_D = 0.0
DRIVE_PID_FF = 0.0
DRIVE_PID_IZONE = 0.0
DRIVE_PID_KMAX = 1.0
DRIVE_PID_KMIN = -1.0
DRIVE_ENCODER_DEADBAND = 0.33

DRIVE_FWD_DISTANCE = 5.0 ##feeet
DRIVE_WHEEL_DIAMETER = 6.0 ##inches
DRIVE_WHEEL_CIRCUMFERENCE = math.pi * DRIVE_WHEEL_DIAMETER
DRIVE_ENCODER_TICKS_PER_REV = 42
DRIVE_MOTOR_REV_TO_WHEEL_REV = 8.45

# Ticks of the encoder in 1 motor revolution * number of motor revolutions per 1 wheel revolution
DRIVE_ENCODER_TICKS_PER_WHEEL_REV = DRIVE_ENCODER_TICKS_PER_REV * DRIVE_MOTOR_REV_TO_WHEEL_REV 

#Number of ticks we need to see to know we went the distance
DRIVE_ENCODER_TICKS_FWD_DISTANCE = (DRIVE_FWD_DISTANCE*12.0/DRIVE_WHEEL_CIRCUMFERENCE) * DRIVE_ENCODER_TICKS_PER_WHEEL_REV 


#Camera
HORIZONTAL_CENTER = 5.0 ##Deadband value to detect if center

TARGET_PERCENT_OF_IMAGE = 14.0 ## how much of the camera image is the april tag

AUTO_ALIGN_MAX_DRIVE_SPEED = 0.50



