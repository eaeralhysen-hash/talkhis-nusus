from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from google import genai


class TalkhisNususApp(App):
    def build(self):
        root = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=8,
        )

        self.api_key = TextInput(
            hint_text="مفتاح Google AI Studio API",
            multiline=False,
            size_hint_y=None,
            height=90,
        )

        self.duration = TextInput(
            hint_text="المدة المطلوبة (mm:ss)",
            multiline=False,
            size_hint_y=None,
            height=90,
        )

        self.speed = TextInput(
            hint_text="سرعة القراءة (حرف/ثانية)",
            multiline=False,
            size_hint_y=None,
            height=90,
        )

        self.text = TextInput(
            hint_text="ألصق النص البولندي",
            multiline=True,
        )

        self.info = Label(
            size_hint_y=None,
            height=90,
        )

        self.result = TextInput(
            hint_text="النص المختصر",
            readonly=True,
            multiline=True,
        )

        btn = Button(
            text="تلخيص",
            size_hint_y=None,
            height=100,
        )

        btn.bind(on_press=self.run_shorten)

        root.add_widget(self.api_key)
        root.add_widget(self.duration)
        root.add_widget(self.speed)
        root.add_widget(self.text)
        root.add_widget(btn)
        root.add_widget(self.info)
        root.add_widget(self.result)

        return root

    def target_chars(self, chars_per_second, mm_ss):
        minutes, seconds = map(int, mm_ss.split(":"))
        total_seconds = minutes * 60 + seconds
        return round(total_seconds * chars_per_second)

    def run_shorten(self, instance):
        try:
            api_key = self.api_key.text.strip()
            duration = self.duration.text.strip()
            speed = float(self.speed.text.strip())
            text = self.text.text.strip()

            client = genai.Client(api_key=api_key)

            target = self.target_chars(speed, duration)

            prompt = f"""
Skróć poniższy tekst po polsku.

Wymagania:
- Około {target} znaków łącznie ze spacjami.
- Zachowaj wszystkie główne idee.
- Zachowaj kolejność wydarzeń.
- Styl naturalny do TTS.
- Nie dodawaj nowych informacji.
- Nie przekraczaj limitu znaków.

Tekst:
{text}
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            result = response.text.strip()

            self.info.text = (
                f"الهدف: {target} | "
                f"الأصلي: {len(text)} | "
                f"الناتج: {len(result)}"
            )

            self.result.text = result

        except Exception as e:
            self.info.text = f"خطأ: {str(e)}"


if __name__ == "__main__":
    TalkhisNususApp().run()
