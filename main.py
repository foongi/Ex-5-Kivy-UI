import os

# os.environ['DISPLAY'] = ":0.0"
# os.environ['KIVY_WINDOW'] = 'egl_rpi'

import pygame
pygame.init()

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from pidev.Joystick import Joystick
from kivy.animation import Animation

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.clock import Clock

from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'

joy = Joystick(0, False)


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """


    animation = Animation(pos=(100, 100), t='out_bounce')

    def updateJoy(self, dt):


        self.ids["x_label"].text = str(joy.get_axis("x"))
        self.ids["y_label"].text = str(-1 * joy.get_axis("y"))
        self.ids["x_label"].x = self.width * joy.get_axis("x")
        self.ids["y_label"].y = -1 * self.height * joy.get_axis("y")


    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_interval(self.updateJoy, .1)
        self.text = None

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        self.ids.test3.text = "str(joy.get_button_state(3))"

    def animate(self):

        animation = Animation(pos=(100, 100), t='out_bounce')
        animation += Animation(pos=(0, 0), t='out_bounce')

        animation.start(self)

    def toggle_text(self):
        if self.ids.test3.active:
            self.ids.test3.text = "Jesus"
            self.ids.test3.active = False
        else:
            self.ids.test3.text = "Christ"
            self.ids.test3.active = True

    def go_Joystick(self):

        self.parent.current = "JoystickScreen"

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(
            ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(
            MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)


class JoystickScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        Builder.load_file('JoystickScreen.kv')

        super(JoystickScreen, self).__init__(**kwargs)

    def animate(self):
        animation = Animation(pos=(100, 100), t='out_bounce')
        animation += Animation(pos=(0, 0), t='out_bounce')

        animation.start(self)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = "main"

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(JoystickScreen(name="JoystickScreen"))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
