# Tommy_bot

* Project and documentation in early development. Normally I would have a more polished product before adding it to GitHub however I am using GitHub as a way to sync my files between my laptop and RPi 4. I write my code on my laptop then run it on the RPi 4 (tommy) when I need to test it. Its not convenient to have a screen hooked up to a mobile robot and I am not a command line warrior yet so terminal text editors for lengthy coding is not ideal either and I haven't found another good way to keep files synchronised. I am open to alternatives workflows? *

Tommy_bot is a mobile robot I am building for two main reasons: 
 - Learning robotics 
 - Creating a platform to explore fun analogous to robotic systems that could be deployed at extra terrestrial habitats and settlements  

Tommy_bot is currently implemented using Python and ROS, eventually including C++ once I have learnt enough and have the time to re-write my code or I need significant speed improvements. My first robot Dexter_bot was written in pure Python with a lot simpler features. Implementing ROS has advantages and disadvantages but the main reason I did it was for learning purposes, however I am very open to suggestions and tips if you think my implementations of things can be improved. 

Upgrading to ROS2 is a far-future aim but for now standard ROS is good enough. 

## Features 
### Main
	- Broadcasts its own access point on boot
	- Manual control via web browser by connecting through your local network (wifi) or directly via the RPI 4 access point
	- Live video streaming 
	- SLAM for autonomous control - *in progress
	
### Minor
	- LCD screen to relay important messages and robot status
	- Text to Speech for relaying messages via audio
	- LED status indicator

### Wishlist
	- Low battery protection
	- Battery swapout (manual/autonomous)
	- Autonomous navigation
	- Automatic docking
	- Improved software and hardware abstraction 

## Limitations 

I designed tommy_bot with controller indoor environments in mind for now. Obviously in an extra-terreistal setting this is not realistic but a lot of the basic software features needed are similar and its makes it a lot simpler to implement that hardware. Once the project has matured and is more abstracted from the hardware I plan to make an "off-road" version.  


## Hardware
The first implementation of tommy_bot is using the main following hardware: 
- Raspberry Pi 4
- Stepper Motors 
- DVR8825 Stepper Drivers

### Main Hardware Choice Reasoning
I went with a Raspberry Pi 4 as I has some experience with it and Python plus I could *just about* install ROS on it. However I must admit the ROS implementation is a lot slower than my pure python version. I am not smart enough to know why but I assume it due to the lack of RPi4 power and also poor code implementation on my part due to having to get my head around making the stepper motors drive the way I want them to i.e. at one point I have three nested while loops (I know I am terrible, its a work in progress, all help it welcome) 

### Minor Hardware

### Current Hardware Cons

### Current Hardware Pros

### Hardware improvements 
	- Quieter stepper motor drivers 
	

## Files/ Structure
	1. Administrator
	2. Peripherals 
	3. Powertrain
	4. Sensors
	5. Tommy_bringup
	6. Webapp

### Administrator 
This 'module' handles ...
 Included Features
	- Modes ...

### Peripherals 
This 'module' handles ...

### Powertrain
This 'module' handles ...

### Sensors
This 'module' handles ...

### Tommy_bringup
This 'module' handles ...

### Webapp
This 'module' handles ...

## Getting started 
I did this so long ago I cannot remember all the steps I did to get dexter/tommy up and running. I sued a number of tutorials and inspirations especially around setting up an access point and getting the live video stream to work that I will have to dig up the links and do them over again to document them fully. If you are curious in the mean time just raise an issue and I will try and answer your query

##  Installation

## Setup

## Usage
