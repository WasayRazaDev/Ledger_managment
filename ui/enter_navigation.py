# ui/enter_navigation.py
from PyQt5.QtCore import Qt, QObject, QEvent, QTimer
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QAbstractSpinBox, QDateEdit, QTextEdit, QPlainTextEdit


class EnterNavigationManager(QObject):
    def __init__(self, parent_widget, rules=None):
        """
        rules: dict mapping 
            widget -> {
                "mode": "tab_only" | "activate_only" | "both",
                "next": widget_to_focus (optional)
            }
        """
        super().__init__(parent_widget)
        self.parent_widget = parent_widget
        self.rules = rules or {}

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter):
            focused = QApplication.focusWidget()
            if not focused:
                return False

            if not (self.parent_widget is focused or self.parent_widget.isAncestorOf(focused)):
                return False

            # Skip multiline editors
            if isinstance(focused, (QTextEdit, QPlainTextEdit)):
                return False

            rule = self.rules.get(focused, {})
            mode = rule.get("mode", "tab_only")
            custom_next = rule.get("next")

            def after():
                try:
                    # Move focus
                    if mode in ("tab_only", "both"):
                        if custom_next:
                            custom_next.setFocus()
                        else:
                            focused.focusNextChild()

                    # Trigger activation
                    if mode in ("activate_only", "both"):
                        if isinstance(focused, QPushButton):
                            focused.click()
                        elif isinstance(focused, QLineEdit):
                            focused.editingFinished.emit()
                        elif isinstance(focused, QAbstractSpinBox):
                            focused.interpretText()
                        elif isinstance(focused, QDateEdit):
                            focused.editingFinished.emit()
                        else:
                            focused.event(QEvent(QEvent.MouseButtonPress))
                except Exception as e:
                    print("EnterNavigation error:", e)

            QTimer.singleShot(0, after)
            return True

        return super().eventFilter(obj, event)
