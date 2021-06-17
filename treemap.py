import pandas as pd
import numpy as np
import plotly.express as px


#read the data from csv file filled with available market caps
df=pd.read_csv('mkt_caps.csv')
#fill NA where market cap not available
df.Mcap.fillna('NA', inplace=True)
#new colum adjusted marketcap
df['adjmcap']=df.Mcap.apply(lambda x:1 if x=='NA' else 1 if x<1 else x)

#Finviz Colorscheme
df['cat_change']=df.Change.apply(lambda x: '3pl' if x>3 else '2pl' if x>2 else '1pl' if x>1 else 'zero' if x>-1 else '1min'if x>-2 else '2min' if x>-3 else '3min' )
disc_map={'(?)':'black', '3min': '#FF0000','2min': "#CD5C5C",'1min':"#8B0000", 
          'zero':"#696969", '1pl':"#556B2F",  '2pl':"#228B22",'3pl':"#32CD32"}

#adding super container for entire treemap
df['perf']='Market Performance'

fig = px.treemap(df,path=['perf','Sector', 'Industry','Symbol'],
                 values='adjmcap',
                 color='cat_change',
                color_discrete_map=disc_map)   

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