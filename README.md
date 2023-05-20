# raspberrypi-athan-clock

This allows your Raspberry Pi 4 device to show the clock with an Athan clock so you can stay up to date on the upcoming prayer times

Requirements:
- Unicorn HAT Mini https://shop.pimoroni.com/en-us/products/unicorn-hat-mini

Set your internal clock in your Raspberry Pi to your local time and update the GPS coordinates in your main.py file to a location close enough for you. 

See an example of this: https://github.com/theCaravan/raspberrypi-athan-clock/blob/master/20230513_080354.jpg

The clock is displayed vertically, i.e. where most of the LEDs are positioned from top to bottom, as this allows the best use of the LEDs offered by the Unicorn HAT Mini, where the remaining bottom portion is a color snake showing how much is left until the next prayer time. 

The Unicorn Hat Mini comes with 4 buttons, all functional with this program. 

- Press the upper left button once to show the next prayer time. Press it again to return to the clock.
- Press the upper right button once to show the hijri date in the MM/DD format, such that 01 is Muharram, 09 is Ramadan, 12 is Dhul Hijjah. Press it again to return to the clock.
- Press the lower left button once to clear the prayer color snake until the next prayer time. It will automatically return at the next prayer time. Press it again to show the snake again. Note that the color snake will not show between Sunrise and Dhuhr
- Press the lower right button once to clear the clock screen, allowing you to turn off the LEDs without turning off the device. Press it again to return to the clock

Known Issues:
- When pressing one of the buttons before the drawing of the time or date finishes, the screen will stop at that point. You can remedy this by pressing the button again. 
