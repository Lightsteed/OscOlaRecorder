# OscOlaRecorder

a simple python script i hacked together to allow recording, playback, loop and shuffle of dmx data via OLA on a raspberry pi or compatible linux device.
I made it so i could easily record, trigger and run content to an LED installation, with an autopilot/shuffle function so i didnt have to keep my expensive latop at the event.
Runs great on a raspberry pi 3b+, receiving content VIA artnet from Resolume then sending sacn data to a pixlite 4 to control the LEDs.

It's super hacky as i dont know much about coding, but it works very well and is super responsive. If anyone would like to clean up my code or fork it and make it better then be my guest!

things to fix:

Make IP address automatic
Make it so loop duration can be changed on the fly (currently you need to stop and start shuffle playback to affect loop duration due to how i have implemented it.
Make it so you can playback multiple recordings at a time, but not so many that it overloads the CPU. ( i have manually ran 6 recordings at once and OLA merges the data nicely, it wouldnt be a difficult addition but would be a nice one and allow layering of DMX data)
Impliment OSC feedback messages so touchosc buttons can change colour when a particular pattern is playing or recording - i think this is possible but havent looked into it yet.

have fun!
Lightsteed
