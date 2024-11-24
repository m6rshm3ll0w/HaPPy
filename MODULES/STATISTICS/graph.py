import pandas as pd
import plotly.express as px


def render_graph(date_list: list[str], happy_list: list[int], comments_list: list[str]):
    try:
        df = pd.DataFrame(dict(
            дата=date_list,
            настроение=happy_list,
            комментарий=comments_list
        ))

        fig = px.line(df, x='дата', y='настроение', hover_data="комментарий")

        fig.write_html("./DATA/graph.html")

        return True
    except Exception as E:
        print(E)
