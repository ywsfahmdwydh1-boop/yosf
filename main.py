from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.core.window import Window
import random
import json
import os

SAVE_FILE = "game_save.json"

DEFAULT_DATA = {
    "coins": 100,
    "games_played": 0,
    "games_won": 0
}

def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            for key, value in DEFAULT_DATA.items():
                if key not in data:
                    data[key] = value
            return data
        except Exception:
            pass
    return DEFAULT_DATA.copy()

GAME_DATA = load_data()

def save_data():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(GAME_DATA, file, ensure_ascii=False, indent=4)
    except Exception:
        pass

BG_COLOR = (0.06, 0.07, 0.12, 1)
BLUE_COLOR = (0.15, 0.35, 0.75, 1)
GREEN_COLOR = (0.10, 0.65, 0.30, 1)
RED_COLOR = (0.80, 0.15, 0.15, 1)
PURPLE_COLOR = (0.45, 0.20, 0.70, 1)
GOLD_COLOR = (0.90, 0.65, 0.10, 1)
TEXT_COLOR = (1, 1, 1, 1)

def style_button(button, color=BLUE_COLOR):
    button.background_normal = ""
    button.background_color = color
    button.color = TEXT_COLOR
    button.font_size = "18sp"

def make_label(text="", size=18):
    return Label(
        text=text,
        font_size=f"{size}sp",
        color=TEXT_COLOR,
        halign="center",
        valign="middle"
    )

def add_coins(amount):
    GAME_DATA["coins"] += amount
    save_data()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(12)
        )

        title = make_label("GUESS MASTER", 32)
        title.size_hint_y = 0.18

        self.coins_label = make_label("", 21)
        self.coins_label.size_hint_y = 0.10

        guess_button = Button(text="تخمين الرقم", size_hint_y=0.14)
        style_button(guess_button, GREEN_COLOR)

        with_me_button = Button(text="خمن معايا", size_hint_y=0.14)
        style_button(with_me_button, PURPLE_COLOR)

        xo_button = Button(text="لعبة XO", size_hint_y=0.14)
        style_button(xo_button, BLUE_COLOR)

        exit_button = Button(text="خروج", size_hint_y=0.12)
        style_button(exit_button, RED_COLOR)

        layout.add_widget(title)
        layout.add_widget(self.coins_label)
        layout.add_widget(guess_button)
        layout.add_widget(with_me_button)
        layout.add_widget(xo_button)
        layout.add_widget(exit_button)

        self.add_widget(layout)

        guess_button.bind(
            on_release=lambda x: setattr(self.manager, "current", "guess")
        )
        with_me_button.bind(
            on_release=lambda x: setattr(self.manager, "current", "with_me")
        )
        xo_button.bind(
            on_release=lambda x: setattr(self.manager, "current", "xo_menu")
        )
        exit_button.bind(
            on_release=lambda x: App.get_running_app().stop()
        )

    def on_pre_enter(self):
        self.coins_label.text = f"Coins: {GAME_DATA['coins']}"

class GuessScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.number = 0
        self.attempts = 0
        self.finished = False

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(10)
        )

        title = make_label("خمن الرقم من 1 إلى 100", 24)
        title.size_hint_y = 0.13

        self.coins_label = make_label("", 18)
        self.coins_label.size_hint_y = 0.08

        self.input = TextInput(
            hint_text="اكتب الرقم",
            multiline=False,
            input_filter="int",
            font_size="28sp",
            halign="center",
            size_hint_y=0.14
        )

        guess_button = Button(text="خمن", size_hint_y=0.13)
        style_button(guess_button, GREEN_COLOR)

        self.result = make_label("ابدأ التخمين!", 20)
        self.result.size_hint_y = 0.25

        new_button = Button(text="لعبة جديدة", size_hint_y=0.11)
        style_button(new_button)

        back_button = Button(text="الرئيسية", size_hint_y=0.10)
        style_button(back_button)

        layout.add_widget(title)
        layout.add_widget(self.coins_label)
        layout.add_widget(self.input)
        layout.add_widget(guess_button)
        layout.add_widget(self.result)
        layout.add_widget(new_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

        guess_button.bind(on_release=self.check_guess)
        new_button.bind(on_release=self.new_game)
        back_button.bind(
            on_release=lambda x: setattr(self.manager, "current", "main")
        )

        self.new_game()

    def on_pre_enter(self):
        self.coins_label.text = f"Coins: {GAME_DATA['coins']}"

    def new_game(self, *args):
        self.number = random.randint(1, 100)
        self.attempts = 0
        self.finished = False
        self.input.text = ""
        self.result.text = "ابدأ التخمين!"

    def check_guess(self, instance):
        if self.finished:
            return

        if not self.input.text:
            self.result.text = "اكتب رقمًا أولًا!"
            return

        guess = int(self.input.text)

        if guess < 1 or guess > 100:
            self.result.text = "الرقم من 1 إلى 100"
            return

        self.attempts += 1

        if guess == self.number:
            reward = max(5, 20 - self.attempts)
            add_coins(reward)
            self.finished = True
            self.result.text = (
                f"صح!\n"
                f"الرقم هو {self.number}\n"
                f"+{reward} Coins"
            )
        elif guess < self.number:
            self.result.text = "الرقم الصحيح أكبر"
        else:
            self.result.text = "الرقم الصحيح أصغر"

class XOMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(15)
        )

        title = make_label("اختر طريقة اللعب", 28)
        title.size_hint_y = 0.20

        computer_button = Button(text="ضد الكمبيوتر", size_hint_y=0.18)
        style_button(computer_button, PURPLE_COLOR)

        friend_button = Button(
            text="مع صديق على نفس الجهاز",
            size_hint_y=0.18
        )
        style_button(friend_button, BLUE_COLOR)

        back_button = Button(text="الرئيسية", size_hint_y=0.14)
        style_button(back_button)

        layout.add_widget(title)
        layout.add_widget(computer_button)
        layout.add_widget(friend_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

        computer_button.bind(on_release=lambda x: self.start_game("computer"))
        friend_button.bind(on_release=lambda x: self.start_game("friend"))
        back_button.bind(
            on_release=lambda x: setattr(self.manager, "current", "main")
        )

    def start_game(self, mode):
        game = self.manager.get_screen("xo")
        game.start_game(mode)
        self.manager.current = "xo"

class XOScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.board = [""] * 9
        self.player = "X"
        self.mode = "friend"
        self.buttons = []

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(8)
        )

        self.status = make_label("دور اللاعب X", 23)
        self.status.size_hint_y = 0.12

        grid = GridLayout(
            cols=3,
            rows=3,
            spacing=dp(5),
            size_hint_y=0.66
        )

        for index in range(9):
            button = Button(text="", font_size="40sp")
            style_button(button)
            button.bind(
                on_release=lambda btn, i=index: self.play(i)
            )
            self.buttons.append(button)
            grid.add_widget(button)

        restart_button = Button(text="إعادة اللعب", size_hint_y=0.10)
        style_button(restart_button)

        back_button = Button(text="رجوع", size_hint_y=0.10)
        style_button(back_button)

        layout.add_widget(self.status)
        layout.add_widget(grid)
        layout.add_widget(restart_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

        restart_button.bind(on_release=self.restart)
        back_button.bind(
            on_release=lambda x: setattr(self.manager, "current", "xo_menu")
        )

    def start_game(self, mode):
        self.mode = mode
        self.restart()

    def restart(self, *args):
        self.board = [""] * 9
        self.player = "X"

        for button in self.buttons:
            button.text = ""
            button.disabled = False

        if self.mode == "computer":
            self.status.text = "أنت X - دورك"
        else:
            self.status.text = "دور اللاعب X"

    def play(self, index):
        if self.board[index] != "":
            return

        if self.mode == "computer" and self.player != "X":
            return

        self.board[index] = self.player
        self.buttons[index].text = self.player

        winner = self.winner()

        if winner:
            self.finish(winner)
            return

        if "" not in self.board:
            self.finish("draw")
            return

        if self.mode == "computer":
            self.player = "O"
            self.status.text = "الكمبيوتر يفكر..."
            self.computer_move()
        else:
            self.player = "O" if self.player == "X" else "X"
            self.status.text = f"دور اللاعب {self.player}"

    def computer_move(self):
        empty = [
            i for i, value in enumerate(self.board)
            if value == ""
        ]

        if not empty:
            return

        for index in empty:
            self.board[index] = "O"
            if self.winner() == "O":
                self.buttons[index].text = "O"
                self.finish("O")
                return
            self.board[index] = ""

        for index in empty:
            self.board[index] = "X"
            if self.winner() == "X":
                self.board[index] = "O"
                self.buttons[index].text = "O"
                self.after_computer()
                return
            self.board[index] = ""

        index = random.choice(empty)
        self.board[index] = "O"
        self.buttons[index].text = "O"

        if self.winner() == "O":
            self.finish("O")
            return

        if "" not in self.board:
            self.finish("draw")
            return

        self.after_computer()

    def after_computer(self):
        self.player = "X"
        self.status.text = "دورك - X"

    def finish(self, result):
        for button in self.buttons:
            button.disabled = True

        if result == "draw":
            self.status.text = "تعادل!"
        elif result == "X":
            if self.mode == "computer":
                add_coins(10)
                self.status.text = "فزت! +10 Coins"
            else:
                self.status.text = "اللاعب X فاز!"
        else:
            if self.mode == "computer":
                self.status.text = "الكمبيوتر فاز!"
            else:
                self.status.text = "اللاعب O فاز!"

    def winner(self):
        lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6)
        ]

        for a, b, c in lines:
            if (
                self.board[a]
                and self.board[a] == self.board[b] == self.board[c]
            ):
                return self.board[a]

        return None

class GuessWithMeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.low = 1
        self.high = 100
        self.guess = 50
        self.rounds = 0
        self.finished = False

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(10)
        )

        title = make_label("خمن معايا", 28)
        title.size_hint_y = 0.12

        self.info = make_label("", 18)
        self.info.size_hint_y = 0.20

        self.question = make_label("", 25)
        self.question.size_hint_y = 0.15

        bigger_button = Button(text="الرقم أكبر", size_hint_y=0.12)
        style_button(bigger_button, BLUE_COLOR)

        smaller_button = Button(text="الرقم أصغر", size_hint_y=0.12)
        style_button(smaller_button, GOLD_COLOR)

        correct_button = Button(
            text="صح! خمنت الرقم",
            size_hint_y=0.12
        )
        style_button(correct_button, GREEN_COLOR)

        restart_button = Button(text="رقم جديد", size_hint_y=0.10)
        style_button(restart_button)

        back_button = Button(text="الرئيسية", size_hint_y=0.09)
        style_button(back_button)

        layout.add_widget(title)
        layout.add_widget(self.info)
        layout.add_widget(self.question)
        layout.add_widget(bigger_button)
        layout.add_widget(smaller_button)
        layout.add_widget(correct_button)
        layout.add_widget(restart_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

        bigger_button.bind(on_release=self.answer_bigger)
        smaller_button.bind(on_release=self.answer_smaller)
        correct_button.bind(on_release=self.answer_correct)
        restart_button.bind(on_release=self.new_game)
        back_button.bind(
            on_release=lambda x: setattr(self.manager, "current", "main")
        )

        self.new_game()

    def new_game(self, *args):
        self.low = 1
        self.high = 100
        self.rounds = 0
        self.finished = False
        self.make_guess()

    def make_guess(self):
        if self.low > self.high:
            self.question.text = "الإجابات متناقضة!"
            self.info.text = "سيتم إعادة طرح السؤال."
            self.finished = True
            return

        self.guess = (self.low + self.high) // 2
        self.rounds += 1

        self.info.text = (
            f"الأرقام المتبقية: {self.low} - {self.high}\n"
            f"السؤال رقم {self.rounds}"
        )

        self.question.text = f"هل رقمك هو {self.guess}؟"

    def answer_bigger(self, instance):
        if self.finished:
            return

        if self.guess >= self.high:
            self.invalid_answer()
            return

        self.low = self.guess + 1
        self.make_guess()

    def answer_smaller(self, instance):
        if self.finished:
            return

        if self.guess <= self.low:
            self.invalid_answer()
            return

        self.high = self.guess - 1
        self.make_guess()

    def answer_correct(self, instance):
        if self.finished:
            return

        self.finished = True
        reward = 10
        add_coins(reward)

        self.question.text = (
            f"عرفت رقمك!\n"
            f"رقمك هو {self.guess}"
        )

        self.info.text = f"حصلت على +{reward} Coins"

    def invalid_answer(self):
        popup_layout = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        message = make_label(
            "الإجابة غير صحيحة!\n\n"
            "الإجابة لا تتفق مع الأرقام المتبقية.\n\n"
            "سيتم إعادة طرح السؤال.",
            17
        )

        close_button = Button(
            text="تمام",
            size_hint_y=0.25
        )
        style_button(close_button, RED_COLOR)

        popup_layout.add_widget(message)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title="تنبيه",
            content=popup_layout,
            size_hint=(0.85, 0.55)
        )

        close_button.bind(on_release=popup.dismiss)
        popup.open()

class GuessMasterApp(App):
    def build(self):
        Window.clearcolor = BG_COLOR

        manager = ScreenManager()

        manager.add_widget(MainScreen(name="main"))
        manager.add_widget(GuessScreen(name="guess"))
        manager.add_widget(XOMenuScreen(name="xo_menu"))
        manager.add_widget(XOScreen(name="xo"))
        manager.add_widget(GuessWithMeScreen(name="with_me"))

        return manager

if __name__ == "__main__":
    GuessMasterApp().run()
