import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock

# Load KV files for the app layout
Builder.load_file('kv/splash.kv')
Builder.load_file('kv/main.kv')

# Load lessons from JSON file
def load_lessons():
    with open('data/lessons.json') as f:
        return json.load(f)

# Splash Screen that appears at the beginning
class SplashScreen(Screen):
    def on_enter(self):
        # Schedule to switch to home after 2 seconds
        Clock.schedule_once(self.go_to_home, 2)

    def go_to_home(self, dt):
        self.manager.current = 'home'

# Home Screen where subjects are displayed
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(Label(text='Welcome to the Educational App', font_size='20sp'))

        # Load subjects from the JSON file
        self.subjects = load_lessons()['subjects']

        for subject in self.subjects:
            btn = Button(text=subject['name'], size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn, subject=subject: self.go_to_lessons(subject))
            layout.add_widget(btn)

        self.add_widget(layout)

    def go_to_lessons(self, subject):
        # Switch to the lesson screen and pass the selected subject
        self.manager.current = 'lesson_screen'
        self.manager.get_screen('lesson_screen').display_lessons(subject)

# Lesson Screen that displays lessons for the selected subject
class LessonScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

    def display_lessons(self, subject):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text=f"Lessons for {subject['name']}", font_size='20sp'))

        for lesson in subject['lessons']:
            btn = Button(text=lesson['title'], size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn, lesson=lesson: self.show_lesson_content(lesson))
            self.layout.add_widget(btn)

    def show_lesson_content(self, lesson):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text=lesson['content'], font_size='18sp'))

# Main application class that initializes the screen manager
class EducationalApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))  # Add SplashScreen
        sm.add_widget(HomeScreen(name='home'))       # Add HomeScreen
        sm.add_widget(LessonScreen(name='lesson_screen'))  # Add LessonScreen
        sm.add_widget(LessonScreen(name='lessons'))  # Add LessonScreen for 'lessons'
        # sm.add_widget(SearchScreen(name='search'))  # Add SearchScreen if it exists
        return sm

# Run the application
if __name__ == '__main__':
    EducationalApp().run()
