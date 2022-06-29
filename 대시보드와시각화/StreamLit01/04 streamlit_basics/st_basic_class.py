import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier


plt.rc('font', family='Malgun Gothic')


st.title(':book: Streamlit Basic Tutorial')
st.markdown('---')

with st.sidebar:
    a = st.selectbox('Select tutorial', ('Getting started',
                                        'Write text', 
                                        'Data and Layouts', 
                                        'Charts',
                                        'Exercise 1)', 
                                        'Interactions',
                                        'Example 1)',
                                        'Exercise 2)',
                                        'Exercise 3)'
                                        ))
    st.markdown('---')


if a == 'Getting started':
    st.markdown('''
    ### Getting started
    #### 1) Streamlit 이란?
    - https://streamlit.io/ 
    - Streamlit은 파이썬 기반의 웹 어플리케이션을 만들 수 있는 라이브러리
    - 데이터사이언스, 머신러닝 프로젝트를 웹 어플리케이션으로 편리하게 배포 가능
    - interactive한 widget을 통해 웹페이지 탐색 가능
    - 웹 개발에 대한 지식 없이도 간단하게 페이지를 제작할 수 있음

    #### 2) 설치
    - [installation document](https://docs.streamlit.io/library/get-started/installation)
    - `pip install streamlit` : 설치 명령어
    - `streamlit hello` : 명령어를 통해 잘 설치되었는지 확인
    - `streamlit run filename.py` : 명령어를 통해 자신의 앱(filename.py) 실행

    #### 3) 기타 필요 라이브러리
    - `pip install finance-datareader`
    - `pip install beautifulsoup4`
    - `pip install -U scikit-learn`
    ''')



if a == 'Write text':
    
    st.header('1. Writing texts in streamlit')

    st.title('Title')

    # header
    st.header('This is header')

    # subheader
    st.subheader('Subheader')

    # markdown
    st.markdown('''
    ## Markdown
    #### Markdown
    `code block`
    - list 1
    - list 2
    ''')

    # code
    st.code('''
    for i in range(5):
        print(i)
    ''', language='python')

    # st.echo()
    # with st.echo():
    #     for i in range(5):
    #         print(i)

    # latex
    st.latex(' \mu ')

    # caption
    st.caption('caption')

    # status
    st.info('This is information')
    st.success('Success')
    st.error('error')
    st.warning('warning')

    # emoji
    st.write(':tulip:')
    st.write(':coffee:')

if a == 'Data and Layouts':

    st.header('2. Data display and Layouts')
    st.info('''
    - Data display elements examples: [link](https://docs.streamlit.io/library/api-reference/data)
    - Layout examples: [link](https://docs.streamlit.io/library/api-reference/layout)
    - FinanceDataReader github: [link](https://github.com/FinanceData/FinanceDataReader)
    ''')

    # dataframe
    st.subheader('KRX 시가총액 Dataframe')
    
    @st.cache # stores the result in a local cache
    def get_StockListing(ticker):
        df = fdr.StockListing(ticker)
        return df

    df = get_StockListing('KRX-MARCAP')
    st.dataframe(df)

    st.table(df.iloc[:10, :8])

    st.metric('삼성전자', 67600, 1.96)

    st.metric('삼성전자',
            str(df[df['Name']=='삼성전자']['Close'].values[0]),
            str(df[df['Name']=='삼성전자']['Changes'].values[0]))

    # image
    image = Image.open('desert.jpg')
    st.image(image, caption='This is desert')
    st.image("https://static.streamlit.io/examples/cat.jpg")

    ### Layouts

    st.subheader('Column Layout')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('네이버', 
                str(df[df['Name']=='NAVER']['Close'].values[0]), 
                str(df[df['Name']=='NAVER']['ChagesRatio'].values[0]) + '%')
    with col2:
        st.metric('카카오', 
                str(df[df['Name']=='카카오']['Close'].values[0]) , 
                str(df[df['Name']=='카카오']['ChagesRatio'].values[0]) + '%')
    with col3:
        st.metric('현대차', 
                str(df[df['Name']=='현대차']['Close'].values[0]) , 
                str(df[df['Name']=='현대차']['ChagesRatio'].values[0]) + '%')
    
    col4, col5 = st.columns([1, 2])
    with col4:
        st.image("https://static.streamlit.io/examples/cat.jpg")

    with col5:
        st.image("https://static.streamlit.io/examples/dog.jpg")

    with st.sidebar:
        st.header('Sidebar')
        st.write('text')
    
    with st.expander('click', expanded=False):
        st.write('## Expander')
        st.image("https://static.streamlit.io/examples/dog.jpg")

