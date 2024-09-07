This repository contains MIDI Remote Scripts for using APC64's Custom Mode as a plugin manager for Ableton.

At this moment, functionality includes:
- Adding Effect to selected channel
- Adding Instruments to new channels

For this plugin to be working properly, place `mapping.txt` file under the following directory:
- Mac: `/Users/*your_username*/Ableton/Resources/mapping.txt`
- Windows: `C:\\Users\\*your_username*\\Ableton\\Resources\\mapping.txt`


# How to work with mapping.txt

`mapping.txt` defines which device is assigned to which button, and can be customized at any time
This file should contain lines in following format:

`Position, Device Name, Preset Name (optional)`
- `Position` is defined as a pair of numbers: `column:row`. For example, `1:1` is the top left pad, `8:1` is the top right pad, `1:2` is the first pad in the second row. *Only __first four rows__ are used*, the others are ignored.
- `Device Name` is a name of a desired device, as presented in Abletons browser, for example, `EQ Three`, `Compressor`, `Drum Rack`.
- `Preset Name` is a name of a desired preset for given device. Specifying it is __optional__, *but you __MUST__ put a __comma__ after `Device name` __in any case__*. If no `Preset Name` is given, device will load with what is your default preset for it.
- `mapping.txt` file in this repository is with my mappings :)

## Sample mapping.txt file:
```
1:1, EQ Three,
1:2, Compressor,
2:1, Saturator,
8:1, Drum Rack, 808 Core Kit 
8:2, Drum Rack, 606 Core Kit
```

# Future features
- Ableton browser navigation. Progress for it can be found on `browser` branch
