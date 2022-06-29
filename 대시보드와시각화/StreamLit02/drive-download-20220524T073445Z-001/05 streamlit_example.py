import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import plotly.express as px
plt.rc('font', family='Malgun Gothic')

BASE_PATH = '/media/leelabsg-storage0/UKBB_WORK/KFDA_GUEST1'
DRUG_DATA_PATH = os.path.join(BASE_PATH, 'drug_data')
META_DATA_PATH = os.path.join(BASE_PATH, 'metabolomics_data')


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': 'made by Lim',
    }
)

st.title(':book: KFDA Dashboard')
st.markdown('---')


with st.sidebar:
    a = st.selectbox('MENU', 
                        (
                            # 'README',
                            'Data',
                            'Charts',
                            'Experiment',
                            # 'Exercise 1)',
                            # 'Interactions',
                            # 'Example 1)',
                            # 'Exercise 2)',
                            # 'Exercise 3)'
                        )
    )
    
    st.markdown('---')

    st.markdown(
        '''
            <style>
                [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
                    width: 500px;
                }
                [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
                    width: 500px;
                    margin-left: -500px;
                }
            </style>
        ''',
        unsafe_allow_html=True
    )



if a == 'README':
    st.header('Getting Started')

    st.markdown('''
    ### 1) Streamlit 이란?
    - https://streamlit.io/ 
    - Streamlit은 파이썬 기반의 웹 어플리케이션을 만들 수 있는 라이브러리
    - 데이터사이언스, 머신러닝 프로젝트를 웹 어플리케이션으로 편리하게 배포 가능
    - interactive한 widget을 통해 웹페이지 탐색 가능
    - 웹 개발에 대한 지식 없이도 간단하게 페이지를 제작할 수 있음

    ### 2) 설치
    - [installation document](https://docs.streamlit.io/library/get-started/installation)
    - `pip install streamlit` : 설치 명령어
    - `streamlit hello` : 명령어를 통해 잘 설치되었는지 확인
    - `streamlit run filename.py` : 명령어를 통해 자신의 앱(filename.py) 실행

    ### 3) 기타 필요 라이브러리
    - `pip install finance-datareader`
    - `pip install beautifulsoup4`
    - `pip install -U scikit-learn`
    ''')

    st.info('''
    - Data display elements examples: [link](https://docs.streamlit.io/library/api-reference/data)
    - Layout examples: [link](https://docs.streamlit.io/library/api-reference/layout)
    - FinanceDataReader github: [link](https://github.com/FinanceData/FinanceDataReader)
    ''')



list_file_drug = list(filter(lambda file: file.endswith('csv'), os.listdir(DRUG_DATA_PATH)))
list_file_meta = list(filter(lambda file: file.endswith('csv'), os.listdir(META_DATA_PATH)))
list_file = list_file_meta + list_file_drug
dict_file = {file: DRUG_DATA_PATH if file in list_file_drug else META_DATA_PATH for file in list_file}

st.sidebar.header("filter options")

file_name = st.sidebar.selectbox(
    'data',
    list_file
)

@st.cache
def load_data(file_name):
    df = pd.read_csv(os.path.join(dict_file[file_name], file_name))
    # df.style # later...
    return df

df = load_data(file_name)

range_row = st.sidebar.slider(
    "data range",
    value=(0, len(df.index))
)

df = df.loc[range(*range_row)]



if a == 'Data':
    def draw_table(df):
        with st.spinner('Wait for it...'):
            st.dataframe(df, height=1000)
    
    list_col_selected = st.sidebar.multiselect(
        'columns',
        df.columns.tolist(),
        df.columns.tolist()
    )

    df = df[list_col_selected]

    
    mode = st.sidebar.radio(
        "mode",
        ['raw data', 'summary statistics', 'correlation', 'covariance']
        # ['summary statistics', 'correlation', 'covariance']
    )

    if mode == 'raw data':
        df = df
    if mode == 'summary statistics':
        df = df.describe()
    elif mode == 'correlation':
        df = df.corr()
    elif mode == 'covariance':
        df = df.cov()

    submit = st.sidebar.button('Submit')
    
    if submit:
        draw_table(df)
    


