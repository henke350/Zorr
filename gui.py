import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

# Import the game logic class and data from our other file
from main import ZorrAI, TABLES

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.game = ZorrAI()
        self.init_ui()

    def init_ui(self):
        # --- Window Setup ---
        self.setWindowTitle("Deep IQ: The Wrath of Zorr")
        self.setMinimumSize(800, 600)
        self.setGeometry(100, 100, 900, 700)

        # A nice dark gradient background for the whole window
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2E3440, stop: 1 #4C566A
                );
            }
        """)

        # --- Fonts ---
        # Using a more modern font stack that's common on Windows/macOS
        self.font_header = QFont("Segoe UI Variable", 32, QFont.Bold)
        self.font_body = QFont("Segoe UI Variable", 24)
        self.font_special = QFont("Segoe UI Variable", 28, QFont.Bold)
        self.font_instructions = QFont("Segoe UI Variable", 14)
        self.font_symbol = QFont("Segoe UI Emoji", 24) # Font for the Unicode symbols

        # --- A central container frame for the HUD effect ---
        container_frame = QFrame()
        container_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(46, 52, 64, 0.85); /* Semi-transparent dark background */
                border-radius: 15px;
            }
        """)
        
        main_layout = QVBoxLayout(container_frame)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # --- Create Labels ---
        self.table_label = self.create_label("", self.font_header, "#ECEFF4", alignment=Qt.AlignCenter)

        # --- Roll Layout (Symbol + Text) ---
        roll_layout = QHBoxLayout()
        self.die_symbol_label = self.create_label("🎲", self.font_symbol, "#88C0D0")
        self.roll_label = self.create_label("", self.font_body, "#D8DEE9")
        roll_layout.addWidget(self.die_symbol_label)
        roll_layout.addWidget(self.roll_label, 1)

        self.result_label = self.create_label("", self.font_body, "#ECEFF4", word_wrap=True)

        # --- Visual Divider ---
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("background-color: #4C566A;")

        # --- Special Result Layout (Symbol + Text) ---
        extra_layout = QHBoxLayout()
        self.wrath_symbol_label = self.create_label("🔥", self.font_symbol, "#BF616A")
        self.extra_label = self.create_label("", self.font_body, "#EBCB8B", word_wrap=True)
        self.apply_glow_effect(self.extra_label, "#D08770")
        extra_layout.addWidget(self.wrath_symbol_label)
        extra_layout.addWidget(self.extra_label, 1)

        # --- Advancement Layout (Symbol + Text) ---
        advancement_layout = QHBoxLayout()
        self.advance_symbol_label = self.create_label("⬆️", self.font_symbol, "#A3BE8C")
        self.advancement_label = self.create_label("", self.font_special, "#A3BE8C")
        self.apply_glow_effect(self.advancement_label, "#A3BE8C")
        advancement_layout.addWidget(self.advance_symbol_label)
        advancement_layout.addWidget(self.advancement_label, 1)

        self.instructions_label = self.create_label(
            "Press SPACE to roll for Zorr's turn. Press ESC to quit.",
            self.font_instructions, "#81A1C1"
        )

        # --- Add all widgets and layouts to the main container ---
        main_layout.addWidget(self.table_label)
        main_layout.addLayout(roll_layout)
        main_layout.addWidget(self.result_label)
        main_layout.addSpacing(20)
        main_layout.addWidget(divider)
        main_layout.addSpacing(20)
        main_layout.addLayout(extra_layout)
        main_layout.addLayout(advancement_layout)
        main_layout.addStretch() # Pushes instructions to the bottom
        main_layout.addWidget(self.instructions_label, alignment=Qt.AlignCenter)

        # Set the main window layout to contain the frame, creating margins around it
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(20, 20, 20, 20)
        window_layout.addWidget(container_frame)
        
        self.update_display()
        self.show()

    def create_label(self, text, font, color, alignment=Qt.AlignLeft, word_wrap=False):
        """Helper function to create and style a QLabel."""
        label = QLabel(text)
        label.setFont(font)
        label.setStyleSheet(f"color: {color}; background: transparent;")
        label.setAlignment(alignment | Qt.AlignVCenter)
        if word_wrap:
            label.setWordWrap(True)
        return label

    def apply_glow_effect(self, widget, color_hex):
        """Applies a colored drop shadow effect to a widget to make it 'glow'."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(color_hex))
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 0)
        widget.setGraphicsEffect(shadow)

    def update_display(self, turn_data=None):
        """Updates all the labels and symbols with new information from the game logic."""
        if turn_data is None:
            # Initial state before the first roll
            self.table_label.setText(f"{TABLES[self.game.current_table_num]['name']}")
            self.roll_label.setText("Waiting for Zorr's turn...")
            self.result_label.setText("")
            self.extra_label.setText("")
            self.advancement_label.setText("")
            # Hide all optional symbols initially
            self.die_symbol_label.hide()
            self.wrath_symbol_label.hide()
            self.advance_symbol_label.hide()
        else:
            # Update text from turn data
            self.table_label.setText(f"{turn_data['table_name']}")
            self.roll_label.setText(f"Roll: {turn_data['roll']}")
            self.result_label.setText(f"Result: {turn_data['result']}")
            self.die_symbol_label.show() # Always show the die symbol on a turn

            # Handle the extra info (Wrath/Bonus)
            extra_text = turn_data['bonus_info'] or turn_data['wrath_info']
            if extra_text:
                self.extra_label.setText(extra_text)
                self.wrath_symbol_label.show()
            else:
                self.extra_label.setText("")
                self.wrath_symbol_label.hide()

            # Handle advancement info
            if turn_data['advancement_info']:
                self.advancement_label.setText(turn_data['advancement_info'])
                self.advance_symbol_label.show()
            else:
                self.advancement_label.setText("")
                self.advance_symbol_label.hide()

    def keyPressEvent(self, event):
        """Handle key presses for the window."""
        if event.key() == Qt.Key_Space:
            turn_results = self.game.play_zorr_turn()
            self.update_display(turn_results)
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())