# Vacuum Skill
This skill allowes you to control your vacuums with Alice.

### Supported devices:
- Xiaomi Vacuum
- Roborock S5 / S5max / S6

### Setup:
- Enter the web interface and go to "myHome".
- Create all rooms you want to clean
- Add devices where ever they are in your home
- Create "device links" from every device to the rooms it should be able to clean
- change the device settings
    - Roborock/Xiaomi:
        - Insert the fixed IP of the device in your network (find it in your router)
        - Insert the token of your vacuum ([How to find your token])
        - Edit the settings per room. 
            - Every room needs a "roomId", which is numeric, starting from 1.
        Enter a number, start cleaning that room, and see in your app, what room is cleaned. 
        Repeat with other numbers until you have all your Roborock roomId.
        A "fresh" vacuum should start with 1 and have consecutive numbers.

### Usage:
- Clean a room
    - "clean the living room"
    - "vacuum in the kitchen"
    - "Please clean the kitchen and bathing room"
- Recharge the vacuum
    - "Please recharge the vacuum"
    - "Return the vacuum to its base"
    - "Send the vacuum to the station"
- Locate the vacuum
    - "Where is the vacuum"
    - "Please find my vacuum"
    - "Can you look for the vacuum"


[How to find your token]: https://www.smarthomeassistent.de/token-auslesen-roborock-s6-roborock-s5-xiaomi-mi-robot-xiaowa/
