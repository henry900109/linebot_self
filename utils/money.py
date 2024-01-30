import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
def draw():
    matplotlib.rc('font', family='Microsoft JhengHei')


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
        df['日期'] = pd.to_datetime(df['日期'], format='%m/%d')
        

        # 繪製折線圖
        plt.figure(figsize=(10, 6))
        plt.plot(result_df['日期'], result_df['淨值'],label='淨值' ,  color='r')
        plt.title('統一奔騰')
        plt.xlabel('Data')
        plt.ylabel('Price')
        plt.xticks(result_df['日期'][::2], rotation=45)
        plt.yticks(result_df['淨值'][::2])
        plt.gca().invert_xaxis()  # 將 x 軸數據反轉
        plt.gca().invert_yaxis()  # 將 y 軸數據反轉
        plt.grid(True)
        plt.tight_layout()

        plt.legend()
         # 將圖片轉換為二進制數據
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        # 清除Matplotlib繪圖狀態，以便可以進行下一次繪圖
        plt.clf()
    
        return img_buffer.getvalue()
    except Exception as e:
        print(e)


