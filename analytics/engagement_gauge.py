import plotly.graph_objects as go

def engagement_gauge(score):

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=score,

        title={'text': "Engagement Score"},

        gauge={'axis': {'range': [0,100]}}
    ))

    fig.show()