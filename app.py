from distutils.command.upload import upload
from matplotlib.pyplot import scatter
import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import warnings
warnings.filterwarnings('ignore')

# make layout widw
st.set_page_config(layout="wide")

# load data set
df = pd.read_csv('final_df.csv')

# sidebar with page options
page = st.sidebar.radio(
     "Select Page",
     ('About', 'Exploratory Data Analysis', 'Alzheimer\'s Disease Prediction'))


# about section
if page=='About':

    st.title('About Dataset')
    st.header('Context:')
    st.write("""The Open Access Series of Imaging Studies (OASIS) is a project aimed at making MRI data sets of the brain freely available to the scientific community. By compiling and freely distributing MRI data sets, we hope to facilitate future discoveries in basic and clinical neuroscience. OASIS is made available by the Washington University Alzheimer’s Disease Research Center, Dr. Randy Buckner at the Howard Hughes Medical Institute (HHMI)( at Harvard University, the Neuroinformatics Research Group (NRG) at Washington University School of Medicine, and the Biomedical Informatics Research Network (BIRN).""")
    st.header('Content:')
    st.write("""
Cross-sectional MRI Data in Young, Middle Aged, Nondemented and Demented Older Adults: This set consists of a cross-sectional collection of 416 subjects aged 18 to 96. For each subject, 3 or 4 individual T1-weighted MRI scans obtained in single scan sessions are included. The subjects are all right-handed and include both men and women. 100 of the included subjects over the age of 60 have been clinically diagnosed with very mild to moderate Alzheimer’s disease (AD). Additionally, a reliability data set is included containing 20 nondemented subjects imaged on a subsequent visit within 90 days of their initial session.
Longitudinal MRI Data in Nondemented and Demented Older Adults: This set consists of a longitudinal collection of 150 subjects aged 60 to 96. Each subject was scanned on two or more visits, separated by at least one year for a total of 373 imaging sessions. For each subject, 3 or 4 individual T1-weighted MRI scans obtained in single scan sessions are included. The subjects are all right-handed and include both men and women. 72 of the subjects were characterized as nondemented throughout the study. 64 of the included subjects were characterized as demented at the time of their initial visits and remained so for subsequent scans, including 51 individuals with mild to moderate Alzheimer’s disease. Another 14 subjects were characterized as nondemented at the time of their initial visit and were subsequently characterized as demented at a later visit.""")

