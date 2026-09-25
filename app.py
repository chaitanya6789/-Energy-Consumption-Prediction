
import inspect
import joblib

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PJM Load Forecast",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN TOKENS
# ============================================================

AMBER = "#f5a524"
SLATE = "#5b6b8c"
RED = "#ff6b6b"
TEAL = "#2dd4bf"
GRID = "#1f2a44"
MUTED = "#93a1bd"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'IBM Plex Sans', sans-serif;
}

h1, h2, h3, .display {
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.01em;
}

.block-container {
    padding-top: 1.6rem;
    max-width: 1280px;
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}


/* ---------- Header ---------- */

.masthead {
    display: grid;
    grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr);
    gap: 32px;
    align-items: end;
    padding: 8px 0 26px 0;
    border-bottom: 1px solid #1f2a44;
    margin-bottom: 22px;
}

.masthead .title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.7rem;
    font-weight: 700;
    line-height: 1.05;
    color: #111a2e;
}

.masthead .title span {
    color: #f5a524;
}

.masthead .lede {
    margin-top: 12px;
    color: #93a1bd;
    font-size: 1.02rem;
    max-width: 520px;
    line-height: 1.55;
}

.pulse-label {
    color: #93a1bd;
    font-size: .86rem;
    margin-bottom: 4px;
}

.pulse-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.9rem;
    font-weight: 600;
    color: #111a2e;
}
}

.pulse-value small {
    font-size: .95rem;
    color: #93a1bd;
    font-weight: 500;
}


/* ---------- Metric strip ---------- */

.strip {
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: 1fr;
    background: #111a2e;
    border: 1px solid #1f2a44;
    border-radius: 10px;
    margin: 6px 0 18px 0;
}

.strip .cell {
    padding: 16px 20px;
    border-right: 1px solid #1f2a44;
}

.strip .cell:last-child {
    border-right: none;
}

.strip .lab {
    color: #93a1bd;
    font-size: .86rem;
}

.strip .val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.55rem;
    font-weight: 600;
    color: #f4f7fd;
    margin-top: 2px;
}

.strip .sub {
    color: #6f7f9f;
    font-size: .8rem;
    margin-top: 2px;
}

.strip .cell.hot .val {
    color: #f5a524;
}


/* ---------- Section headings ---------- */

.sec {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
<<<<<<< HEAD
    color: #000000;
=======
    color: #111a2e;
>>>>>>> fa56967 (Change section titles to black)
    margin: 22px 0 4px 0;
}

.sec-note {
    color: #93a1bd;
    font-size: .9rem;
    margin-bottom: 8px;
}


/* ---------- Empty-state steps ---------- */

.steps {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0;
    border: 1px solid #1f2a44;
    border-radius: 10px;
    margin-top: 18px;
    background: #111a2e;
}

.steps .s {
    padding: 20px 22px;
    border-right: 1px solid #1f2a44;
}

.steps .s:last-child {
    border-right: none;
}

.steps .n {
    font-family: 'Space Grotesk', sans-serif;
    color: #f5a524;
    font-size: 1.3rem;
    font-weight: 700;
}

.steps .t {
    color: #f4f7fd;
    font-weight: 600;
    margin: 4px 0 2px 0;
}

.steps .d {
    color: #93a1bd;
    font-size: .9rem;
    line-height: 1.5;
}


/* ---------- Result banner ---------- */

.banner {
    border-left: 3px solid #f5a524;
    background: #111a2e;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    color: #e6ebf5;
    margin: 6px 0 14px 0;
}

.banner b {
    color: #f5a524;
    font-weight: 600;
}


/* ---------- Controls ---------- */

div.stButton > button[kind="primary"],
div.stDownloadButton > button {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.02rem;
    border-radius: 8px;
    height: 3.1rem;
    border: 1px solid #f5a524;
}

div.stButton > button[kind="primary"] {
    background: #f5a524;
    color: #0b1220;
}

div.stButton > button[kind="primary"]:hover {
    background: #ffb93d;
    border-color: #ffb93d;
    color: #0b1220;
}

