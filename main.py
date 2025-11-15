# import sys
# from PyQt5.QtWidgets import QApplication
# from ui.mainwindow_ui import MainWindow

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     sys.exit(app.exec_())



import sys
from PyQt5.QtWidgets import QApplication
from ui.mainwindow_ui import MainWindow
import traceback

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        main_window = MainWindow()
        main_window.show()
    except Exception as e:
        print("❌ Error while creating MainWindow:")
        traceback.print_exc()
        sys.exit(1)
    sys.exit(app.exec_())