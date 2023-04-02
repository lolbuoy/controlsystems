# controlsystems

code used to command the autopilot thru a companion computer based on external i/ps or other functions
Requirements:


   i) Ardupilot code setup on your linux machine :
   
   
   
   
   make sure you have 'git' ; if not follow the below :
    
        i)sudo apt-get update
    
    
        ii)sudo apt-get install git
   video reference:

   https://www.youtube.com/watch?v=G1Kc-1aF8HI  
   
   
   then clone the ardupilot rep:
   
      git clone https://github.com/your-github-userid/ardupilot
   
      cd ardupilot
    
      git submodule update --init --recursive
  video reference:
  
  https://www.youtube.com/watch?v=kAli2y2-n-M
  
  for this section please follow the video link :
  
  https://www.youtube.com/watch?v=4B8BVskH0vc
  
  From ardupilot directory :

      Tools/environment_install/install-prereqs-ubuntu.sh -y

Reload the path (log-out and log-in to make permanent):

      . ~/.profile
 
If there have been updates to some git submodules you may need to do a full clean build. To do that use:

      ./waf clean

that will remove the build artifacts so you can do a build from scratch

Start SITL simulator :

      cd ardupilot/Tools/autotest
      
      python sim_vehicle.py -v ArduCopter --map --console


ii) Pymavlink installed on your machine :

      pip install --upgrade pymavlink MAVProxy --user
