# GCS
Ground Control Station

## Working with the interop server:
  ### To establish a vpn connection to the pi via SSH (Obtain username & IP from someone):
    > sshuttle -r USER@IP -x IP -x 192.168.0.27 0/32 0/0
  ### To access the administration (in browser):
    > 192.168.0.27:8000

## Structure
- */main.py*
    - The file that is run and controls all of the submodules
- */modules/*
  - Each submodule represents an area of the competition
    - *interop*
      - [ ] Be able to successfully connect to the interop server with a given mission ID
      - [ ] Be able to parse mission details and generate a map containing mission waypoints and obstacles
      - [ ] Be able to retrieve telemetry data from Mission Planner and submit to interop
      - [ ] Be able to parse ODCL object data (both from GUI and from plane, includes characteristics, cropped image, and localization details) and submit it to interop
      - [ ] Be able to get the other plane's position from telemetry
      - [ ] Whatever needs to be run on startup is run on startup (directly called by *main.py*)

    - *MP communication*
      - [ ] Be able to run a script on MP
      - [ ] Communication w/ MP script is established on startup
      - [ ] Be able to send telemetry data from MP script to main script
      - [ ] Be able to automatically upload waypoints generated from OA script

    - *ODLC*
      - [ ] Setup JS/HTML/CSS frontend for ODCL GUI w/ all necessary features
      - [ ] Setup Flask backend for ODCL GUI that allows for communication (using endpoints)
      - [ ] Be able to generate ODCL objects based on characteristics/geolocation

    - *Flight communication*
      - [ ] Create a consistent packet format that will be used for all messages
      - [ ] Establish a socket communication on startup
      - [ ] Be able to receive and send data at the same time, and be able to send multiple packets in a row w/o accumulation of data
      - [ ] Create a list of commands that will be used for communication between flight software and ground station
      - [ ] Be able to parse through a packet received from the flight software and perform all the necessary commands
