# Manipulator
The high level design and approach to this lab is to define the joint screw axes in space and body frame. 
From there, the user must derive forward kinematics via product of exponentials of matrix representations of screws. 
For the inverse kinematics, we must calculate the joint coordinates. 
Finally, run the program and verify the positions of the x,y, and z.           
 

The low level design and description to the approach of this problem is first to find the M matrix of the actuator. 
Secondly, finding the S values of each joint.With those values, it will be multiplied with the angle.
Then it will use Grubler’s formula to exponentiate each array. The program only care for the position of the end effector. 
This means that we should use augmented vector
