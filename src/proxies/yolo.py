import threading
from ultralytics import YOLO

class YOLOModelProxy:
    _model_instance = None
    _lock = threading.Lock()
    
    @classmethod
    def get_model(cls):
        if cls._model_instance is None:
            with cls._lock:
                if cls._model_instance is None:
                    cls._model_instance = YOLO("vehicle-plate-recognition.pt")
        return cls._model_instance