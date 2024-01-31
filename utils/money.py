import pandas as pd
from io import BytesIO
def draw():
   


    try:
        # 基本資料
        url = "https://www.moneydj.com/funddj/ya/yp010000.djhtm?a=acps10&topc="

        data = pd.read_html(url)

        data1 = data[5]
        df = pd.DataFrame(data1[1:])
        df = df.rename(columns={0: '日期', 1: '淨值'})
        # print(df)
        data1 = data[6]
        df2 = pd.DataFrame(data1[1:])
        df2 = df2.rename(columns={0: '日期', 1: '淨值'})

        data1 = data[7]
        df3 = pd.DataFrame(data1[1:])
        df3 = df3.rename(columns={0: '日期', 1: '淨值'})

        # # 將多個DataFrame合併成一個
        result_df = pd.concat([df, df2,df3], ignore_index=True)
        # df['日期'] = pd.to_datetime(df['日期'], format='%m/%d')
        

        result_df = result_df.dropna()
    
        result_df['淨值'] = pd.to_numeric(result_df['淨值'], errors='coerce').astype(float)

        result_df = result_df.iloc[::-1, ::-1]

    
        ax = result_df.plot(x='日期', y='淨值', kind='line', color='r', figsize=(10, 6),grid=True,rot = 45 ,title='統一奔騰')

        ax = df.plot()
        fig = ax.get_figure()



        # 將圖片轉換為二進制數據
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png')
        img_buffer.seek(0)
    
    
        return img_buffer.getvalue()
    except Exception as e:
        print(e)


