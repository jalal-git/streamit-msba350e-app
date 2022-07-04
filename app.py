import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

import warnings
warnings.filterwarnings('ignore')

st.write('Hello World')

df = pd.read_csv('final_df.csv')

# Gender X Group
df1 = df[['Group', 'M/F', 'Subject ID']].groupby(['Group', 'M/F']).count().reset_index()
fig1 = px.bar(df1, x="Group", y="Subject ID", color="M/F")
st.plotly_chart(fig1)

# Age distplot
# Create distplot with custom bin_size
fig4 = ff.create_distplot([df['Age']], ['Age'], show_hist=True, show_rug=False, show_curve=False)
st.plotly_chart(fig4)

# Distplot
distplot_options = st.selectbox(label='Select feautre', options=['ASF', 'eTIV', 'nWBV', 'Age', 'EDUC'])

hist_data = [list(df[distplot_options][df['Group']=='Demented']), list(df[distplot_options][df['Group']=='Nondemented'])]
group_labels = ['Demented', 'Non-Demented']


# Create distplot with custom bin_size
fig2 = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False)
st.plotly_chart(fig2)

# corr heatmap

df2 = df[['Age', 'EDUC', 'SES', 'MMSE', 'CDR','eTIV', 'nWBV', 'ASF']].corr()
fig3 = px.imshow(df2)
st.plotly_chart(fig3)
