from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import HoverTool, ColumnDataSource
import pandas as pd
from data import StockData


class Plot:
    def __init__(self, title, code__, start, end):
        self.data = StockData(code__=code__, start=start, end=end)
        self.plot = figure(x_axis_type='datetime', width=1000, height=300)
        self.plot.sizing_mode = "scale_width"
        self.plot.title = title
        self.plot.grid.grid_line_alpha = 0.5
        hover = HoverTool(tooltips=[("Open", "@Open_String{int}"), ("Close", "@Close_String{int}"),
                                    ("High", "@High_String{int}"), ("Low", "@Low_String{int}")])
        self.plot.add_tools(hover)

    @staticmethod
    def __makeHoverData(lst):
        return ColumnDataSource(pd.DataFrame(data={"index": lst[0],
                                                   "x": (lst[1] + lst[2]) / 2,
                                                   "width": 12 * 60 * 60 * 1000,
                                                   "height": abs(lst[1] - lst[2]),
                                                   "Open_String": lst[1],
                                                   "Close_String": lst[2],
                                                   "High_String": lst[3],
                                                   "Low_String": lst[4]}))

    def __plotRect_increase_days(self):
        list1 = self.data.increase_days()
        self.plot.rect("index", "x", "width", "height",
                       fill_color="#73f062", line_color="black", source=self.__makeHoverData(list1),
                       legend_label="Rise")

    def __plotRect_decrease_days(self):
        list1 = self.data.decrease_days()
        self.plot.rect("index", "x", "width", "height",
                       fill_color="#f06262", line_color="black", source=self.__makeHoverData(list1),
                       legend_label="Fall")

    def __plotRect_equal_days(self):
        list1 = self.data.equal_days()
        self.plot.rect("index", "x", "width", "height",
                       line_color="black", source=self.__makeHoverData(list1))

    def plotRect(self, increase=True, decrease=True, equal=True):
        if increase:
            self.__plotRect_increase_days()
        if decrease:
            self.__plotRect_decrease_days()
        if equal:
            self.__plotRect_equal_days()

    def plotSegment(self):
        list1 = [self.data.df.index, self.data.df.Open, self.data.df.Close,
                 self.data.df.High, self.data.df.Low]
        self.plot.segment("index", "High_String", "index", "Low_String",
                          source=self.__makeHoverData(list1), color="Black")

    def embed(self):
        script, html = components(self.plot)
        cdn_js = CDN.js_files
        return [script, html, cdn_js[0]]

    def output(self, output):
        output_file(output)
        show(self.plot)
