# XAda

## What is it?

XAda is a custom Ada syntax highlighter written for GNAT Studio. It extends the default highlighting by adding additional styles for types, constants, exceptions, attributes, enumerations, packages, member/global variables, pragmas and even operators.

The result of this is a much more colourful editor, which may (or may not) enhance readability. See for yourself!

![Preview 1 / 3](examples/1.png?raw=true)

![Preview 2 / 3](examples/2.png?raw=true)

![Preview 3 / 3](examples/3.png?raw=true)

## How do I install it?

***NOTE:*** *This plugin requires GNAT Studio 2018 (or newer) to function properly!*

Copy:

- the file `xada_highlighter.py`
- the folder `xada_lib`

into your plug-ins folder (e.g. `C:\Users\YOUR_USERNAME\.gps\plug-ins\`).

Upon restarting GNAT Studio, the plugin should be loaded and running.

## Caveats

Because of how it is written, this plugin overwrites the native Ada highlighting. As a result, a good chunk of it aims to recreate the original highlighting functionality, but does not fully cover it. Most things work, but you will almost certainly encounter issues with it (pre- and post-conditions, for example, are not supported).

In order to fix these issues, the current highlighting engine implementation (or at the very least, parts thereof) would need to be rewritten to allow for overlapping additions rather than requiring a complete handler. Until this day comes, these issues will most likely not be addressed.

## Disclaimer

The files located inside `xada_lib` are (slightly) modified versions of the ones shipped with [GNAT Studio](https://github.com/AdaCore/gps/blob/master/share/support/languages/highlighter/). As such, they fall under the same license as their original counterparts.

The Software is distributed without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. The Software is not an official addon or tool. Use of the Software (in whole or in part) is entirely at your own risk.
