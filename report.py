"""Module responsible for creating the Pandas report."""
import os
import pandas as pd

from datetime import datetime
from datetime import timedelta


class Report:
    """
    Class to generate the Pandas report for the
    face detection that was executed.

    It is responsible for building the report strcuture
    and saving as a file format. The default is CSV.
    """

    def __init__(self, timestamps: list, fmt: str = "csv"):
        self.__create_report_dir()
        self.timestamps = timestamps
        self.__build_dataframe()
        self.fmt = fmt

    def __build_dataframe(self) -> None:
        """Instantiate a new DataFrame."""
        self.dataframe = pd.DataFrame(columns=["timestamp", "confidence", "face"])

    def __get_saving_table(self) -> dict[callable]:
        """Get the dictionary containing all
        the available formats to generate the report.

        :returns: dict with the save methods.
        """
        return {
            "csv": [self.dataframe.to_csv],
            "xlsx": [self.dataframe.to_excel],
            "json": [self.dataframe.to_json, 'index'],
        }

    @staticmethod
    def __create_report_dir() -> None:
        """Create the report directory to store the output file.
        :return:
        """
        if not os.path.exists(os.path.join(os.getcwd(), "reports")):
            os.mkdir(os.path.join(os.getcwd(), "reports"))

    def __save_dataframe(self) -> None:
        """Save the DataFrame as the given format.
        :return:
        """
        if len(self.__get_saving_table()[self.fmt]) == 1:
            self.__get_saving_table()[self.fmt][0](
                f'{os.getcwd()}/reports/face_detection_{datetime.now().strftime("%Y%m%d")}.{self.fmt}'
            )

        else:
            self.__get_saving_table()[self.fmt][0](
                f'{os.getcwd()}/reports/face_detection_{datetime.now().strftime("%Y%m%d")}.{self.fmt}',
                orient=self.__get_saving_table()[self.fmt][-1],
            )

    def __populate_dataframe(self) -> None:
        """Populate the DataFrame with the list of
        timestamps generated.
        :return:
        """

        values = dict()

        values["timestamp"] = list()
        values["confidence"] = list()
        values["face"] = list()

        for ts in self.timestamps:

            try:
                values["timestamp"].append(str(timedelta(milliseconds=ts[0])))
                values["confidence"].append(ts[1])
                values["face"].append(ts[2])
            except TypeError:
                pass

        self.dataframe = pd.DataFrame(
            data=values, columns=["timestamp", "confidence", "face"]
        ).set_index("timestamp")

    def generate_report(self) -> None:
        """Generates the pandas report.
        :return:
        """
        self.__populate_dataframe()
        self.__save_dataframe()
