from random import randrange
from datetime import timedelta, datetime
import plotly.graph_objects as go
from plotly.graph_objs import Layout
import numpy as np
import json
from PIL import Image
import io

HEIGHT = 100000
WIDTH = 61


def random_date(start=datetime(2016, month=1, day=1), end=datetime(2018, month=1, day=1)):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


class Stonk:
    def __init__(self, start, p):
        self.history = []
        self.value = start
        self.p = p
        start_date = random_date()
        self.dates = [i.strftime("%d.%m") for i in np.arange(start_date, start_date + timedelta(days=60), timedelta(days=1)).astype(datetime)]

    def sim(self):
        self.history.append(self.value)
        x = randrange(0, 100)

        if self.p / 2 < x < self.p:
            self.value += randrange(5, 15)
        elif x < self.p / 2:
            pass
        else:
            self.value -= randrange(10, 20)

        self.value = max(0, self.value)
        self.value = min(HEIGHT - 1, self.value)


def create_tasks(case='default'):
    if case == 'risk':
        p = 30
    elif case == 'div':
        p = 30
    else:
        p = 80

    # simulate market activity
    stonk = Stonk(randrange(150, 350), p)
    while len(stonk.history) < WIDTH - 1:
        stonk.sim()

    half = int(stonk.history.__len__() / 2)

    half_difference = stonk.history[half] - stonk.history[0]
    difference = stonk.history[-1] - stonk.history[0]

    # draw half plot

    layout = Layout(
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis={'side': 'right'},
        coloraxis={
            'colorbar_tickfont_color': 'rgb(241, 241, 241)'
        }
    )

    half_chart = go.Figure(layout=layout)

    half_chart.add_trace(
        go.Scatter(x=stonk.dates[:half], y=stonk.history[:half], marker_color='rgb(120, 120, 120)',
                   fillcolor='rgba(241, 241, 241, 0.5)', fill='tozeroy'))

    half_chart.update_xaxes(showline=True, linewidth=2, linecolor='rgb(241, 241, 241)', gridcolor='rgb(241, 241, 241)', dtick=14)
    half_chart.update_yaxes(showline=True, linewidth=2, linecolor='rgb(241, 241, 241)', gridcolor='rgb(241, 241, 241)', dtick=100)

    chart_bytes = half_chart.to_image(format="png", width=375, height=285, scale=5)

    image_data = chart_bytes
    image = Image.open(io.BytesIO(image_data))
    image.save('images/half_chart.png')
    # image.show()

    # draw full plot
    if difference > 0:
        line_color = 'green'
        fillcolor = 'rgba(0, 254, 0, 0.1)'

    elif difference == 0:
        line_color = 'blue'
        fillcolor = 'rgba(0, 0, 254, 0.1)'

    elif difference < 0:
        line_color = 'red'
        fillcolor = 'rgba(254, 0, 0, 0.1)'

    chart = go.Figure(layout=layout)

    chart.add_trace(
        go.Scatter(x=stonk.dates, y=stonk.history, marker_color=line_color,
                   fillcolor=fillcolor, fill='tozeroy'))

    chart.update_xaxes(showline=True, linewidth=2, linecolor='rgb(241, 241, 241)', gridcolor='rgb(241, 241, 241)', dtick=28)
    chart.update_yaxes(showline=True, linewidth=2, linecolor='rgb(241, 241, 241)', gridcolor='rgb(241, 241, 241)', dtick=100)

    chart_bytes = chart.to_image(format="png", width=375, height=285, scale=5)

    image_data = chart_bytes
    image = Image.open(io.BytesIO(image_data))
    image.save('images/chart.png')
    # image.show()

    res = {
        'half_difference': half_difference,
        'difference': difference,
        'half_img_path': 'images/half_chart.png',
        'img_path': 'images/chart.png'
    }

    return json.dumps(res)


if __name__ == '__main__':
    print(create_tasks(case='default'))
