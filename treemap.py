import pandas as pd
import numpy as np
import plotly.express as px


#read the data from csv file filled with available market caps
#df=pd.read_csv('mkt_caps.csv')
df=pd.read_csv('mkt_caps_decimal.csv')

#fill NA where market cap not available
df.Mcap.fillna('NA', inplace=True)

#new colum adjusted marketcap
df['adjmcap']=df.Mcap.apply(lambda x:1 if x=='NA' else 1 if x<1 else x)

#Finviz Colorscheme
df['cat_change']=df.Change.apply(lambda x: '3pl' if x>3 else '2pl' if x>2 else '1pl' if x>1 else 'zero' if x>-1 else '1min'if x>-2 else '2min' if x>-3 else '3min' )
disc_map={'(?)':'black', '3min': '#FF0000','2min': "#CD5C5C",'1min':"#8B0000", 
          'zero':"#696969", '1pl':"#556B2F",  '2pl':"#228B22",'3pl':"#32CD32"}

#Add new column for continuous code
disc_code={'3pl':7,'2pl':6,'1pl':5, 'zero':4, '1min':3,  '2min':2,  '3min':1}
df['disc_code']=df.cat_change.apply(lambda x:disc_code[x])

#Continuous color scale
scale=[(0.00, "#FF0000"),   (0.14285714, "#FF0000"),
       (0.14285714, "#CD5C5C"), (0.28571429, "#CD5C5C"),
       (0.28571429, "#8B0000"), (0.42857143, "#8B0000"),
       (0.42857143, "#696969"), (0.57142857, "#696969"),
       (0.57142857, "#556B2F"), (0.71428571, "#556B2F"),
       (0.71428571, "#228B22"), (0.85714286, "#228B22"),
       (0.85714286, "#32CD32"),  (1.00, "#32CD32")]

#adding super container for entire treemap
df['perf']='Market Performance'

#sort values
df.sort_values(by=['Symbol', 'Industry','Sector'],inplace=True)

#Generate treemap
fig = px.treemap(df,
                 path=['perf','Sector', 'Industry','Symbol'],
                 values='adjmcap',
                 color='disc_code',
                 range_color=[0.5, 7.5],
                 color_continuous_scale=scale)

#Generate color bar
fig.update_layout(coloraxis_colorbar=dict(
    title="Change",
    tickvals=[1,2,3,4,5,6,7],
    ticktext=["-3%","-2%","-1%","0","1","2","3"],
    lenmode="pixels", len=300,
))


#disable hover-mode
fig.layout.hovermode = False

#disable color axis
#fig.update_layout(coloraxis_showscale=False)

#Add customdata to label (Change percentage)
fig.data[0].customdata = np.column_stack([df.Change])
fig.data[0].texttemplate = "%{label}<br><b>%{customdata[0]}%</b>"

#save image
fig.write_image("fig1.png", height=800, width=1200)

#show fig
fig.show()