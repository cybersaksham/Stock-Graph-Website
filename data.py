# Importing Modules
from pandas_datareader import data


class StockData:
    def __init__(self, code__, start, end):
        self.start = start
        self.end = end
        self.df = data.DataReader(name=code__, data_source="yahoo",
                                  start=self.start, end=self.end)
        self.df["Status"] = [self.getStatus(c, o) for c, o in zip(self.df.Close,
                                                                  self.df.Open)]

    @staticmethod
    def getStatus(c, o):
        # Setting status to show different colors on increased & decreased data
        if c <= o:
            return "Decrease"
        elif c > o:
            return "Increase"

    def increase_days(self):
        # Getting days for stock rise
        data__ = self.df[self.df["Status"] == "Increase"]
        return data__.T.to_dict()

    def decrease_days(self):
        # Getting days for stock fall
        data__ = self.df[self.df["Status"] == "Decrease"]
        return data__.T.to_dict()