div.stDownloadButton > button {
    background: transparent;
    color: #f5a524;
}

div.stDownloadButton > button:hover {
    background: rgba(245,165,36,.1);
    color: #ffb93d;
    border-color: #ffb93d;
}


.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: 1px solid #1f2a44;
}

.stTabs [data-baseweb="tab"] {
    font-weight: 500;
    padding: 10px 16px;
}

.stTabs [aria-selected="true"] {
    color: #f5a524;
}


section[data-testid="stSidebar"] {
    border-right: 1px solid #1f2a44;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-size: 1.05rem;
    margin-bottom: .2rem;
}

.side-card {
    background: #0b1220;
    border: 1px solid #1f2a44;
    border-radius: 8px;
    padding: 10px 12px;
    margin: 10px 0 14px 0;
    font-size: .92rem;
    color: #e6ebf5;
}

.side-card b {
    color: #f5a524;
    font-weight: 600;
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# COMPATIBILITY HELPER
# ============================================================

def stretch(func):
    """Return correct full-width argument for Streamlit version."""
    params = inspect.signature(func).parameters

    if "use_container_width" in params:
        return {"use_container_width": True}

    return {"width": "stretch"}


# ============================================================
# LOAD XGBOOST MODEL
# ============================================================

@st.cache_resource
def load_xgboost_model():

    model = joblib.load("pjm_xgboost_model.pkl")

    return model


# ============================================================
# LOAD XGBOOST FEATURE LIST
# ============================================================

@st.cache_resource
def load_xgb_features():

    features = joblib.load("xgb_features.pkl")

    return list(features)


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_excel("PJMW_MW_Hourly.xlsx")

    df["Datetime"] = pd.to_datetime(
        df["Datetime"],
        errors="coerce"
    )

    df["PJMW_MW"] = pd.to_numeric(
        df["PJMW_MW"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Datetime", "PJMW_MW"]
    )

    df = (
        df
        .sort_values("Datetime")
        .reset_index(drop=True)
    )

    return df[["Datetime", "PJMW_MW"]]


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def create_features(history_df, timestamp):

    values = history_df["PJMW_MW"].values

    row = {}

    # --------------------------------------------------------
    # LAG FEATURES
    # --------------------------------------------------------

    lag_map = {
        "lag_1": 1,
        "lag_2": 2,
        "lag_3": 3,
        "lag_6": 6,
        "lag_12": 12,
        "lag_24": 24,
        "lag_48": 48,
        "lag_72": 72,
        "lag_168": 168,
        "lag_336": 336,
        "lag_504": 504,
        "lag_720": 720,
    }

    for feature_name, lag in lag_map.items():

        if len(values) >= lag:
            row[feature_name] = float(values[-lag])

        else:
            row[feature_name] = np.nan


    # --------------------------------------------------------
    # ROLLING FEATURES
    # --------------------------------------------------------

    if len(values) >= 24:

        last_24 = values[-24:]

        row["rolling_mean_24"] = float(
            np.mean(last_24)
        )

        row["rolling_std_24"] = float(
            np.std(last_24)
        )

    else:

        row["rolling_mean_24"] = np.nan
        row["rolling_std_24"] = np.nan


    if len(values) >= 168:

        last_168 = values[-168:]

        row["rolling_mean_168"] = float(
            np.mean(last_168)
        )

        row["rolling_std_168"] = float(
            np.std(last_168)
        )

    else:

        row["rolling_mean_168"] = np.nan
        row["rolling_std_168"] = np.nan


    # --------------------------------------------------------
    # TIME FEATURES
    # --------------------------------------------------------

    row["Hour"] = timestamp.hour
    row["Month"] = timestamp.month
    row["Year"] = timestamp.year
    row["Day"] = timestamp.day
    row["Day_of_Week"] = timestamp.dayofweek


    # --------------------------------------------------------
    # WEEKDAY ONE-HOT FEATURES
    # --------------------------------------------------------

    for i in range(7):

        row[f"Day_of_Week_{i}"] = (
            1 if timestamp.dayofweek == i else 0
        )


    # --------------------------------------------------------
    # SEASON
    # --------------------------------------------------------

    month = timestamp.month

    if month in [12, 1, 2]:

        season = "Winter"

    elif month in [6, 7, 8]:

        season = "Summer"

    else:

        season = "Other"


    row["Season_Winter"] = (
        1 if season == "Winter" else 0
    )

    row["Season_Summer"] = (
        1 if season == "Summer" else 0
    )

    row["Season_Other"] = (
        1 if season == "Other" else 0
    )


    return row


# ============================================================
# XGBOOST RECURSIVE FORECAST
# ============================================================

def forecast_xgboost(
    model,
    feature_list,
    history_df,
    start_datetime,
    hours_to_predict
):

    history = history_df.copy()

    predictions = []

    future_dates = pd.date_range(
        start=start_datetime,
        periods=hours_to_predict,
        freq="h"
    )

    for future_time in future_dates:

        # ----------------------------------------------
        # CREATE FEATURES FOR NEXT HOUR
        # ----------------------------------------------

        feature_dict = create_features(
            history,
            future_time
        )

        feature_row = pd.DataFrame(
            [feature_dict]
        )

        # ----------------------------------------------
        # MAKE SURE FEATURE ORDER MATCHES TRAINING
        # ----------------------------------------------

        for feature in feature_list:

            if feature not in feature_row.columns:

                feature_row[feature] = 0

        feature_row = feature_row[
            feature_list
        ]

        # ----------------------------------------------
        # HANDLE MISSING VALUES
        # ----------------------------------------------

        feature_row = feature_row.replace(
            [np.inf, -np.inf],
            np.nan
        )

        feature_row = feature_row.fillna(0)

        # ----------------------------------------------
        # PREDICTION
        # ----------------------------------------------

        prediction = model.predict(
            feature_row
        )[0]

        prediction = float(
            max(prediction, 0)
        )

        predictions.append(
            prediction
        )

        # ----------------------------------------------
        # APPEND PREDICTION TO HISTORY
        # ----------------------------------------------

        new_row = pd.DataFrame({
            "Datetime": [future_time],
            "PJMW_MW": [prediction],
        })

        history = pd.concat(
            [history, new_row],
            ignore_index=True
        )


    return np.array(predictions)


# ============================================================
# UI HELPERS
# ============================================================

def sparkline_svg(
    values,
    width=420,
    height=70
):

    v = np.asarray(
        values,
        dtype=float
    )

    lo = v.min()
    hi = v.max()

    xs = np.linspace(
        2,
        width - 6,
        len(v)
    )

    ys = (
        height
        - 8
        - (v - lo)
        / (hi - lo + 1e-9)
        * (height - 16)
    )

    pts = " ".join(
        f"{x:.1f},{y:.1f}"
        for x, y in zip(xs, ys)
    )

    area = (
        f"2,{height} "
        + pts
        + f" {width - 6},{height}"
    )

    return (
        f'<svg viewBox="0 0 {width} {height}" '
        f'width="100%" height="{height}" '
        f'preserveAspectRatio="none" '
        f'role="img" '
        f'aria-label="Last 7 days of actual load">'

        f'<polygon points="{area}" '
        f'fill="{AMBER}" fill-opacity="0.10"/>'

        f'<polyline points="{pts}" '
        f'fill="none" stroke="{AMBER}" '
        f'stroke-width="1.6" '
        f'stroke-linejoin="round"/>'

        f'<circle cx="{xs[-1]:.1f}" '
        f'cy="{ys[-1]:.1f}" r="3.5" '
        f'fill="{AMBER}"/>'

        f"</svg>"
    )


def metric_strip(items):

    cells = ""

    for label, value, sub, hot in items:

        cls = (
            "cell hot"
            if hot
            else "cell"
        )

        cells += (
            f'<div class="{cls}">'
            f'<div class="lab">{label}</div>'
            f'<div class="val">{value}</div>'
            f'<div class="sub">{sub}</div>'
            f'</div>'
        )

    st.markdown(
        f'<div class="strip">{cells}</div>',
        unsafe_allow_html=True
    )


def section(title, note=None):

    html = (
        f'<div class="sec">{title}</div>'
    )

    if note:

        html += (
            f'<div class="sec-note">{note}</div>'
        )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def style_chart(chart, height=380):

    return (
        chart
        .properties(
            height=height,
            background="transparent"
        )
        .configure_view(
            strokeWidth=0
        )
        .configure_axis(
            labelColor=MUTED,
            titleColor=MUTED,
            gridColor=GRID,
            domainColor=GRID,
            tickColor=GRID,
            labelFontSize=12,
            titleFontSize=12,
        )
        .configure_legend(
            labelColor=MUTED,
            titleColor=MUTED,
            orient="top",
            labelFontSize=12
        )
    )


# ============================================================
# LOAD EVERYTHING
# ============================================================

try:

    model = load_xgboost_model()

    feature_list = load_xgb_features()

    df = load_data()

except FileNotFoundError as e:

    st.error(
        f"File not found: {e.filename}. "
        "Keep the Streamlit app, XGBoost model, "
        "feature file and Excel dataset in the same folder."
    )

    st.stop()

except Exception as e:

    st.error(
        f"Application loading error: {e}"
    )

    st.stop()


# ============================================================
# DATASET INFORMATION
# ============================================================

min_datetime = df["Datetime"].min()

max_datetime = df["Datetime"].max()

last_actual_load = df["PJMW_MW"].iloc[-1]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    "## Forecast settings"
)


forecast_days = st.sidebar.slider(
    "Forecast period (days)",
    min_value=1,
    max_value=30,
    value=7,
    step=1
)


hours_to_predict = (
    forecast_days * 24
)


st.sidebar.markdown(
    f'''
    <div class="side-card">
        <b>{forecast_days} day(s)</b> means
        <b>{hours_to_predict}</b>
        hourly predictions
    </div>
    ''',
    unsafe_allow_html=True
)


st.sidebar.markdown(
    "### Forecast start"
)


use_last_timestamp = st.sidebar.checkbox(
    "Start right after the last dataset value",
    value=True
)


if use_last_timestamp:

    selected_datetime = (
        max_datetime
        + pd.Timedelta(hours=1)
    )

else:

    selected_date = st.sidebar.date_input(
        "Select date",
        value=max_datetime.date()
    )

    selected_time = st.sidebar.time_input(
        "Select time",
        value=(
            max_datetime
            + pd.Timedelta(hours=1)
        ).time()
    )

    selected_datetime = pd.Timestamp(
        f"{selected_date} {selected_time}"
    )


st.sidebar.markdown(
    f'''
    <div class="side-card">
        Forecast starts at<br>
        <b>
        {selected_datetime.strftime("%Y-%m-%d %H:%M")}
        </b>
    </div>
    ''',
    unsafe_allow_html=True
)


with st.sidebar.expander(
    "About the model"
):

    st.markdown(
        "- XGBoost Regressor\n"
        "- Recursive hourly forecasting\n"
        "- Lag-based historical features\n"
        "- Rolling mean/std features\n"
        "- Calendar and seasonal features\n"
        "- No scaler required"
    )


# ============================================================
# MASTHEAD
# ============================================================

recent_actual = (
    df["PJMW_MW"]
    .tail(168)
    .values
)

st.markdown(
    f"""
<div class="masthead">
<div>
<div class="title">
PJM electricity<br>
load <span>forecast</span>
</div>
<div class="lede">
Hourly demand forecasts for up to
30 days ahead, generated by a trained
XGBoost regression model on PJM West data.
</div>
</div>
<div>
<div class="pulse-label">
Last 7 days of actual load
</div>
{sparkline_svg(recent_actual)}
<div class="pulse-value">
{last_actual_load:,.0f}
<small>
MW at
{max_datetime.strftime("%Y-%m-%d %H:%M")}
</small>
</div>
</div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# TOP METRICS
# ============================================================

metric_strip([
    (
        "Historical data start",
        min_datetime.strftime("%Y-%m-%d"),
        "First record",
        False
    ),

    (
        "Last available data",
        max_datetime.strftime("%Y-%m-%d %H:%M"),
        "Latest record",
        False
    ),

    (
        "Hourly records",
        f"{len(df):,}",
        "Used for forecasting",
        False
    ),

    (
        "Last actual load",
        f"{last_actual_load:,.0f} MW",
        "Latest reading",
        True
    ),
])


# ============================================================
# PREDICTION BUTTON
# ============================================================

run = st.button(
    f"Generate {forecast_days}-day forecast",
    type="primary",
    **stretch(st.button)
)


if run:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if selected_datetime <= min_datetime:

        st.error(
            "The forecast start must be after "
            "the beginning of the available dataset."
        )

        st.stop()


    # --------------------------------------------------------
    # BUILD HISTORY
    # --------------------------------------------------------

    if selected_datetime <= max_datetime:

        matching_rows = df[
            df["Datetime"] == selected_datetime
        ]

        if matching_rows.empty:

            st.error(
                "That date and time isn't in the hourly dataset. "
                "Select an available timestamp."
            )

            st.stop()


        selected_index = (
            matching_rows.index[0]
        )


        # XGBoost model uses up to 720-hour lag
        if selected_index < 720:

            st.error(
                "At least 720 previous hourly records "
                "are required for this XGBoost model."
            )

            st.stop()


        history_df = (
            df.iloc[:selected_index]
            [["Datetime", "PJMW_MW"]]
            .copy()
        )

    else:

        history_df = (
            df[
                ["Datetime", "PJMW_MW"]
            ]
            .copy()
        )


    # --------------------------------------------------------
    # FORECAST
    # --------------------------------------------------------

    with st.spinner(
        f"Generating {hours_to_predict} hourly predictions..."
    ):

        try:

            predictions = forecast_xgboost(
                model=model,
                feature_list=feature_list,
                history_df=history_df,
                start_datetime=selected_datetime,
                hours_to_predict=hours_to_predict
            )

        except Exception as e:

            st.error(
                f"Prediction failed: {e}"
            )

            st.stop()


    # --------------------------------------------------------
    # FORECAST DATAFRAME
    # --------------------------------------------------------

    future_dates = pd.date_range(
        start=selected_datetime,
        periods=hours_to_predict,
        freq="h"
    )


    forecast_df = pd.DataFrame({

        "Prediction_Number":
            np.arange(
                1,
                hours_to_predict + 1
            ),

        "Datetime":
            future_dates,

        "Predicted_MW":
            predictions,

    })


    # ========================================================
    # DAILY SUMMARY
    # ========================================================

    daily_df = (
        forecast_df
        .set_index("Datetime")["Predicted_MW"]
        .resample("D")
        .agg(
            Average_MW="mean",
            Maximum_MW="max",
            Minimum_MW="min",
            Total_Hourly_MW="sum",
        )
        .reset_index()
    )


    # ========================================================
    # HISTORICAL DATA FOR CHART
    # ========================================================

    hist_df = (
        df[
            df["Datetime"] < selected_datetime
        ]
        .tail(168)
        [["Datetime", "PJMW_MW"]]
    )


    # ========================================================
    # SESSION STATE
    # ========================================================

    st.session_state["result"] = {

        "forecast_df":
            forecast_df,

        "daily_df":
            daily_df,

        "hist_df":
            hist_df,

        "start":
            selected_datetime,

        "days":
            forecast_days,

        "hours":
            hours_to_predict,

    }


# ============================================================
# RESULTS
# ============================================================

result = (
    st.session_state.get("result")
)


if result is None:

    st.markdown(
        """
<div class="steps">
<div class="s">
<div class="n">1</div>
<div class="t">
Pick a period
</div>
<div class="d">
Use the slider in the sidebar
to choose 1 to 30 days.
</div>
</div>
<div class="s">
<div class="n">2</div>
<div class="t">
Set the start
</div>
<div class="d">
Begin after the last record,
or choose an earlier hour
in the dataset.
</div>
</div>
<div class="s">
<div class="n">3</div>
<div class="t">
Generate
</div>
<div class="d">
XGBoost predicts hour by hour
and shows charts, tables,
and downloads.
</div>
</div>
</div>
""",
        unsafe_allow_html=True
    )


else:

    forecast_df = result["forecast_df"]

    daily_df = result["daily_df"]

    hist_df = result["hist_df"]

    days = result["days"]

    hours = result["hours"]

    start = result["start"]


    preds = (
        forecast_df["Predicted_MW"]
        .values
    )

    times = (
        forecast_df["Datetime"]
    )


    avg_load = preds.mean()

    max_load = preds.max()

    min_load = preds.min()


    max_time = (
        times.iloc[
            int(np.argmax(preds))
        ]
    )

    min_time = (
        times.iloc[
            int(np.argmin(preds))
        ]
    )


    total_gwh = (
        preds.sum() / 1000
    )


    # ========================================================
    # RESULT BANNER
    # ========================================================

    st.markdown(
        f'''
<div class="banner">
Forecast ready:
<b>{hours} hourly predictions</b>
for {days} day(s),
starting
{start.strftime("%Y-%m-%d %H:%M")}.
</div>
''',
        unsafe_allow_html=True
    )


    # ========================================================
    # FORECAST METRICS
    # ========================================================

    metric_strip([

        (
            "Average load",
            f"{avg_load:,.0f} MW",
            f"Across {hours} hours",
            False
        ),

        (
            "Peak load",
            f"{max_load:,.0f} MW",
            max_time.strftime(
                "%Y-%m-%d %H:%M"
            ),
            True
        ),

        (
            "Minimum load",
            f"{min_load:,.0f} MW",
            min_time.strftime(
                "%Y-%m-%d %H:%M"
            ),
            False
        ),

        (
            "Total energy",
            f"{total_gwh:,.1f} GWh",
            "Sum of hourly load",
            False
        ),

    ])


    # ========================================================
    # TABS
    # ========================================================

    (
        tab_chart,
        tab_daily,
        tab_hourly,
        tab_export
    ) = st.tabs([
        "Forecast",
        "Daily view",
        "Hourly data",
        "Export"
    ])


    # ========================================================
    # FORECAST TAB
    # ========================================================

    with tab_chart:

        section(
            "Hourly load forecast",
            "Grey shows the last 7 days of actual load. "
            "Drag to pan and scroll to zoom.",
        )


        hist_plot = (
            hist_df
            .rename(
                columns={
                    "PJMW_MW": "Load_MW"
                }
            )
            .assign(
                Series="Recent actual"
            )
        )


        fc_plot = (
            forecast_df[
                ["Datetime", "Predicted_MW"]
            ]
            .rename(
                columns={
                    "Predicted_MW": "Load_MW"
                }
            )
            .assign(
                Series="Forecast"
            )
        )


        combined = pd.concat(
            [
                hist_plot,
                fc_plot
            ],
            ignore_index=True
        )


        color = alt.Color(
            "Series:N",

            scale=alt.Scale(
                domain=[
                    "Recent actual",
                    "Forecast"
                ],

                range=[
                    SLATE,
                    AMBER
                ]
            ),

            legend=alt.Legend(
                title=None
            ),
        )


        base = (
            alt.Chart(combined)
            .encode(

                x=alt.X(
                    "Datetime:T",
                    title=None
                ),

                y=alt.Y(
                    "Load_MW:Q",
                    title="Load (MW)",
                    scale=alt.Scale(
                        zero=False
                    )
                ),

                color=color,
            )
        )


        lines = (
            base
            .mark_line(
                strokeWidth=2.2
            )
        )


        hover = (
            base
            .mark_circle(
                size=60,
                opacity=0
            )
            .encode(

                tooltip=[

                    alt.Tooltip(
                        "Series:N"
                    ),

                    alt.Tooltip(
                        "Datetime:T",
                        format="%Y-%m-%d %H:%M"
                    ),

                    alt.Tooltip(
                        "Load_MW:Q",
                        title="Load (MW)",
                        format=",.1f"
                    ),

                ]
            )
        )


        start_rule = (
            alt.Chart(
                pd.DataFrame({
                    "Datetime": [start]
                })
            )
            .mark_rule(
                strokeDash=[5, 4],
                color=MUTED,
                opacity=0.7
            )
            .encode(
                x="Datetime:T"
            )
        )


        peak_data = pd.DataFrame({

            "Datetime": [max_time],

            "Load_MW": [max_load],

            "Label": ["Peak"]

        })


        peak_pt = (
            alt.Chart(peak_data)
            .mark_circle(
                size=140,
                color=RED
            )
            .encode(

                x="Datetime:T",

                y="Load_MW:Q",

                tooltip=[
                    "Label:N"
                ]
            )
        )


        peak_txt = (
            alt.Chart(peak_data)
            .mark_text(
                dy=-14,
                color=RED,
                fontWeight="bold",
                fontSize=12
            )
            .encode(

                x="Datetime:T",

                y="Load_MW:Q",

                text="Label:N"
            )
        )


        min_data = pd.DataFrame({

            "Datetime": [min_time],

            "Load_MW": [min_load],

            "Label": ["Low"]

        })


        min_pt = (
            alt.Chart(min_data)
            .mark_circle(
                size=140,
                color=TEAL
            )
            .encode(

                x="Datetime:T",

                y="Load_MW:Q",

                tooltip=[
                    "Label:N"
                ]
            )
        )


        min_txt = (
            alt.Chart(min_data)
            .mark_text(
                dy=16,
                color=TEAL,
                fontWeight="bold",
                fontSize=12
            )
            .encode(

                x="Datetime:T",

                y="Load_MW:Q",

                text="Label:N"
            )
        )


        layered = (
            alt.layer(
                start_rule,
                lines,
                hover,
                peak_pt,
                peak_txt,
                min_pt,
                min_txt
            )
            .interactive()
        )


        st.altair_chart(
            style_chart(
                layered,
                400
            ),
            theme=None,
            **stretch(
                st.altair_chart
            )
        )


        st.caption(
            "Forecasts are recursive: every predicted "
            "hour becomes part of the historical input "
            "used to create the next hour's XGBoost features."
        )


    # ========================================================
    # DAILY TAB
    # ========================================================

    with tab_daily:

        section(
            "Daily average load",
            "Bars show the daily average; "
            "the thin line spans the daily "
            "minimum to maximum."
        )


        bars = (
            alt.Chart(daily_df)
            .mark_bar(
                cornerRadiusTopLeft=4,
                cornerRadiusTopRight=4,
                color=AMBER,
                opacity=0.9
            )
            .encode(

                x=alt.X(
                    "Datetime:T",
                    timeUnit="yearmonthdate",
                    title=None
                ),

                y=alt.Y(
                    "Average_MW:Q",
                    title="Load (MW)",
                    scale=alt.Scale(
                        zero=False
                    )
                ),

                tooltip=[

                    alt.Tooltip(
                        "Datetime:T",
                        title="Date",
                        format="%Y-%m-%d"
                    ),

                    alt.Tooltip(
                        "Average_MW:Q",
                        title="Average (MW)",
                        format=",.1f"
                    ),

                    alt.Tooltip(
                        "Maximum_MW:Q",
                        title="Maximum (MW)",
                        format=",.1f"
                    ),

                    alt.Tooltip(
                        "Minimum_MW:Q",
                        title="Minimum (MW)",
                        format=",.1f"
                    ),

                ],
            )
        )


        rng = (
            alt.Chart(daily_df)
            .mark_rule(
                color="#e6ebf5",
                strokeWidth=1.5
            )
            .encode(

                x=alt.X(
                    "Datetime:T",
                    timeUnit="yearmonthdate"
                ),

                y="Minimum_MW:Q",

                y2="Maximum_MW:Q",

            )
        )


        st.altair_chart(
            style_chart(
                alt.layer(
                    bars,
                    rng
                ),
                320
            ),
            theme=None,
            **stretch(
                st.altair_chart
            )
        )


        # ----------------------------------------------------
        # HEATMAP
        # ----------------------------------------------------

        if days >= 2:

            section(
                "Load pattern by hour",
                "Each row is a day, each column an hour. "
                "Brighter means higher demand."
            )


            heat_df = forecast_df.assign(

                Date=forecast_df[
                    "Datetime"
                ].dt.strftime("%b %d"),

                Hour=forecast_df[
                    "Datetime"
                ].dt.hour,

            )


            heat = (
                alt.Chart(heat_df)
                .mark_rect()
                .encode(

                    x=alt.X(
                        "Hour:O",
                        title="Hour of day",
                        axis=alt.Axis(
                            labelAngle=0
                        )
                    ),

                    y=alt.Y(
                        "Date:O",
                        sort=None,
                        title=None
                    ),

                    color=alt.Color(
                        "Predicted_MW:Q",

                        scale=alt.Scale(
                            scheme="inferno"
                        ),

                        legend=alt.Legend(
                            title="MW",
                            orient="right",
                            titleColor=MUTED,
                            labelColor=MUTED
                        ),
                    ),

                    tooltip=[

                        alt.Tooltip(
                            "Date:O"
                        ),

                        alt.Tooltip(
                            "Hour:O"
                        ),

                        alt.Tooltip(
                            "Predicted_MW:Q",
                            title="Load (MW)",
                            format=",.1f"
                        ),

                    ],
                )
            )


            st.altair_chart(
                style_chart(
                    heat,
                    max(
                        180,
                        26 * days + 60
                    )
                ),
                theme=None,
                **stretch(
                    st.altair_chart
                ),
            )


        # ----------------------------------------------------
        # DAILY TABLE
        # ----------------------------------------------------

        section(
            "Daily summary table"
        )


        st.dataframe(

            daily_df,

            hide_index=True,

            column_config={

                "Datetime":
                    st.column_config.DateColumn(
                        "Date",
                        format="YYYY-MM-DD"
                    ),

                "Average_MW":
                    st.column_config.NumberColumn(
                        "Average (MW)",
                        format="%.1f"
                    ),

                "Maximum_MW":
                    st.column_config.NumberColumn(
                        "Maximum (MW)",
                        format="%.1f"
                    ),

                "Minimum_MW":
                    st.column_config.NumberColumn(
                        "Minimum (MW)",
                        format="%.1f"
                    ),

                "Total_Hourly_MW":
                    st.column_config.NumberColumn(
                        "Total (MWh)",
                        format="%.0f"
                    ),

            },

            **stretch(
                st.dataframe
            ),
        )


    # ========================================================
    # HOURLY TAB
    # ========================================================

    with tab_hourly:

        section(
            f"Hourly predictions ({hours} rows)"
        )


        st.dataframe(

            forecast_df,

            hide_index=True,

            column_config={

                "Prediction_Number":
                    st.column_config.NumberColumn(
                        "#",
                        format="%d",
                        width="small"
                    ),

                "Datetime":
                    st.column_config.DatetimeColumn(
                        "Datetime",
                        format="YYYY-MM-DD HH:mm"
                    ),

                "Predicted_MW":
                    st.column_config.ProgressColumn(

                        "Predicted load",

                        min_value=float(
                            min_load
                        ),

                        max_value=float(
                            max_load
                        ),

                        format="%.1f MW"
                    ),

            },

            **stretch(
                st.dataframe
            ),
        )


    # ========================================================
    # EXPORT TAB
    # ========================================================

    with tab_export:

        section(
            "Download results",
            "Both files open directly in Excel."
        )


        c1, c2 = st.columns(2)


        with c1:

            st.download_button(

                label=
                    "Download hourly forecast (CSV)",

                data=
                    forecast_df
                    .to_csv(index=False)
                    .encode("utf-8"),

                file_name=
                    f"pjm_load_forecast_{days}_days.csv",

                mime=
                    "text/csv",

                **stretch(
                    st.download_button
                ),
            )


        with c2:

            st.download_button(

                label=
                    "Download daily summary (CSV)",

                data=
                    daily_df
                    .to_csv(index=False)
                    .encode("utf-8"),

                file_name=
                    f"pjm_daily_summary_{days}_days.csv",

                mime=
                    "text/csv",

                **stretch(
                    st.download_button
                ),
            )