if a == 'Charts':
    
    st.markdown('### 3. Charts')
    st.info('''
    - You can check other ways to make charts in [here](https://docs.streamlit.io/library/api-reference/charts)
    - FinanceDataReader github: [link](https://github.com/FinanceData/FinanceDataReader)
    ''')

    @st.cache
    def get_price(ticker, start, end):
        df = fdr.DataReader(ticker, start, end)
        return df

    @st.cache # stores the result in a local cache
    def get_StockListing(ticker):
        df = fdr.StockListing(ticker)
        return df

    df = get_price('005930', '2017-01-01', '2022-04-04')
    st.dataframe(df)
    st.line_chart(df['Close'])

    st.markdown('''
    #### Streamlit line chart 2
    - Closing price of multiple stocks
    ''')

    stock_list = [["삼성전자", "005930"],
                ["SK하이닉스", "000660"],
                ["현대차", "005380"],
                ["셀트리온", "068270"],
                ["LG화학", "051910"],
                ["POSCO", "005490"],
                ["삼성물산", "028260"],
                ["NAVER", "035420"]]

    @st.cache
    def get_prices(stock_list):
        df_list = [fdr.DataReader(code, '2022-01-01', '2022-04-30')['Close'] for name, code in stock_list]
        df = pd.concat(df_list, axis=1)
        df.columns = [name for name, code in stock_list]
        return df

    df = get_prices(stock_list)
    st.dataframe(df)
    st.line_chart(df)

    df_norm = df / df.iloc[0] - 1  

    st.bar_chart(df_norm)

    st.area_chart(df_norm)

    df = get_StockListing('KRX-MARCAP')
    st.dataframe(df)
    fig, ax = plt.subplots()
    ax.bar(df.iloc[:10]['Name'], df.iloc[:10]['Marcap'])
    plt.xticks(rotation=90)
    plt.ylabel('Market Cap')
    plt.xlabel('Companies')

    st.pyplot(fig)

if a == 'Exercise 1)':
    with st.sidebar:
        st.markdown('''
        
        ### Exercise 1)
        #### 목표: 주식 정보 시각화 하기

        - 페이지의 제목 쓰기
        - `st.expander()` 를 이용해 아래의 내용을 expander 안에 담기
        - 모든 데이터와 차트에 대해 text를 쓰는 명령어를 이용해 간단한 제목 추가
        - 2017-01-01부터 2022-04-30 까지 Apple의 주가 데이터를 `st.dataframe()` 으로 출력
        - `st.line_chart()` 을 이용해 Close, Open, High, Low 가격 그래프 그리기
        - S&P500 에서 4개의 주식종목 데이터를 가져와서 종가 데이터를 이용해 line chart를 그리고, 수익률을 계산하여 area chart 그리기
        - `st.columns()` 을 이용해 3개의 column을 나누어서 각 주식의 가격과 수익률을 `st.metric()` 을 이용해 출력

        ''')


    @st.cache
    def get_price(ticker, start, end):
        df = fdr.DataReader(ticker, start, end)
        return df
    
    @st.cache
    def get_prices(stock_list, start, end):
        df_list = [fdr.DataReader(code, start, end)['Close'] for name, code in stock_list]
        df = pd.concat(df_list, axis=1)
        df.columns = [name for name, code in stock_list]
        return df

    ## To DO
    ##########################################################

    st.write('#### :information_source: 주식 정보 시각화하기')
    with st.expander('click', expanded=True):

        stock_list = [["Tesla", "TSLA"], ["Amazon", "AMZN"], ['Google', 'GOOGL']]

        df = get_prices(stock_list, '2017-01-01', '2022-04-30')
        df_norm = df / df.iloc[0] - 1
        st.line_chart(df)

        st.area_chart(df_norm)

        df_norm = df_norm.round(3) * 100
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Tesla', '$' + str(df.iloc[-1]['Tesla']), str(df_norm.iloc[-1]['Tesla']) + '%')
        with col2:
            st.metric('Amazon', '$' + str(df.iloc[-1]['Amazon']), str(df_norm.iloc[-1]['Amazon']) + '%')
        with col3:
            st.metric('Google', '$' + str(df.iloc[-1]['Google']), str(df_norm.iloc[-1]['Google']) + '%')

     
    ########################################################################

if a == 'Interactions':

    st.header('4. Interactions')
    st.info(''' 
    - You can check other input widgets in [here](https://docs.streamlit.io/library/api-reference/widgets) ''')

    var = st.selectbox('Select box', ['A', 'B', 'C'])
    if var:
        st.write('You selected', var)

    fruits = st.multiselect('Multiselect Box', ['banana', 'apple', 'strawberry', 'kiwi'])

    if fruits:
        st.write('You selected :', fruits)
        st.write('data type :', type(fruits))

    size = st.select_slider('Select slider', ['S', 'M', 'L', 'XL'])
    with st.expander('result'):
        st.write('You selected :', size)

    st.slider('Slider', 0, 100, 50)

    st.radio('Radio', [1, 2, 3, 4, 5])

    file = st.file_uploader('File uploader')
    with st.expander('result'):
        if file:
            df = pd.read_csv(file)
            st.dataframe(df)

    # picture = st.camera_input('Camera input)
    # with st.expander('picture', expanded=False):
    #   if picture:
    #       st.image(picture)

    with st.form(key='my_form'):
        username = st.text_input('User name')
        password = st.text_input('Password')

        login = st.form_submit_button('login')

    if login:
        if username == password == 'hello':
            st.success('Log-in success!')
        else:
            st.error('Error!')


