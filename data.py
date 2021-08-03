from pandas_datareader import data


class StockData:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.df = data.DataReader(name="GOOG", data_source="yahoo",
                                  start=self.start, end=self.end)
        self.df["Status"] = [self.getStatus(c, o) for c, o in zip(self.df.Close,
                                                                  self.df.Open)]

    @staticmethod
    def getStatus(c, o):
        if c < o:
            return "Decrease"
        elif c > o:
            return "Increase"
        else:
            return "Equal"

    def increase_days(self):
        index = self.df.index[self.df["Status"] == "Increase"]
        open_data = self.df.Open[self.df["Status"] == "Increase"]
        close_data = self.df.Close[self.df["Status"] == "Increase"]
        high_data = self.df.High[self.df["Status"] == "Increase"]
        low_data = self.df.Low[self.df["Status"] == "Increase"]
        return [index, open_data, close_data, high_data, low_data]

    def decrease_days(self):
        index = self.df.index[self.df["Status"] == "Decrease"]
        open_data = self.df.Open[self.df["Status"] == "Decrease"]
        close_data = self.df.Close[self.df["Status"] == "Decrease"]
        high_data = self.df.High[self.df["Status"] == "Decrease"]
        low_data = self.df.Low[self.df["Status"] == "Decrease"]
        return [index, open_data, close_data, high_data, low_data]

    def equal_days(self):
        index = self.df.index[self.df["Status"] == "Equal"]
        open_data = self.df.Open[self.df["Status"] == "Equal"]
        high_data = self.df.High[self.df["Status"] == "Equal"]
        low_data = self.df.Low[self.df["Status"] == "Equal"]
        return [index, open_data, open_data, high_data, low_data]
