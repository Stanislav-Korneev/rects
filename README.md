# Rect Project

## General info
* Project uses PyQt6 6.2.0
* You can change project settings, such as window size, available rect colors and many others, by changing **config.json**.
* You can add connections between rects by using rect central button.
  1. Click on rects central button.
  2. Click on central button of rect you want to connect to.
* You can delete connections by repeating the same algorithm but between rects that have already been connected.
* When the rect is ready to connect or disconnect, its central button changes its color.
* If you click somewhere outside any rect, the connection/disconnection process will be aborted.
* But worry not! If you miss the button and land your click somewhere on the rect, the process will be safe, and you can ~~fullfill your destiny~~ end your operation.

## ~~Difficult~~ code decisions:
* I used camelCase instead of snake_case, so variables and method names would be accordance with PyQt library
* I limited random rect colors to a list instead of generating completely random colors, so that interface would look better
 