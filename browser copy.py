import Live
from _Framework import ButtonElement
from ableton.v2.control_surface import MIDI_NOTE_TYPE
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface import Component

class BrowserNavigationComponent(Component):

    def __init__(self, parent):
        self._parent = parent
        self._application = Live.Application.get_application()
        self._presets_expanded = False
        self._hotswap_mode = False

        self._button_up = None #41
        self._button_down = None 
        self._button_left = None
        self._button_right = None
        self._button_select = None
        self._button_effects = None
        self._button_drums = None
        self._button_samples = None
        self._button_hotswap_mode = None #40

    def select_sample_browser(self, value):
        if value:
            self._set_browser_category('samples')

    def select_drum_rack_browser(self, value):
        if value:
            self._set_browser_category('drum_racks')

    def select_audio_effect_browser(self, value):
        if value:
            self._set_browser_category('audio_effects')

    def scroll_up(self, value):
        if value:
            self._application.browser.scroll(Live.Browser.ScrollDirection.up)

    def scroll_down(self, value):
        if value:
            self._application.browser.scroll(Live.Browser.ScrollDirection.down)

    def toggle_presets(self, value):
        if value:
            if self._presets_expanded:
                self._application.browser.load_next(-1)  # Collapse presets
            else:
                self._application.browser.load_next(1)  # Expand presets
            self._presets_expanded = not self._presets_expanded

    def insert_selected(self, value):
        if value:
            if self._hotswap_mode:
                self._application.browser.hotswap_target = Live.Browser.HotswapTarget.none
                self._application.browser.load_item(Live.Browser.ItemType.device)
            else:
                self._application.browser.load_item(Live.Browser.ItemType.device)

    def toggle_hotswap_mode(self, value):
        if value:
            self._hotswap_mode = not self._hotswap_mode
            if self._hotswap_mode:
                self.show_message("Hotswap Mode: ON")
            else:
                self.show_message("Hotswap Mode: OFF")

    def show_message(self, message):
        self._application.show_message(message)

    def _set_browser_category(self, category):
        browser = self._application.browser
        items = browser.category_items
        for item in items:
            if item.name.lower() == category.lower():
                browser.load_item(item)
                break

    def set_button_up(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if self._button_up != button:
            if self._button_up != None:
                self._button_up.remove_value_listener(self.scroll_up)
            self._button_up = button
            if (self._button_up != None):
                self._button_up.add_value_listener(self.scroll_up)

    def set_button_down(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if self._button_down != button:
            if self._button_down != None:
                self._button_down.remove_value_listener(self.scroll_down)
            self._button_down = button
            if (self._button_down != None):
                self._button_down.add_value_listener(self.scroll_down)
    
    def set_button_right(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if self._button_right != button:
            if self._button_right != None:
                self._button_right.remove_value_listener(self.scroll_right)
            self._button_right = button
            if (self._button_right != None):
                self._button_right.add_value_listener(self.scroll_right)
    
    def set_button_left(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if self._button_left != button:
            if self._button_left != None:
                self._button_left.remove_value_listener(self.scroll_left)
            self._button_left = button
            if (self._button_left != None):
                self._button_left.add_value_listener(self.scroll_left)

    def set_button_select(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if self._button_select != button:
            if self._button_select != None:
                self._button_select.remove_value_listener(self.insert_selected)
            self._button_select = button
            if (self._button_select != None):
                self._button_select.add_value_listener(self.insert_selected)

    def set_button_hotswap_mode(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if self._button_hotswap_mode != button:
            if self._button_hotswap_mode != None:
                self._button_hotswap_mode.remove_value_listener(self.toggle_hotswap_mode)
            self._button_hotswap_mode = button
            if (self._button_hotswap_mode != None):
                self._button_hotswap_mode.add_value_listener(self.toggle_hotswap_mode)

    def set_button_drums(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if self._button_drums != button:
            if self._button_drums != None:
                self._button_drums.remove_value_listener(self.select_drum_rack_browser)
            self._button_drums = button
            if (self._button_drums != None):
                self._button_drums.add_value_listener(self.select_drum_rack_browser)

    def set_button_effects(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if self._button_effects != button:
            if self._button_effects != None:
                self._button_effects.remove_value_listener(self.select_audio_effect_browser)
            self._button_effects = button
            if (self._button_effects != None):
                self._button_effects.add_value_listener(self.select_audio_effect_browser)

    def set_button_samples(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if self._button_samples != button:
            if self._button_samples != None:
                self._button_samples.remove_value_listener(self.select_sample_browser)
            self._button_samples = button
            if (self._button_samples != None):
                self._button_samples.add_value_listener(self.select_sample_browser)