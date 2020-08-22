from unittest.mock import MagicMock, ANY
class BrythonMock(MagicMock):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg) 
        self.__le__ = MagicMock()
SPAN = BrythonMock()
document = BrythonMock()
timer = MagicMock()
window = MagicMock()
ajax = MagicMock()

