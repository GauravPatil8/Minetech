from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from datetime import datetime
from kivy.uix.widget import Widget
import sounddevice as sd
import wave
import numpy as np
from fpdf import FPDF  # For PDF generation
import os

class ElitShiftLogApp(App):

    def build(self):
        # Set the background to a dark theme with elegant tones
        Window.clearcolor = (0.05, 0.05, 0.05, 1)  # Dark background

        # Main layout with padding for balanced appearance
        main_layout = BoxLayout(orientation='vertical', padding=40, spacing=25)

        # Header section with a centered title
        header_layout = AnchorLayout(anchor_x='center', anchor_y='top', size_hint=(1, 0.2))
        header_label = Label(text="[b]Shift Log[/b]", font_size=48, bold=True, markup=True, color=(1, 1, 1, 1))
        header_layout.add_widget(header_label)
        main_layout.add_widget(header_layout)

        # Date label beneath the header
        date_layout = AnchorLayout(anchor_x='center', anchor_y='top', size_hint=(1, 0.1))
        current_datetime = datetime.now().strftime("%d %B, %Y \n%H:%M:%S")
        date_label = Label(text=current_datetime, font_size=20, color=(0.6, 0.6, 0.6, 1))
        date_layout.add_widget(date_label)
        main_layout.add_widget(date_layout)

        # Recipient selection section
        self.to_spinner = Spinner(text='Shift In-charge', values=('Shift In-charge', 'Supervisor', 'Manager'),
                                  background_color=(0.15, 0.15, 0.15, 1), size_hint_x=0.75,
                                  color=(0.9, 0.9, 0.9, 1), font_size=18)
        to_layout = GridLayout(cols=2, size_hint=(1, 0.1), padding=[0, 5, 0, 5], spacing=10)
        to_label = Label(text="To:", font_size=22, color=(1, 1, 1, 1), halign='right')
        to_layout.add_widget(to_label)
        to_layout.add_widget(self.to_spinner)
        main_layout.add_widget(to_layout)

        # Audio recording section with perfect alignment of image and button
        record_layout = BoxLayout(orientation='horizontal', padding=[20, 0, 20, 0], spacing=15, size_hint=(1, 0.2))
        mic_image = Image(source=R'..\resources\mic_image.png', size_hint=(None, 1), size=(30, 30))  # Adjust image size
        record_button = Button(text="Record", size_hint=(0.6, 1), background_normal='',
                               background_color=(0.1, 0.6, 0.8, 1), font_size=20,
                               color=(1, 1, 1, 1), border=(30, 30, 30, 30))
        record_button.bind(on_press=self.start_recording)

        record_layout.add_widget(mic_image)
        record_layout.add_widget(record_button)
        main_layout.add_widget(record_layout)

        # Stop button with improved style
        stop_button = Button(text="Stop & Save", size_hint_y=0.15, background_normal='',
                             background_color=(0.87, 0.12, 0.12, 1), font_size=20,
                             color=(1, 1, 1, 1), border=(30, 30, 30, 30))
        stop_button.bind(on_press=self.stop_recording)
        main_layout.add_widget(stop_button)

        # Notes section with contrasting background for clarity
        self.note_input = TextInput(hint_text="Additional shift notes (optional)",
                                    size_hint_y=0.2, background_color=(0.2, 0.2, 0.2, 1),
                                    foreground_color=(1, 1, 1, 1), font_size=18,
                                    padding=(10, 10), cursor_color=(0.9, 0.9, 0.9, 1))
        main_layout.add_widget(self.note_input)

        # Button section for sending and generating report
        button_layout = BoxLayout(orientation='horizontal', padding=[20, 0, 20, 0], spacing=30, size_hint=(1, 0.2))

        # Send button with fresh green tone
        send_button = Button(text="Send", size_hint=(0.5, 0.8), background_normal='',
                             background_color=(0.18, 0.8, 0.4, 1), font_size=20,
                             color=(1, 1, 1, 1), border=(30, 30, 30, 30))
        button_layout.add_widget(send_button)

        # Generate report button with an accent blue tone
        report_button = Button(text="Generate Report", size_hint=(0.5, 0.8), background_normal='',
                               background_color=(0.15, 0.5, 0.85, 1), font_size=20,
                               color=(1, 1, 1, 1), border=(30, 30, 30, 30))
        report_button.bind(on_press=self.generate_report)
        button_layout.add_widget(report_button)

        main_layout.add_widget(button_layout)

        return main_layout

    def start_recording(self, instance):
        self.fs = 44100
        self.duration = 5  # Recording duration in seconds
        self.recording = True
        instance.text = "Recording..."  # Change button text during recording
        self.audio_data = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=2, dtype='int16')

    def stop_recording(self, instance):
        if self.recording:
            sd.wait()
            self.recording = False
            instance.text = "Record"  # Revert button text after stopping
            self.save_audio()

    def save_audio(self):
        file_name = "shift_recording.wav"
        path = os.path.join(os.getcwd(), file_name)
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes(np.array(self.audio_data).tobytes())
        print(f"Audio saved as {file_name}")

    def generate_report(self, instance):
        # Get the values from Spinner and TextInput
        recipient = self.to_spinner.text
        notes = self.note_input.text
        current_datetime = datetime.now().strftime("%d %B, %Y \n%H:%M:%S")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create instance of FPDF class
        pdf = FPDF()

        # Add a page and set up the document
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add content to the PDF
        pdf.cell(200, 10, txt="Shift Log Report", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Date: {current_datetime}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Recipient: {recipient}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Additional Notes: {notes}", ln=True, align='L')

        # Define file path
        file_name = f"shift_log_report_{timestamp}.pdf"
        file_path = os.path.join(os.getcwd(), file_name)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Output the PDF
        pdf.output(file_path)
        print(f"PDF saved at {file_path}")


if __name__ == "__main__":
    ElitShiftLogApp().run()
