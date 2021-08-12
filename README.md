# Covid19-Surveillance-System--HealthPass

A system to quickly detect symptoms of COVID19, such as body temperature and loss of smelling ability, in the entrance of public buildings.
The system also detects the mask usage of the entrant and the crowdness inside to allow the incoming person to enter.

## Remarks: 

* The system uses MongoDB to keep track of the number of people inside (from different entrances of the building, if there are) and to provide the options presented in the screen. If the user will not use the database, they can leave the variable inside the .env file as empty, otherwise "dbadress" string should be set to MongoDB connection string.
* The system designed to run on Raspberry Pi 4B. The pin configuration of the following sensors can be found in the final report document:
  * 2 HC-SR04 Ultrasound Distance Sensors
  * 1 MLX90614 Infrared Temperature Sensor
  * 1 Nokia 5110 LCD Screen
  * A relay circuit and doorlock 
  * 6 membrane buttons

Remaining details can be found in the [final report](AlgoDetectium%20Final%20Report.pdf). A video showing the usage of the system can be found [here](https://youtu.be/WAtMLCSrfC0).