if a == 'Example 1)':
    st.markdown('''
    #### Example 1) Stock Information
    - Select trade center
    - Select stocks
    - Select start and end date
    - Click get result
    ''')

    @st.cache 
    def get_StockListing(ticker):
        df = fdr.StockListing(ticker)
        return df
    
    @st.cache
    def get_stocklist(df):
        stock_list = []
        for i in range(len(df)):
            name = df.iloc[i]['Name']
            symbol = df.iloc[i]['Symbol']
            stock_list.append([name, symbol])
        return stock_list

    @st.cache
    def get_prices(stock_list, start, end):
        df_list = [fdr.DataReader(code, start, end)['Close'] for name, code in stock_list]
        df = pd.concat(df_list, axis=1)
        df.columns = [name for name, code in stock_list]
        return df
    
  


if a == 'Exercise 2)':
    with st.sidebar:
        st.markdown('''
        
        ### Exercise 2)
        #### 목표: Interactive하게 주식 정보 시각화 하기
        - `st.sidebar` 를 이용해서 interactive widget을 왼쪽에 위치 시키기
        - `st.radio()`를 이용하여 KODEX와 NASDAQ을 선택 widget 만들기
        - `st.form()`을 이용해 form 안에 주식종목들, start date, end date를 입력하는 widget 만들기
        - 주식종목들은 `st.multiselect()`, start date와 end date는 `st.text_input()`를 이용해 생성
        - 정보를 입력하고 click을 할 경우 `st.expander`안에, 
            -  주식 가격들을 `st.line chart()`로 나타내고, column을 나누어서 상관관계를 `st.pyplot()`과 `st.dataframe()`을 이용해 히트맵과 dataframe으로 나타내기
            - 수익률 변화를 `st.area_chart()`로 나타내고, 총 수익률을 `st.table()`로 출력하게 만들기 
        - 페이지 상단에 웹애플리케이션 이름과 사용방법을 적기
        ___
        ''')

    @st.cache 
    def get_StockListing(ticker):
        df = fdr.StockListing(ticker)
        return df
    
    @st.cache
    def get_stocklist(df):
        stock_list = []
        for i in range(len(df)):
            name = df.iloc[i]['Name']
            symbol = df.iloc[i]['Symbol']
            stock_list.append([name, symbol])
        return stock_list

    @st.cache
    def get_prices(stock_list, start, end):
        df_list = [fdr.DataReader(code, start, end)['Close'] for name, code in stock_list]
        df = pd.concat(df_list, axis=1)
        df.columns = [name for name, code in stock_list]
        return df
        
    ## To Do
    ####################################################################
   

    #####################################################################

if a == 'Exercise 3)':

    st.write("""
    # Simple Iris Flower Prediction App
    This app predicts the **Iris flower** type!
    - source : [DataProfessor]('https://github.com/dataprofessor/streamlit_freecodecamp/blob/main/app_7_classification_iris/iris-ml-app.py')
    """)

    st.sidebar.header('User Input Parameters')

    def user_input_features():
        sepal_length = st.sidebar.slider('Sepal length', 4.3, 7.9, 5.4)
        sepal_width = st.sidebar.slider('Sepal width', 2.0, 4.4, 3.4)
        petal_length = st.sidebar.slider('Petal length', 1.0, 6.9, 1.3)
        petal_width = st.sidebar.slider('Petal width', 0.1, 2.5, 0.2)
        data = {'sepal_length': sepal_length,
                'sepal_width': sepal_width,
                'petal_length': petal_length,
                'petal_width': petal_width}
        features = pd.DataFrame(data, index=[0])
        return features


    iris = datasets.load_iris()
    X = iris.data
    Y = iris.target

    clf = RandomForestClassifier()
    clf.fit(X, Y)



    df = user_input_features()
    prediction = clf.predict(df)
    prediction_prob = clf.predict_proba(df)


    st.subheader('User Input parameters')
    st.write(df)

    st.subheader('Class labels and their corresponding index number')
    st.write(iris.target_names)

    st.subheader('Prediction')
    st.write(iris.target_names[prediction])


    st.subheader('Prediction Probabilities')
    st.write(prediction_prob)
    
    # To Do    
    ####################################################################
   

    #####################################################








    

