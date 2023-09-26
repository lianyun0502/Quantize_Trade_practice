from datetime import datetime

from vnpy.trader.ui import create_qapp, QtCore
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import get_database
from vnpy.chart import ChartWidget, VolumeItem, CandleItem


if __name__ == "__main__":
    import json
    from vnpy.trader.object import BarData
    import pandas as pd
    app = create_qapp()

    database = get_database()
    bars = database.load_bar_data(
        "IF888",
        Exchange.CFFEX,
        interval=Interval.MINUTE,
        start=datetime(2019, 7, 1),
        end=datetime(2019, 7, 17)
    )
    with open(r"C:\Users\eric.li\Desktop\My Github\vnpy\examples\candle_chart\3715.json",encoding='utf-8') as f:
        bars = json.load(f)
    
    df = pd.DataFrame.from_dict(bars)
    df['datetime'] = pd.to_datetime(df['ts'])
    bars = []

    for i in range(len(df)):
        bar = BarData(
            symbol='TW3715',
            exchange=Exchange.TSE,
            interval=Interval.MINUTE,
            datetime=df['datetime'][i],
            open_price=df['Open'][i],
            high_price=df['High'][i],
            low_price=df['Low'][i],
            close_price=df['Close'][i],
            volume=df['Volume'][i],
            gateway_name='DB'
        )
        bars.append(bar) 

    widget = ChartWidget()
    widget.add_plot("candle", hide_x_axis=True)
    widget.add_plot("volume", maximum_height=200)
    widget.add_item(CandleItem, "candle", "candle")
    widget.add_item(VolumeItem, "volume", "volume")
    widget.add_cursor()

    n = 1000
    history = bars[:50]
    new_data = bars[50:]

    widget.update_history(history)

    def update_bar():
        pass
        try:
            bar = new_data.pop(0)
        except IndexError:
            timer.stop()
            return
        widget.update_bar(bar)

    timer = QtCore.QTimer()
    timer.timeout.connect(update_bar)
    timer.start(100)

    widget.show()
    app.exec()
