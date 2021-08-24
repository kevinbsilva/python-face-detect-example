"""Module for parsing the arguments when executing the application."""
from argparse import ArgumentParser


class ArgParser:
    """Class for parsing the Arguments, using ArgumentParser
    library.
    """
    def __init__(self):
        self.ap = ArgumentParser()

        self.ap.add_argument(
            '-f', '--format', default='csv', type=str, help='Format of the output report'
        )
        self.ap.add_argument(
            "-v", "--video", default=0, help="Path to the video file. Webcam if none"
        )
        
        self.ap.add_argument(
            "-p", "--prototxt", required=True, help="Path to the prototxt file"
        )
        
        self.ap.add_argument(
            "-m", "--model", required=True, help="Path to the model file"
        )

        self.ap.add_argument(
            "-c",
            "--confidence",
            type=float,
            default=0.5,
            help="Minimum probability to filter weak detections",
        )

    def get_args(self):
        """Returns the parsed arguments.

        :return:
        """
        return vars(self.ap.parse_args())