# EDA section
if page=='Exploratory Data Analysis':
    st.title('Exploratory Data Analysis')
    st.header('About the Sample')

    # creating 2 column layout for dropdowns
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # pie chart dropdown
    with col1:
        pie_chart_options = st.selectbox(label='Select Variable', options=['Group', 'M/F'])

    # histogram dropdown 
    with col2:
        num_dist_plot_options = st.selectbox(label='Select Variable', options=['Age', 'EDUC', 'eTIV'])

    # pie chart for gender and group
    with col3:
        # distribution pie chart
        df3 = df[[pie_chart_options]+['Subject ID']].groupby(pie_chart_options).count().reset_index()
        #  Use `hole` to create a donut-like pie chart
        fig4 = go.Figure(data=[go.Pie(labels=df3[pie_chart_options], values=df3['Subject ID'], hole=.3)])
        fig4.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=450, width=450)
        st.plotly_chart(fig4, use_container_width=True)

    # histogram for numerical variables
    with col4:
        # Age distplot
        # Create distplot with custom bin_size
        fig4 = ff.create_distplot([df[num_dist_plot_options]], [num_dist_plot_options], show_hist=True, show_rug=False, show_curve=False)
        fig4.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=450, width=450)
        st.plotly_chart(fig4, use_container_width=True)

    # 2 column layout
    col5, col6 = st.columns(2)


    # bar chart count of socio economic status
    with col5:
        df4 = df[['Subject ID', 'SES']].groupby('SES').count().reset_index()
        fig6 = px.bar(df4, x="SES", y="Subject ID", labels={'SES':'Socio-Economic Status', 'Subject ID':'Count'})
        fig6.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=450)
        st.plotly_chart(fig6, use_container_width=True)

    # bar chart for number of visits
    with col6:
        df5 = df[['Subject ID', 'Visit']][df['Group']=='Demented'].groupby('Visit').count().reset_index()
        fig7 = px.bar(df5, x="Visit", y="Subject ID", labels={'Subject ID':'Count'})
        fig7.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=450)
        st.plotly_chart(fig7, use_container_width=True)
        


    st.header('Deep Dive and Findings')

    st.subheader('Distribution of Different Variables and Variation with Age')

    # 2 column layout for charts and dropdowns
    col7, col8 = st.columns(2)
    col9, col10 = st.columns(2)

    # distplot dropdwon
    with col7:
        distplot_options = st.selectbox(label='Select Variable', options=['Age', 'eTIV', 'nWBV', 'EDUC'])
    
    # scatter plot dropdown
    with col8:
        scatter_plot_options_2 = st.selectbox(label='Select Variable', options=['nWBV','eTIV'], key='2')

    # distplot chart for different variables
    with col9:
        # Create distplot with custom bin_size
        hist_data = [list(df[distplot_options][df['Group']=='Demented']), list(df[distplot_options][df['Group']=='Nondemented'])]
        group_labels = ['Demented', 'Non-Demented']
        fig2 = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False)
        fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=450, width=450)
        st.plotly_chart(fig2, use_container_width=True)

        if distplot_options=='Age':
            caption_1 = """There's a higher percentage of demented patients between the ages of 65 and 75."""
        
        elif distplot_options=='EDUC':
            caption_1 = """Demented patients tend to have lower education (10-15 years of education) than non-demented patients (15+ years of education)."""
        
        elif distplot_options=='nWBV':
            caption_1 = """Dementia can associated with smaller brain volume as there's a higher percentage of demented patients in the low spectrum of brain volume values."""

        elif distplot_options=='eTIV':
            caption_1 = """For abnormal levels of intracranial volume (<1450 cm^3) the percentage of demented patients is higher"""

        if caption_1:
            st.caption(caption_1)

    
    # scatter plot with trendlines for age vs brain volume and intracranial volume
    with col10:
        # scatter plot
        trendline = 'ols' if scatter_plot_options_2=='nWBV' else 'lowess'
        fig5 = px.scatter(df, x='Age', y=scatter_plot_options_2, color='Group', trendline=trendline)
        fig5.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=450, width=450)
        st.plotly_chart(fig5, use_container_width=True)
        caption_2 = 'As we age our brains shrink in volume, however the amount of shrinkage is more significant for demented patients.' if scatter_plot_options_2=='nWBV' else 'The intracranial volume of demented and non-demented patients approaches almost the same values in later age. However the intracranial volume of demented patients decreases with time while it increases for non-demented patients.'
        st.caption(caption_2)

    # group by gender
    st.subheader('Gender and Dementia')
    # Gender X Group
    df1 = df[['Group', 'M/F', 'Subject ID']].groupby(['Group', 'M/F']).count().reset_index()
    fig1 = px.bar(df1, x="Group", y="Subject ID", color="M/F", barmode="group", labels={'Subject ID':'Count'})
    fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=450)
    st.plotly_chart(fig1, use_container_width=True)
    st.caption('Males are more likely to get Alzheimer\'s disease.')

# prediction page
if page=='Alzheimer\'s Disease Prediction':
    st.title('Input Your MRI results to Get a Diagnosis')
    st.subheader('This model has an accuracy of 74%')

    # load model
    lr = joblib.load('model.joblib')

    # upload data
    uploaded_file = st.file_uploader('Load CSV file')

    if uploaded_file:

        # read data
        df_ml = pd.read_csv(uploaded_file)

        # generate predictions and probabilities
        outcome = lr.predict(df_ml)[0]
        outcome_probability = round(max(lr.predict_proba(df_ml)[0])*100, 1)

        st.write(f"There's a {outcome_probability}% that you are {outcome}")
    

    

