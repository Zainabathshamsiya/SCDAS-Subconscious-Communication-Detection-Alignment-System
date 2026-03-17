import plotly.graph_objects as go
import plotly.express as px


def emotion_chart(emotion_counts):

    fig = px.pie(
        names=list(emotion_counts.keys()),
        values=list(emotion_counts.values()),
        title="Emotion Distribution"
    )

    return fig


def engagement_gauge(score):

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=score,

        title={"text":"Engagement Score"},

        gauge={"axis":{"range":[0,100]}}
    ))

    return fig


def timeline(scores):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=scores,
        mode="lines+markers"
    ))

    fig.update_layout(
        title="Engagement Timeline"
    )

    return fig