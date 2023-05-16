import time
import redis
from flask import Flask, render_template
import os 
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64



app = Flask(__name__, static_url_path='/Users/kevingiesen/docker/static')
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_titanic_data():
    retries = 5
    while True:
        try:
            url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
            df = pd.read_csv(url)
            df = df.head(5)
            df = df.to_html
            return df
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)             


def get_plot():
    retries = 5
    while True:
        try:
            url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"

            # Load the Titanic dataset into a Pandas DataFrame
            titanic_df = pd.read_csv(url)

            # Group the data by gender and survival and count the number of passengers in each group
            gender_survival_count = titanic_df.groupby(['Sex', 'Survived'])['Name'].count()

            # Reshape the data into a pivot table
            gender_survival_count = gender_survival_count.unstack()

            # Create a bar chart of the data
            fig, ax = plt.subplots()
            gender_survival_count.plot(kind='bar', stacked=True, ax=ax)

            # Set the chart title and axis labels
            ax.set_title('Survival Numbers by Gender')
            ax.set_xlabel('Gender')
            ax.set_ylabel('Number of Passengers')

            # Render the plot to an image buffer
            buffer = BytesIO()
            canvas = plt.get_current_fig_manager().canvas
            canvas.draw()
            image = canvas.tostring_rgb()
            buffer.write(image)

            # Encode the image buffer as a base64 string
            img_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Include the base64 string in an HTML img tag
            html = f'<img src="data:image/png;base64,{img_data}">'

            # Return the HTML
            return (html)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)             
 



@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name= "BIPM", count = count)

@app.route('/titanic')
def hello2():
    dataf = get_titanic_data()
    plot = get_plot()
    return render_template('titanic.html', name= "BIPM", df = dataf, plot = plot)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)