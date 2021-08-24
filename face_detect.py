"""Main module for executing the face detection."""
import cv2
import imutils
import numpy as np

from arg_parser import ArgParser
from cv2 import dnn_Net
from logger import Logger
from report import Report


class FaceDetect:
    """
    Main class for detecting face from Video
    Frames, using the opencv library.
    """
    def __init__(self):
        self.log = Logger()

        self.timestamps = list()
        self.boxes = list()

        self.ap = ArgParser()
        self.args = self.ap.get_args()

        self.log.log('Parsing arguments. Following arguments where found.', level='d')
        self.log.log(f'Arguments parsed: {self.args}', level='d')

        self.net = self.__load_model()

    def __load_model(self) -> dnn_Net:
        """Loads the model file.
        :return: net object.
        """
        self.log.log(
            f'Loading model from file {self.args["model"]} and {self.args["prototxt"]}'
        )
        return cv2.dnn.readNetFromCaffe(self.args['prototxt'], self.args['model'])

    def __exit(self, key) -> bool:
        """
        Check if the key for quitting the application
        was pressed.

        :param key: keyboard key that was pressed.
        """
        if key == ord('q'):
            self.log.log('Exit key pressed. Quitting detection.')
            return True

    def face_detection(self) -> None:
        """Executes the detection.
        :return:
        """
        if self.args["video"] == 0:
            self.log.log("Loading video from webcam.")
        else:
            self.log.log(f"Loading video from file {self.args['video']}.")

        vs = cv2.VideoCapture(self.args["video"])

        fps = vs.get(cv2.CAP_PROP_FPS)
        self.log.log(f"Video loaded with {round(fps,0)} fps.", level="d")

        self.timestamps = [vs.get(cv2.CAP_PROP_POS_MSEC)]

        while vs.isOpened():
            vs.grab()
            ret, frame = vs.retrieve()

            try:
                frame = imutils.resize(frame, width=400)
            except AttributeError:
                break

            (h, w) = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(
                cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
            )

            self.net.setInput(blob)
            detections = self.net.forward()

            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence < self.args["confidence"]:
                    continue

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                self.boxes.append(box)
                self.timestamps.append(
                    [vs.get(cv2.CAP_PROP_POS_MSEC), confidence, True]
                )

                if self.boxes[-1].all() == box.all():
                    pass
                else:
                    self.timestamps.append(vs.get(cv2.CAP_PROP_POS_MSEC))
                    self.boxes.append(box)

                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(
                    frame,
                    text,
                    (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    (0, 0, 255),
                    2,
                )

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)

            if self.__exit(key):
                break

        cv2.destroyAllWindows()
        self.log.log("Closing video frames.")

        if self.args['video'] != 0:
            report = Report(timestamps=self.timestamps, fmt=self.args['format'])
            report.generate_report()

            self.log.log("Saving CSV containing all the face detections found.")


def main():
    fd = FaceDetect()
    fd.face_detection()


if __name__ == '__main__':
    main()
