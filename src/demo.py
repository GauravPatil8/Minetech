from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
import sounddevice as sd
import wave
import numpy as np
import os

class ShiftLogApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        header_layout = BoxLayout(orientation='vertical', size_hint_y=0.2)
        header_label = Label(text="Shift Log", font_size=30, halign='center', size_hint=(1, 0.5))
        date_label = Label(text="30 August, 2024", font_size=20, halign='center', size_hint=(1, 0.5))
        header_layout.add_widget(header_label)
        header_layout.add_widget(date_label)
        layout.add_widget(header_layout)

        to_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        to_label = Label(text="To:", font_size=18, size_hint=(0.2, 1))
        to_spinner = Spinner(text='Shift In-charge', values=('Shift In-charge', 'Supervisor', 'Manager'),
                             size_hint=(0.8, 1))
        to_layout.add_widget(to_label)
        to_layout.add_widget(to_spinner)
        layout.add_widget(to_layout)

        record_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=10)
        mic_icon = Image(source=R'..\resources\mic_image.png', size_hint=(None, 1), size=(30, 30))
        self.record_button = Button(size_hint=(1, 1), background_normal='', background_color=(0.1, 0.6, 1, 1), text="Record")
        self.record_button.bind(on_press=self.start_recording)
        record_layout.add_widget(mic_icon)
        record_layout.add_widget(self.record_button)
        layout.add_widget(record_layout)

        self.stop_button = Button(text="Stop and Save", size_hint_y=0.1, background_color=(0.9, 0.3, 0.3, 1))
        self.stop_button.bind(on_press=self.stop_recording)
        layout.add_widget(self.stop_button)

        note_input = TextInput(hint_text="Write about shift if preferred", size_hint_y=0.2)
        layout.add_widget(note_input)

        send_button = Button(text="Send", size_hint_y=0.1, background_color=(0.1, 0.6, 1, 1))
        layout.add_widget(send_button)

        report_button = Button(text="Generate Report", size_hint_y=0.1, background_color=(0.5, 0.8, 0.2, 1))
        report_button.bind(on_press=self.generate_report)
        layout.add_widget(report_button)

        return layout

    def start_recording(self, instance):
        self.fs = 44100  
        self.duration = 5  
        self.recording = True
        self.record_button.text = "Recording..."
        self.audio_data = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=2, dtype='int16')

    def stop_recording(self, instance):
        if self.recording:
            sd.wait()  
            self.recording = False
            self.record_button.text = "Record"
            self.save_audio()

    def save_audio(self):
        file_name = "recording.wav"
        path = os.path.join(os.getcwd(), file_name)  
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(2)  
            wf.setsampwidth(2)  
            wf.setframerate(self.fs)
            wf.writeframes(np.array(self.audio_data).tobytes())
        print(f"Audio saved as {file_name}")

    def generate_report(self, instance):
        print("Report generated!")

if __name__ == "__main__":
    ShiftLogApp().run()
