import pandas as pd
import numpy as np
import plotly.express as px


#read the data from csv file filled with available market caps
df=pd.read_csv('mkt_caps.csv')
#fill NA where market cap not available
df.Mcap.fillna('NA', inplace=True)
#new colum adjusted marketcap
df['adjmcap']=df.Mcap.apply(lambda x:1 if x=='NA' else 1 if x<1 else x)

#adding super container for entire treemap
df['perf']='Market Performance'

fig = px.treemap(df,path=['perf','Sector', 'Industry','Symbol'],
                 values='adjmcap',
                 names='Change',
                 color='Change',
                color_continuous_scale='RdYlGn',
                color_continuous_midpoint=0)    #np.average(df['Change'], weights=df['adjmcap'])

#save image
fig.write_image("fig1.png", height=800, width=1200)

#disable hover-mode
fig.layout.hovermode = False

#disable color axis
fig.update_layout(coloraxis_showscale=False)

#Add customdata to label (Change percentage)
fig.data[0].customdata = np.column_stack([df.Change])#np.column_stack([salaries, percents])
fig.data[0].texttemplate = "%{label}<br>%{customdata[0]}%"

#show fig
fig.show()