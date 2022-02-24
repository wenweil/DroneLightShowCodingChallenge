# DroneLightShowCodingChallenge

There are two main part of of this project

simulator.py found in the folder control

This is a server that listens for any incomming commands for any particular drones
and move its position in 3d space as well as change its color,
since I don't have any drones in my disposal I used a library to render boxes representing the drones
This server will also dump information (position, color, LED brightness) about every drown it can control, and report on a specific one if necessary 

controller.py found in the folder shape

This file will generate points for the drones to follow by converting a wavefront object file into a series of points and then rotating said points by 
a set amout along the z-axis to generate new points. As drones fly toward these points they generate a rotating shape in the sky.

A video demoing the code running on my machine can be found here:
https://youtu.be/yFTLg0dOof8





