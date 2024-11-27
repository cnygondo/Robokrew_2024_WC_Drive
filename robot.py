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
        self.leftLeadMotor = CANSparkMax(constants.LEFT_DRIVE_MOTOR_LEADER_CAN_ID, rev.CANSparkMax.MotorType.kBrushless)
        self.rightLeadMotor = CANSparkMax(constants.RIGHT_DRIVE_MOTOR_LEADER_CAN_ID, rev.CANSparkMax.MotorType.kBrushless)
        self.leftFollowMotor1 = CANSparkMax(constants.LEFT_DRIVE_MOTOR_FOLLOWER1_CAN_ID, rev.CANSparkMax.MotorType.kBrushless)
        #self.leftFollowMotor2 = CANSparkMax(constants.LEFT_DRIVE_MOTOR_FOLLOWER2_CAN_ID, rev.CANSparkMax.MotorType.kBrushless)
        self.rightFollowMotor1 = CANSparkMax(constants.RIGHT_DRIVE_MOTOR_FOLLOWER1_CAN_ID, rev.CANSparkMax.MotorType.kBrushless) 
        #self.rightFollowMotor2 = CANSparkMax(constants.RIGHT_DRIVE_MOTOR_FOLLOWER2_CAN_ID, rev.CANSparkMax.MotorType.kBrushless) 
        self.climbMotor = CANSparkMax(constants.CLIMBER_MOTOR_CAN_ID,rev.CANSparkMax.MotorType.kBrushless)
        # else:

        #if the robot is in a simulation, then use CTREPCM for the pistons
        #else, set the pistons to REVPH
        if wpilib.RobotBase.isSimulation():
            self.tablePiston = wpilib.Solenoid(wpilib.PneumaticsModuleType.CTREPCM,0)
            self.sliderPiston = wpilib.Solenoid(wpilib.PneumaticsModuleType.CTREPCM,1)
        else:
            self.tablePiston = wpilib.Solenoid(wpilib.PneumaticsModuleType.REVPH,0)
            self.sliderPiston = wpilib.Solenoid(wpilib.PneumaticsModuleType.REVPH,1)
        self.currentTableState = Table.TableState.PICKUP
        self.currentSliderState = Table.SliderState.IN

       
        
    def autonomousInit(self) -> None:
        self.drivetrain.leftEncoder.setPosition(0.0)
        self.drivetrain.rightEncoder.setPosition(0.0)
        return super().autonomousInit()
   
    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.drivetrain.setMotorSpeeds(0.0, 0.0)
        wpilib.SmartDashboard.putString("TABLE STATE", "NONE")
        self.table.updateSliderState(Table.SliderState.IN)




    def teleopPeriodic(self):
        #display limelightvalues to Dashboard
        # wpilib.SmartDashboard.putBoolean("Valid Target", self.limelight.foundValidTarget())
        # wpilib.SmartDashboard.putNumber("Horizontal Offset", self.limelight.getHorizontalOffset())
        # wpilib.SmartDashboard.putNumber("Vertical Offset", self.limelight.getVerticalOffset())
        # wpilib.SmartDashboard.putNumber("Target Area", self.limelight.getTargetArea())
        # wpilib.SmartDashboard.putBoolean("areWeCloseEnough", self.limelight.areWeCloseEnough())
        # wpilib.SmartDashboard.putBoolean("hasTarget", self.limelight.hasTarget())
        wpilib.SmartDashboard.putNumber("TeleopDriveSpeedL", self.drivetrain.leftLeadMotor.get())
        wpilib.SmartDashboard.putNumber("TeleopDriveSpeedR", self.drivetrain.rightLeadMotor.get())
        
        #values for colors do NOT match the list online on the REV website
        # if self.limelight.hasTarget():
        #     if self.limelight.areWeCloseEnough():
        #         wpilib.SmartDashboard.putString("LED COLOR", "GREEN")
        #         self.lights.setColor(Lights.Color.GREEN)
        #     else:
        #         wpilib.SmartDashboard.putString("LED COLOR", "YELLOW")
        #         self.lights.setColor(Lights.Color.YELLOW)
        # else:
        #         wpilib.SmartDashboard.putString("LED COLOR", "RED")
        #         self.lights.setColor(Lights.Color.RED)
        #         # No Target Found RED
                
        #runs auto sequence to score note (lift table,extend,wait,lower table,retract)
        if self.operatorJoy.getXButtonPressed():
            self.score.engage()
        
        #runs auto sequence to pickup note (lower table,retract,flash lights)
        if self.operatorJoy.getBButtonPressed():
            self.pickup.pickupNote() 
        
        # #takes input from directional pad/POV and converts it to motor speed
        # if self.driveJoy.getPOV() == 0:
        #     self.climber.setMotorSpeed(constants.CLIMBER_MOTOR_SPEED)
        # if self.driveJoy.getPOV() == 180:
        #     self.climber.setMotorSpeed(-constants.CLIMBER_MOTOR_SPEED)
        # if self.driveJoy.getPOV() == -1:
        #     self.climber.setMotorSpeed(0.0)


        ## controls for independent movement of each mechanism
        if self.operatorJoy.getLeftBumperPressed():
            self.table.updateSliderState(Table.SliderState.IN)  
        if self.operatorJoy.getRightBumperPressed():
            self.table.updateSliderState(Table.SliderState.OUT)  
        if self.operatorJoy.getYButtonPressed():
            self.table.updateTableState(Table.TableState.SCORE)
        if self.operatorJoy.getAButtonReleased():
            self.table.updateTableState(Table.TableState.PICKUP)
        
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