if a == 'Charts':
    package = st.sidebar.radio(
        "vis package",
        ['streamlit', 'plotly', 'matplotlib']
    )

    if package == 'streamlit':
        mode = st.sidebar.radio(
            "mode",
            ['bar', 'line', 'area']
        )
    elif package == 'plotly':
        mode = st.sidebar.radio(
            "mode",
            ['bar', 'line', 'area', 'heatmap']
        )
    elif package == 'matplotlib':
        mode = st.sidebar.radio(
            "mode",
            ['bar', 'line', 'area', 'heatmap']
        )

    if mode in ['bar', 'line', 'area']:
        col1, col2, col3 = st.sidebar.columns(3)
        
        x = col1.selectbox(
            "x",
            df.columns.tolist()
        )

        y = col2.selectbox(
            "y",
            df.columns.tolist()
        )
        
        z = col3.selectbox(
            "z",
            [None] + df.columns.tolist()
        )
        if x == y or x == z or y == z:
            st.warning('Please select three different variables!')
    elif mode == 'heatmap':                
        list_col_selected = st.sidebar.multiselect(
            'columns',
            df.columns.tolist(),
            df.columns.tolist()
        )
        df = df[list_col_selected]

    submit = st.sidebar.button('Submit')
    
    if submit:
        if package == 'streamlit':
            if z:
                list_variates = [x,y,z]
                df_gb = df[list_variates].groupby([x, z]).count()
                df_gb = df_gb.unstack()
                df_gb.columns = df_gb.columns.droplevel(0)
                df_gb.columns.name = None
            else:
                list_variates = [x,y]
                df_gb = df[list_variates].groupby(x).count()
            
            with st.spinner('Wait for it...'):
                if mode == 'bar':
                    st.bar_chart(df_gb)
                elif mode == 'line':
                    st.line_chart(df_gb)
                elif mode == 'area':
                    st.area_chart(df_gb)
        elif package == 'plotly':
            with st.spinner('Wait for it...'):
                if mode == 'bar':
                    if z:
                        d = df.groupby([x, z]).count()[y].reset_index()
                        fig = px.bar(d, x=x, y=y, color=z, labels={y: f'count of {y}'})
                    else:
                        d = df.groupby(x).count()[y].reset_index()
                        fig = px.bar(d, x=x, y=y, labels={y: f'count of {y}'})
                elif mode == 'line':
                    if z:
                        d = df.groupby([x, z]).count()[y].reset_index()
                        fig = px.line(d, x=x, y=y, color=z, labels={y: f'count of {y}'})
                    else:
                        d = df.groupby(x).count()[y].reset_index()
                        fig = px.line(d, x=x, y=y, labels={y: f'count of {y}'})
                elif mode == 'area':
                    if z:
                        d = df.groupby([x, z]).count()[y].reset_index()
                        fig = px.area(d, x=x, y=y, color=z, labels={y: f'count of {y}'})
                    else:
                        d = df.groupby(x).count()[y].reset_index()
                        fig = px.area(d, x=x, y=y, labels={y: f'count of {y}'})
                elif mode == 'heatmap':
                    fig = px.imshow(df.corr(), text_auto=True)
                    fig.update_layout(
                        height=1000
                    )
                st.plotly_chart(fig, use_container_width=True)
        elif package == 'matplotlib':
            with st.spinner('Wait for it...'):
                if mode == 'bar':
                    d = df.groupby(x).count()[y].reset_index()
                    fig = plt.figure()
                    plt.bar(d[x], d[y])
                elif mode == 'line':
                    d = df.groupby(x).count()[y].reset_index()
                    fig = plt.figure()
                    plt.plot(d[x], d[y])
                elif mode == 'area':
                    d = df.groupby(x).count()[y].reset_index()
                    fig = plt.figure()
                    plt.fill_between(d[x], d[y])
                elif mode == 'heatmap':
                    fig = plt.figure()
                    plt.pcolor(df.corr())
                st.pyplot(fig)



if a == 'Experiment':
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from sklearn.linear_model import LinearRegression

    x = st.sidebar.selectbox(
        'x', 
        df.columns.tolist()
    )

    y = st.sidebar.selectbox(
        'y', 
        df.columns.tolist()
    )

    df_ = df[[x, y]].dropna()
    x_value = df_[x].values.reshape(-1, 1)
    y_value = df_[y]

    model = LinearRegression()
    model.fit(x_value, y_value)

    x_range = np.linspace(x_value.min(), x_value.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = px.scatter(df_, x=x, y=y, opacity=0.3)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
    
    submit = st.sidebar.button('Submit')

    if submit:
        with st.spinner('Wait for it...'):
            st.plotly_chart(fig, use_container_width=True)
