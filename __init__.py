from __future__ import absolute_import, print_function, unicode_literals

import json
import os
import sys
from functools import partial

import Live
from ableton.v2.control_surface.layer import Layer
from ableton.v2.control_surface.midi import CC_STATUS
from ableton.v3.control_surface import (
    MIDI_NOTE_TYPE,
    ControlSurface,
    ControlSurfaceSpecification,
)
from ableton.v3.control_surface.capabilities import (
    CONTROLLER_ID_KEY,
    HIDDEN,
    NOTES_CC,
    PORTS_KEY,
    SCRIPT,
    SYNC,
    controller_id,
    inport,
    outport,
)
from ableton.v3.control_surface.elements_base import (
    ElementsBase,
    create_matrix_identifiers,
)
from ableton.v3.live.util import song

from . import midi
from .browser import BrowserNavigationComponent
from .colors import Rgb


def get_capabilities():
    return {
        CONTROLLER_ID_KEY: controller_id(
            vendor_id=2536, product_ids=[83], model_name=["APC64_"]
        ),
        PORTS_KEY: [
            inport(props=[NOTES_CC, SCRIPT, HIDDEN]),
            outport(
                props=[NOTES_CC, SCRIPT, HIDDEN]
            ),  # TODO remove later, leave only in
            outport(props=[SYNC]),
        ],
    }


def create_instance(c_instance):
    return APC64Plugins(c_instance=c_instance)


def read_file_to_dict(file_path):
    mappings = {}
    home_dir = os.path.expanduser("~")
    file_path = os.path.join(home_dir, "Ableton/Resources/mappings.txt")
    sys.stderr.write(str(file_path))

    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(",")

            # Extract and convert the coordinate
            coordinate_str = parts[0].strip().split(":")
            column, row = int(coordinate_str[0]), int(coordinate_str[1])
            if row < 5:
                value = coordinate_to_value(column, row)

                device_name = parts[1].strip()
                preset_name = parts[2].strip()

                # Add to the dictionary
                mappings[value] = (device_name, preset_name)

    sys.stderr.write(json.dumps(mappings, indent=4))

    return mappings


def coordinate_to_value(column, row):
    base_value = 24
    value = base_value + (column - 1) + (8 - row) * 8
    return value


class Elements(ElementsBase):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        add_button_matrix = partial(
            self.add_button_matrix,
            msg_type=MIDI_NOTE_TYPE,
            led_channel=(midi.FULL_BRIGHTNESS_LED_CHANNEL),
        )
        add_button_matrix(
            create_matrix_identifiers(56, 88, width=8, flip_rows=True), "Pads"
        )
        add_button = partial(
            (self.add_button),
            msg_type=MIDI_NOTE_TYPE,
            led_channel=(midi.FULL_BRIGHTNESS_LED_CHANNEL),
        )
        add_button(41, "Button_Up")
        add_button(25, "Button_Down")
        add_button(32, "Button_Left")
        add_button(34, "Button_Right")
        add_button(33, "Button_Select")
        add_button(48, "Button_Effects")
        add_button(49, "Button_Drums")
        add_button(50, "Button_Samples")
        add_button(40, "Button_Hotswap_Mode")


class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    identity_response_id_bytes = (71, 83, 0, 25)


class APC64Plugins(ControlSurface):
    def __init__(self, *a, **k):
        (super().__init__)(Specification, *a, **k)

    def _create_components(self):
        #elements = self.elements  # Get elements instance
        #browser_navigation = BrowserNavigationComponent()
        #browser_navigation.layer = Layer(
        #    button_up=elements.button_up,
        #    button_down=elements.button_down,
        #    button_left=elements.button_left,
        #    button_right=elements.button_right,
        #    button_select=elements.button_select,
        #    button_effects=elements.button_effects,
        #    button_drums=elements.button_drums,
        #    button_samples=elements.button_samples,
        #    button_hotswap_mode=elements.button_hotswap_mode,
        #    priority=4,  # Set layer priority
        #)
        #browser_navigation.layer.set_enabled = True

        # Add the component to ensure it is managed properly
        self._pads = getattr(self.elements, "pads_raw", None)
        if self._pads:
            self._initialize_listeners()

    def _initialize_listeners(self):
        for button in self._pads:
            if button:
                button.add_value_listener(
                    lambda value, b=button: self._on_pad_pressed(value, b)
                )

    def _initialize_mfxpads(self):
        sys.stderr.write("mfx init")
        for button in self._mfxpads:
            if button:
                button.add_value_listener(
                    lambda value, b=button: self._on_mfxpad_pressed(value, b)
                )

    def _on_pad_pressed(self, value, button):
        if value > 0:
            note_value = button.message_identifier()
            plugin_data = self._device_mapping.get(note_value)
            if plugin_data:
                plugin_name, preset_name = plugin_data
                self._add_plugin_to_selected_track(plugin_name, preset_name)
                button.send_midi((CC_STATUS, 0, Rgb.GREY.midi_value))

    def disconnect(self):
        super().disconnect()

    def setup(self):
        self._device_mapping = read_file_to_dict("mapping.txt")
        super().setup()
        with self.component_guard():
            self._create_components()

    def _add_plugin_to_selected_track(self, device_name, preset_name):
        browser = Live.Application.get_application().browser
        browser_item = self._find_device_in_browser(browser, device_name)
        if browser_item:
            if self._is_instrument(browser_item):
                track = song().create_midi_track(-1)
                browser_item = self._add_device_to_track(browser_item, track)
            else:
                browser_item = self._add_device_to_track(
                    browser_item, song().view.selected_track
                )
            if browser_item and preset_name:
                self._load_preset(device_name, preset_name)

    def _add_device_to_track(self, device, track):
        song().view.selected_track = track
        browser = Live.Application.get_application().browser
        if device:
            browser.load_item(device)
            return track.devices[-1]

    def _load_preset(self, device, preset_name):
        browser = Live.Application.get_application().browser
        preset_item = self._find_preset_in_browser(browser, preset_name)
        if preset_item:
            browser.load_item(preset_item)
        else:
            sys.stderr.write(f"Preset '{preset_name}' not found for device '{device}'")

    def _find_preset_in_browser(self, browser, preset_name):
        for category in [browser.instruments, browser.drums, browser.audio_effects]:
            for item in category.iter_children:
                if preset_name in item.name:
                    return item
        return None

    def _find_device_in_browser(self, browser, device_name):
        instrument_device = self._find_in_category(browser.instruments, device_name)
        if instrument_device:
            return instrument_device
        drum_device = self._find_in_category(browser.drums, device_name)
        if drum_device:
            return drum_device
        effect_device = self._find_in_category(browser.audio_effects, device_name)
        if effect_device:
            return effect_device
        sys.stderr.write(f"Device '{device_name}' not found in browser")
        return None

    def _find_in_category(self, category, device_name):
        for item in category.iter_children:
            if item.name == device_name:
                return item
        return None

    def _is_instrument(self, browser_item):
        instrument_keywords = ["query:synths", "query:drums", "query:instruments"]
        if any(keyword in browser_item.uri.lower() for keyword in instrument_keywords):
            return True
        return False
