import Live
from ableton.v2.control_surface.components.view_control import ViewControlComponent
from ableton.v3.control_surface.component import Component
from ableton.v3.control_surface.controls.button import ButtonControl
from ableton.v3.control_surface.display.renderable import Renderable
from .colors import Rgb
NavDirection = Live.Application.Application.View.NavDirection

class BrowserNavigationComponent(Component, Renderable):
    button_up = ButtonControl(color=None)
    button_down = ButtonControl(color=Rgb.RED_PULSE)
    button_left = ButtonControl()
    button_right = ButtonControl()
    button_select = ButtonControl()
    button_effects = ButtonControl()
    button_drums = ButtonControl()
    button_samples = ButtonControl()
    button_hotswap_mode = ButtonControl()

    def __init__(self, *a, **k):
        super(BrowserNavigationComponent, self).__init__(*a, **k)
        self._application = Live.Application.get_application()

    @button_effects.pressed
    def on_button_effects_pressed(self, button):
        self.toggle_browser()

    def toggle_browser(self):
        view = self._application.view
        if not (view.is_view_visible('Browser')):
            view.focus_view('Browser')
        else:
            view.hide_view('Browser')

    @button_drums.pressed
    def on_button_drums_pressed(self, button):
        pass

    @button_samples.pressed
    def on_button_samples_pressed(self, button):
        pass

    @button_up.pressed
    def on_button_up_pressed(self, button):
        self._navigate_browser(NavDirection.up)

    @button_down.pressed
    def on_button_down_pressed(self, button):
        self._navigate_browser(NavDirection.down)

    @button_left.pressed
    def on_button_up_pressed(self, button):
        self._navigate_browser(NavDirection.left)

    @button_right.pressed
    def on_button_down_pressed(self, button):
        self._navigate_browser(NavDirection.right)

    def _navigate_browser(self, direction):
        view = self._application.view
        if not (view.is_view_visible('Browser')):
            view.focus_view('Browser')
        else:
            view.scroll_view(direction, 'Browser', False)

    def _set_browser_filter(self, filter):
        self._application.browser.filter_type = filter

    def _clear_browser_filter(self):
        self._application.browser.filter_type = None

    @button_select.pressed
    def on_button_select_pressed(self, button):
        #self._preview_selected_item()
        pass

    @button_select.double_clicked
    def on_button_select_pressed(self, button):
        #self._preview_selected_item()
        pass
        