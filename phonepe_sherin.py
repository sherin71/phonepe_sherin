import pandas as pd
import mysql.connector as sql
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo
import plotly.express as px
import os
import json



# PhonePe logo URL
phonepe_logo_url = "https://download.logo.wine/logo/PhonePe/PhonePe-Logo.wine.png"

# Display the PhonePe logo in the sidebar
st.sidebar.image(phonepe_logo_url, use_column_width=True)

# Sidebar header
st.sidebar.header(":wave: :violet[**Welcome to the dashboard!**]")

# Custom HTML and Markdown for the "About" section with emojis and styling
st.sidebar.markdown(
    """
    <h1 style='color: violet; font-size: 25px;'> 👉About the Creator</h1>
    <p>This dashboard app is created by <strong>sherin</strong></p>
    """,
    unsafe_allow_html=True,
)
# Creating connection with mysql workbench
mydb = sql.connect(host="localhost",
                   user="root",
                   password="stc123",
                   database= "phonepe_pulse"
                  )
mycursor = mydb.cursor(buffered=True)
# #To clone the Github Pulse repository use the following code
# Reference Syntax - Repo.clone_from("Clone Url", "Your working directory")
# Repo.clone_from("https://github.com/PhonePe/pulse.git", "")

# Sidebar image
st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2iXSLAMq-Jzp5oPiBDPDjIvHzMlOoXGm0SA&usqp=CAU", use_column_width=True)

# Define menu options
menu_options = ["🎯 Homepage", "📈 Top Charts", "🔍 Data Exploration", "📚 About"]

# Create a radio button to select the menu option
selected_option = st.sidebar.radio("Menu 🌟", menu_options)

# Display the selected option
st.sidebar.write("You selected:", selected_option)



# Your Streamlit app content based on the selected option
if selected_option == "🎯 Homepage":
    st.markdown("# :violet[📌 Data Visualization & Exploration]", unsafe_allow_html=True)
    st.markdown("## :violet[✨User-Friendly Tool Using Streamlit & Plotly]", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Industry Focus :] 💻💰Online Banking", unsafe_allow_html=True)
        st.markdown("### :violet[Tech Stack :] 🐍Python, Pandas, 🗃️MySQL, 🚀Streamlit, 📊Plotly &💡more", unsafe_allow_html=True)
        st.markdown("### :violet[Overview :] Explore PhonePe Pulse data and gain insights with interactive visualizations.", unsafe_allow_html=True)
    with col2:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvv_d8kQ_Z6qUBx0vFM7pJCQTQNCgA1ij7ncaiBOLEBrW-PGSaWk6ZmOltk2Qs91Zw2l0&usqp=CAU")
# Add more options for other menu items (Top Charts, Data Exploration, About) similarly.


# MENU 2 - TOP CHARTS
if selected_option == "📈 Top Charts":
    st.markdown("## :violet[📈 Top Charts]")
    Type = st.sidebar.radio("**Type**", ("🏧Transactions", "👧Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    with colum2:
        st.image("https://techcrunch.com/wp-content/uploads/2021/09/phonepe-pulse.jpg", use_column_width=True)
        st.markdown(
        """
        ## :violet[🎇 Insights 🎇]

         :violet[Explore the data and uncover valuable insights:]

        - :violet[Rank analysis for a specific Year and Quarter.]
        - :violet[Top 10 Regions (State, District, Pincode) based on transaction volume and total spending on PhonePe.]
        - :violet[Top 10 Regions based on the number of PhonePe users and their app usage frequency.]
        - :violet[Discover the top mobile brands and their market share among PhonePe users.]
        """,
        unsafe_allow_html=True
    )
        

    # Top Charts - TRANSACTIONS    
    if Type == "🏧Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("### :violet[🗺️State]")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10 🎈',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
        with col2:
            st.markdown("### :violet[🏙️District]")
            mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10 🎈',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
    
        with col3:
            st.markdown("### :violet[📱Pincode]")
            mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10 🎈',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
    

    # Top Charts - USERS          
    if Type == "👧Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :violet[🎆Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10 🎈',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   

        with col2:
            st.markdown("### :violet[🏙️District]")
            mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10 🎈',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True) 

        with col3:
            st.markdown("### :violet[📱Pincode]")
            mycursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10 🎈',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')     
            st.plotly_chart(fig,use_container_width=True) 

        with col4:
            st.markdown("### :violet[🗺️State]")
            mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10 🎈',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label') 
            st.plotly_chart(fig,use_container_width=True)

        # MENU 3 - EXPLORE DATA
if selected_option == "🔍 Data Exploration":
  Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
  Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
  Type = st.sidebar.radio("**Type**", ("Transactions", "Users"))
  col1,col2 = st.columns(2)  


  if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - 💵Transactions Amount💰]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
        

        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall 🌏State Data - Transactions Count 👨‍💻]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment 📱 Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])
        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)    
        

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA     
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more 🎇]")
        selected_state = st.radio("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

    # EXPLORE DATA - USERS      
  if Type == "Users":
    # Overall State Data - TOTAL APPOPENS - INDIA MAP
    st.markdown("## :violet[Overall State Data - User App opening frequency]")
    mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
    df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
    df2 = pd.read_csv('Statenames.csv')
    df1.Total_Appopens = df1.Total_Appopens.astype(float)
    df1.State = df2
    fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='sunset')
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig,use_container_width=True)

    # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
    st.markdown("## :violet[Select any State to explore more]")
    selected_state = st.radio("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
    mycursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
    df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
    df.Total_Users = df.Total_Users.astype(int)
        
    fig = px.bar(df,
                 title=selected_state,
                 x="District",
                 y="Total_Users",
                 orientation='v',
                 color='Total_Users',
               color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig,use_container_width=True)
if selected_option == "📚 About":
    col1, col2 = st.columns([3, 3], gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse 🎇:]")
        st.write("##### PhonePe Pulse, launched on September 3, 2021, is India's first interactive website offering data, insights, and trends on digital payments. It showcases over 2000 Crore transactions on an interactive map of India. With a market share of over 45%, PhonePe's data reflects the digital payment habits of the nation.")
        
        st.write("##### :violet[The insights on the website and in the report are derived from PhonePe's transaction data and interviews with merchants and customers. The report is available for free download on the PhonePe Pulse website and GitHub.]")
        
        st.markdown("### :violet[About PhonePe 🎇:]")
        st.write("##### PhonePe is India's leading fintech platform with more than 300 million registered users. Users can send and receive money, recharge mobile, pay at stores, make utility payments, buy gold, and invest. Since 2017, PhonePe has expanded into financial services, offering products like gold purchases, mutual funds, and insurance. The platform also features PhonePe Switch, allowing customers to place orders on over 600 apps. PhonePe is accepted at over 20 million merchant outlets across India.")

    with col2:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOBMaRjGrPV4_i_EmMwIYlJ-5reXh4ZppkJY38sDDjeG-K9led6Ipuk-XKEl-nHXZz758&usqp=CAU")
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfIu6Tby2e3iGVSH6HplcvR95EjYA0YalLiPeikMnMH4gkOGi0g4plUA2bWhFK9RKWst8&usqp=CAU")
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBxTBDRGhPe4w_4N_xdrw9lYaouJKPEKtoFw&usqp=CAU")