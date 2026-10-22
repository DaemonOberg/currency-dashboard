import plotly.express as px

rates = [10.5, 10.7, 10.6]
days = ["Day 1", "Day 2", "Day 3"]
fig = px.line(x=days, y=rates)
fig.show()