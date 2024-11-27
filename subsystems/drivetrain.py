import rev
import wpilib.drive as wpdrive
from wpilib import RobotBase
from rev import SparkRelativeEncoder
from rev import CANSparkMax
import constants


class Drivetrain:
#initializing motors: there are only 4 motors so 1 lead motor and 1 follow motor per side
    leftLeadMotor: CANSparkMax
    rightLeadMotor: CANSparkMax

    leftFollowMotor1: CANSparkMax
    rightFollowMotor1: CANSparkMax

    fwdSpeed: float = 0.0
    turnSpeed: float = 0.0
    currentSpeed: float = 0.0
       
#When the robot starts up, define which motors are which and their orientation. #Setup Defaults
    def setup(self):

#Left side of the chassis      
        self.leftLeadMotor = CANSparkMax(constants.LEFT_DRIVE_MOTOR_LEADER_CAN_ID, rev.CANSparkMax.MotorType.kBrushless)
        self.leftLeadMotor.restoreFactoryDefaults()
        self.leftLeadMotor.setSmartCurrentLimit(constants.PEAK_MOTOR_AMPS)
        self.leftLeadMotor.setInverted(constants.LEFT_INVERTED) #FALSE
        self.leftLeadMotor.setIdleMode(CANSparkMax.IdleMode.kBrake)
        #self.leftLeadMotor.setOpenLoopRampRate(constants.RAMP_RATE)

        self.leftFollowMotor1 = CANSparkMax(constants.LEFT_DRIVE_MOTOR_FOLLOWER1_CAN_ID, rev.CANSparkMax.MotorType.kBrushless)
        self.leftFollowMotor1.restoreFactoryDefaults()
        self.leftFollowMotor1.setSmartCurrentLimit(constants.PEAK_MOTOR_AMPS)
        self.leftFollowMotor1.setInverted(constants.LEFT_INVERTED)
        self.leftFollowMotor1.follow(self.leftLeadMotor)
        self.leftFollowMotor1.setIdleMode(CANSparkMax.IdleMode.kBrake)
        #self.leftFollowMotor1.setOpenLoopRampRate(constants.RAMP_RATE)
        
#Right side of the chassis
        self.rightLeadMotor = CANSparkMax(constants.RIGHT_DRIVE_MOTOR_LEADER_CAN_ID, rev.CANSparkMax.MotorType.kBrushless)
        self.rightLeadMotor.restoreFactoryDefaults()
        self.rightLeadMotor.setSmartCurrentLimit(constants.PEAK_MOTOR_AMPS)
        self.rightLeadMotor.setInverted(constants.RIGHT_INVERTED)
        self.rightLeadMotor.setIdleMode(CANSparkMax.IdleMode.kBrake)
        #self.rightLeadMotor.setOpenLoopRampRate(constants.RAMP_RATE)


        self.rightFollowMotor1 = CANSparkMax(constants.RIGHT_DRIVE_MOTOR_FOLLOWER1_CAN_ID, rev.CANSparkMax.MotorType.kBrushless) 
        self.rightFollowMotor1.restoreFactoryDefaults()
        self.rightFollowMotor1.setSmartCurrentLimit(constants.PEAK_MOTOR_AMPS)
        self.rightFollowMotor1.setInverted(constants.RIGHT_INVERTED)
        self.rightFollowMotor1.follow(self.rightLeadMotor)
        self.rightFollowMotor1.setIdleMode(CANSparkMax.IdleMode.kBrake)
        #self.rightFollowMotor1.setOpenLoopRampRate(constants.RAMP_RATE)
        
#Encoder Stuff
        self.leftEncoder = self.leftLeadMotor.getEncoder(SparkRelativeEncoder.Type.kHallSensor,countsPerRev=constants.DRIVE_ENCODER_TICKS_PER_REV)
        self.leftEncoder.setPosition(0.0)

        self.rightEncoder = self.rightLeadMotor.getEncoder(SparkRelativeEncoder.Type.kHallSensor,countsPerRev=constants.DRIVE_ENCODER_TICKS_PER_REV)
        self.rightEncoder.setPosition(0.0)


        self.diffDrive = wpdrive.DifferentialDrive(self.leftLeadMotor, self.rightLeadMotor)

    def setMotorSpeeds(self,desiredSpeed,turnSpeed):
        
        if (desiredSpeed < 0.2) and (desiredSpeed > -0.2):
            self.currentSpeed = 0.0
        else:
            self.speedChange =  desiredSpeed - self.currentSpeed # see how much we need too accelerate by
            
            if desiredSpeed != self.currentSpeed: 
                # We havent reached out desired speed yet. 
                # Making sure we control how fast we accelerate (aka no 0-100) if the difference between our desired and our current speed is bigger than our RAMP_RATE, 
                # accelerate only by RAMP_RATE
                if self.speedChange >= constants.RAMP_RATE: 
                    self.speedChange = constants.RAMP_RATE
                elif self.speedChange <= -constants.RAMP_RATE: 
                    self.speedChange = -constants.RAMP_RATE
        

            self.currentSpeed = self.currentSpeed + self.speedChange

        self.fwdSpeed = self.currentSpeed
        self.turnSpeed = turnSpeed
    
    
    def execute(self):
        self.diffDrive.arcadeDrive(self.fwdSpeed ,self.turnSpeed)