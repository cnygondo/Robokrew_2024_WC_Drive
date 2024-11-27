import magicbot
from subsystems.drivetrain import Drivetrain
import constants
from rev import CANSparkMax
import wpilib
import rev

class MyRobot(magicbot.MagicRobot):

    drivetrain: Drivetrain

#create objects for initialization
    def createObjects(self):

        self.driveJoy = wpilib.XboxController(0)
        self.operatorJoy = wpilib.XboxController(1)
        #self.leftLeadMotor = CANSparkMax(constants.LEFT_DRIVE_MOTOR_LEADER_CAN_ID, rev.CANSparkMax.MotorType.kBrushless)
        #self.rightLeadMotor = CANSparkMax(constants.RIGHT_DRIVE_MOTOR_LEADER_CAN_ID, rev.CANSparkMax.MotorType.kBrushless)
        #self.leftFollowMotor1 = CANSparkMax(constants.LEFT_DRIVE_MOTOR_FOLLOWER1_CAN_ID, rev.CANSparkMax.MotorType.kBrushless)
        #self.rightFollowMotor1 = CANSparkMax(constants.RIGHT_DRIVE_MOTOR_FOLLOWER1_CAN_ID, rev.CANSparkMax.MotorType.kBrushless) 


    def autonomousInit(self) -> None:
        self.drivetrain.leftEncoder.setPosition(0.0)
        self.drivetrain.rightEncoder.setPosition(0.0)
        return super().autonomousInit()
   
    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.drivetrain.setMotorSpeeds(0.0, 0.0)

    def teleopPeriodic(self):

        wpilib.SmartDashboard.putNumber("TeleopDriveSpeedL", self.drivetrain.leftLeadMotor.get())
        wpilib.SmartDashboard.putNumber("TeleopDriveSpeedR", self.drivetrain.rightLeadMotor.get())
              
    #drivetrain code that reads drivestick values 
    #accounts for xbox controller drift (this applies to green controllers but not the new controllers)
        left_axis_speed = self.driveJoy.getLeftY()
        if(left_axis_speed > -0.2 and left_axis_speed < 0.2):
            left_axis_speed = 0.0 
        right_axis_speed = self.driveJoy.getRightX()
        if(right_axis_speed > -0.2 and right_axis_speed < 0.2):
            right_axis_speed = 0.0
        if self.driveJoy.getRightBumper(): #reverse drive so climber is front
            left_axis_speed = -left_axis_speed
        self.drivetrain.setMotorSpeeds(left_axis_speed, right_axis_speed)
        

if __name__ == '__main__':
    wpilib.run(MyRobot)