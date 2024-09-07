# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.10.0 (default, Feb  4 2024, 05:25:13) [GCC 8.5.0 20210514 (Red Hat 8.5.0-20)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\elements.py
# Compiled at: 2023-08-04 18:30:20
# Size of source mod 2**32: 6147 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.control_surface import MIDI_NOTE_TYPE, ElementsBase, create_matrix_identifiers
from ableton.v3.control_surface.display import Text
from ableton.v3.control_surface.elements import ButtonElement
from . import midi

class TrackColorElement(ButtonElement):

    def reset(self):
        pass
    

class Elements(ElementsBase):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        add_button = partial((self.add_button),
          msg_type=MIDI_NOTE_TYPE,
          led_channel=(midi.FULL_BRIGHTNESS_LED_CHANNEL))
        add_modifier_button = partial((self.add_modifier_button),
          msg_type=MIDI_NOTE_TYPE,
          led_channel=(midi.FULL_BRIGHTNESS_LED_CHANNEL))
        add_button_matrix = partial((self.add_button_matrix),
          msg_type=MIDI_NOTE_TYPE,
          led_channel=(midi.FULL_BRIGHTNESS_LED_CHANNEL))
        add_button_matrix(create_matrix_identifiers(24, 87, width=8, flip_rows=True),
          'Pads',
          channels=(midi.FULL_BRIGHTNESS_LED_CHANNEL))
        self.add_sysex_element((midi.make_message(midi.SET_DISPLAY_OWNER_ID, 0)[:-2]),
          'Display_Ownership_Command',
          (lambda v: midi.make_message(midi.SET_DISPLAY_OWNER_ID, v)
),
          optimized=True,
          use_first_byte_as_value=True)

        def generate_display_message(index, text):
            return (midi.make_message)(midi.DISPLAY_MESSAGE_ID, index, *text + (0, ))

        for i in range(3):
            self.add_sysex_display_line((midi.make_message(midi.DISPLAY_MESSAGE_ID, i)[:-1]),
              ('Display_Line_{}'.format(i + 1)),
              (partial(generate_display_message, i)),
              default_formatting=Text(max_width=8,
              justification=(Text.Justification.CENTER)))