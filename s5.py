import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid,GridOptionsBuilder

st.set_page_config(page_title="CybArena",page_icon="🪪",layout="wide")

st.markdown("""
<style>

.stApp{
    background-color:#0D1117;
}

h1{
    color:#00FFFF;
    text-align:center;
}

h2,h3{
    color:#00E5FF;
}

div[data-testid="stMetric"]{
    background-color:#161B22;
    border:2px solid #00FFFF;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 0px 10px cyan;
}

section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#101820,#161B22,#0D1117);
    border-right:2px solid #00FFFF;
    box-shadow:0 0 20px #00FFFF;
}

section[data-testid="stSidebar"]{
    background-color:#161B22;
}

/* ---------- AGGRID TABLE ---------- */

.ag-root-wrapper{
    border:2px solid #00FFFF !important;
    border-radius:15px !important;
    box-shadow:0 0 10px cyan,
               0 0 20px cyan,
               0 0 35px cyan !important;
}

.ag-header{
    background:#00FFFF !important;
    color:black !important;
    font-weight:bold !important;
}

.ag-row{
    background:#161B22 !important;
    color:white !important;
}

.ag-row:hover{
    background:#0F2E4E !important;
}

.ag-cell{
    border-color:#00FFFF33 !important;
}

</style>
""",unsafe_allow_html=True)

with st.spinner("🛡️ Loading Cyber Intelligence Dashboard..."):
    df = pd.read_csv("Global_Cybersecurity_Threats.csv")
    
    st.toast("✅ Cyber Intelligence Loaded Successfully!", icon="🛡️")

with st.sidebar:
        st.markdown("""
<h2 style="text-align:center;color:#00FFFF;">
🛡️ CybArena
</h2>
<p style="text-align:center;color:white;font-size:14px;">
Cyber Intelligence Center
</p>
""", unsafe_allow_html=True)
        selected=option_menu(menu_title="Main Menu",
        options=["Home","Data-set","Graphs","Attack Guide","About"],icons=["house","table","graph-up-arrow","shield lock","person"],default_index=0)

# ---------------------------------------------- H O M E ------------------------------------------

if selected=="Home":
    st.markdown("""
<style>

.stApp{
    background:#0D1117;
}

[data-testid="stAppViewContainer"]{
    background-image:
    linear-gradient(rgba(13,17,23,0.65), rgba(13,17,23,0.65)),
    url("https://as1.ftcdn.net/v2/jpg/07/95/10/80/1000_F_795108041_6TJyPROjH4cHUYGttdu2vPym9WaXblEm.jpg");

    background-size:cover;
    background-position:center;
    background-repeat:no-repeat;
    background-attachment:fixed;
}

</style>
""", unsafe_allow_html=True)
    st.markdown("""
<h1 style="text-align:center; color:#00FFFF;">
🛡️ CybArena
</h1>

<h3 style="text-align:center; color:white;">
Cyber Threat Intelligence Dashboard
</h3>
""", unsafe_allow_html=True)
    
    current_time = datetime.now().strftime("%d %b %Y | %I:%M %p")

    st.markdown(
    f"""
    <div style="text-align:right; color:#00FFFF; font-size:16px;">
        🕒 {current_time}
    </div>
    """,
    unsafe_allow_html=True
)

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        st.metric("🌍 Countries", df["Country"].nunique())

    with col2:
        st.metric("🛡️ Attack Types", df["Attack Type"].nunique())

    with col3:
        st.metric(
            "👥 Affected Users",
            f'{df["Number of Affected Users"].sum():,}'
        )

    with col4:
        st.metric(
            "💰 Financial Loss ($M)",
            f'{df["Financial Loss (in Million $)"].sum():,.2f}'     
        )
        
    with col5:
        st.metric(
            "🏭 Industries",
            df["Target Industry"].nunique()
        )
        
    with col6:
        st.metric(
            "📆 Years",
            df["Year"].nunique()
        )
    
    st.markdown("""
### 📌 Project Overview
    """)
    st.warning("""
        CybArena is an interactive Cyber Threat Intelligence Dashboard that analyzes global cybersecurity incidents. It helps users explore attack trends, financial losses, affected users, and target industries through interactive visualizations and filters.
    """)

    st.markdown("## 🏆 Top 5 Attack Types")

    top_attacks = (
    df["Attack Type"]
    .value_counts()
    .head(5)
    .reset_index()
)

    top_attacks.columns = ["Attack Type", "Count"]

    fig = px.bar(
    top_attacks,
    x="Count",
    y="Attack Type",
    orientation="h",
    color="Count",
    title="Most Frequent Cyber Attacks"
)

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("## 🌍 Top 10 Countries by Financial Loss")

    top_countries = (
    df.groupby("Country")["Financial Loss (in Million $)"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

    fig_country = px.bar(
    top_countries,
    x="Financial Loss (in Million $)",
    y="Country",
    orientation="h",
    color="Financial Loss (in Million $)",
    title="Top 10 Countries by Financial Loss"
)

    fig_country.update_layout(yaxis={"categoryorder": "total ascending"})

    st.plotly_chart(fig_country, use_container_width=True)
    
    st.markdown("## 📌 Key Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"""
🌍 **Most Targeted Country:**  
**{df['Country'].value_counts().idxmax()}**
""")

    st.info(f"""
🛡️ **Most Common Attack:**  
**{df['Attack Type'].value_counts().idxmax()}**
""")

    with col2:
        st.info(f"""
🏭 **Most Targeted Industry:**  
**{df['Target Industry'].value_counts().idxmax()}**
""")

    st.info(f"""
📅 **Latest Year in Dataset:**  
**{df['Year'].max()}**
""")
    
    st.markdown("## ⚡ Cyber Threat Snapshot")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(f"🌍 Countries Covered: {df['Country'].nunique()}")

    with col2:
        st.warning(f"🛡️ Attack Types: {df['Attack Type'].nunique()}")

    with col3:
        st.error(f"💰 Total Loss: ${df['Financial Loss (in Million $)'].sum():,.2f} Million")
        
   
   
    st.markdown("## 🌍 Global Cyber Threat Hotspots")

    country_loss = (
    df.groupby("Country")["Financial Loss (in Million $)"]
    .sum()
    .reset_index()
)

    fig_map = px.scatter_geo(
    country_loss,
    locations="Country",
    locationmode="country names",
    size="Financial Loss (in Million $)",
    color="Financial Loss (in Million $)",
    hover_name="Country",
    hover_data={
        "Financial Loss (in Million $)":":,.2f"
    },
    projection="orthographic",      # Globe View
    color_continuous_scale="Turbo",
    title="Global Cyber Threat Hotspots"
)

    fig_map.update_traces(
    marker=dict(
        opacity=0.85,
        line=dict(color="#00FFFF", width=1.5)
    )
)

    fig_map.update_geos(
    bgcolor="#0D1117",
    showland=True,
    landcolor="#16213E",
    showocean=True,
    oceancolor="#08131F",
    showcountries=True,
    countrycolor="#00FFFF",
    coastlinecolor="#00FFFF",
    showframe=False,
)

    fig_map.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0D1117",
    plot_bgcolor="#0D1117",
    font=dict(color="white"),
    title_font=dict(size=24, color="#00FFFF"),
    margin=dict(l=0, r=0, t=50, b=0),
    coloraxis_colorbar=dict(
        title="Loss ($M)"
    )
)

    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    st.caption("Developed by Sonali | CybArena | B.Tech AIML")
    
# --------------------------------- D A T A - S E T ------------------------------------

elif selected == "Data-set":

    st.write(f"**Rows:** {df.shape[0]}")
    st.write(f"**Columns:** {df.shape[1]}")

    st.subheader("📂 Dataset Controls")

    rows = st.slider(
        "Select number of rows to display",
        min_value=10,
        max_value=len(df),
        value=100,
        step=10
    )

    # ---------------- FILTERS ----------------

    col1, col2, col3 = st.columns(3)

    with col1:
        country = st.selectbox(
            "🌍 Country",
            ["All"] + sorted(df["Country"].unique())
        )

    with col2:
        attack = st.selectbox(
            "🛡️ Attack Type",
            ["All"] + sorted(df["Attack Type"].unique())
        )

    with col3:
        year = st.selectbox(
            "📅 Year",
            ["All"] + sorted(df["Year"].unique())
        )

    filtered_df = df.copy()

    if country != "All":
        filtered_df = filtered_df[
            filtered_df["Country"] == country
        ]

    if attack != "All":
        filtered_df = filtered_df[
            filtered_df["Attack Type"] == attack
        ]

    if year != "All":
        filtered_df = filtered_df[
            filtered_df["Year"] == year
        ]

    # ---------------- DOWNLOAD BUTTON ----------------

    st.download_button(
        label="📥 Download Filtered Dataset",
        data=filtered_df.to_csv(index=False),
        file_name="Filtered_Cyber_Threats.csv",
        mime="text/csv"
    )

    # ---------------- TABS ----------------

    t1, t2, t3 = st.tabs(["📂 Data", "ℹ️ Info", "📊 Summary"])

    # ================= DATA TAB =================

    with t1:

        st.markdown("""
        <h2 style="color:#00FFFF;">
        📂 Dataset Explorer
        </h2>
        """, unsafe_allow_html=True)

        search = st.text_input("🔍 Search Country")

        display_df = filtered_df.copy()

        if search:
            display_df = display_df[
                display_df["Country"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        display_df = display_df.head(rows)

        gb = GridOptionsBuilder.from_dataframe(display_df)

        gb.configure_default_column(
            filter=True,
            sortable=True,
            resizable=True
        )

        grid_options = gb.build()

        AgGrid(
            display_df,
            gridOptions=grid_options,
            height=500,
            fit_columns_on_grid_load=True,
            theme="streamlit"
        )

    # ================= INFO TAB =================

    with t2:

        st.write("### 📋 Dataset Information")

        st.write("**Rows:**", len(filtered_df))
        st.write("**Columns:**", filtered_df.shape[1])

        st.write("### 📝 Column Names")
        st.write(list(filtered_df.columns))

        st.write("### ❌ Missing Values")
        st.write(filtered_df.isnull().sum())

        st.write("### 🔤 Data Types")
        st.write(filtered_df.dtypes)

    # ================= SUMMARY TAB =================

    with t3:

        st.subheader("📊 Statistical Summary")

        st.dataframe(filtered_df.describe())
        
    st.markdown("---")
    st.caption("Developed by Sonali | CybArena | B.Tech AIML")

# --------------------------------- G R A P H S  ------------------------------------
    
elif selected=="Graphs":

    graph_df = df.copy()

    graph_df.dropna(inplace=True)
    graph_df.reset_index(drop=True, inplace=True)

    country = st.sidebar.selectbox(
    "🌍 Select Country",
    ["All"] + sorted(graph_df["Country"].unique())
)

    if country != "All":
        graph_df = graph_df[graph_df["Country"] == country]

    attack = st.sidebar.selectbox(
    "🛡️ Select Attack Type",
    ["All"] + sorted(graph_df["Attack Type"].unique())
)

    if attack != "All":
        graph_df = graph_df[graph_df["Attack Type"] == attack]
        
    year = st.sidebar.selectbox(
    "📅 Select Year",
    ["All"] + sorted(graph_df["Year"].unique())
)

    if year != "All":
        graph_df = graph_df[graph_df["Year"] == year]
        
    st.download_button(
    label="📥 Download Filtered Dataset",
    data=graph_df.to_csv(index=False),
    file_name="Filtered_Cyber_Threats.csv",
    mime="text/csv"
)
    
    
    ##################################################
    # STREAMLIT
    ##################################################

    st.markdown("## 📊 Data Visualizations")

# Bar Chart
    fig1 = px.bar(
        graph_df,
        x="Country",
        y="Number of Affected Users",
        color="Attack Type",
        title="Affected Users by Country"
)
    st.plotly_chart(fig1, use_container_width=True)

# Line Chart
    fig2 = px.line(
        graph_df,
        x="Year",
        y="Financial Loss (in Million $)",
        color="Country",
        title="Financial Loss Over Years"
)
    st.plotly_chart(fig2, use_container_width=True)

# Scatter Plot
    fig3 = px.scatter(
        graph_df,
        x="Financial Loss (in Million $)",
        y="Number of Affected Users",
        color="Attack Type",
        size="Financial Loss (in Million $)",
        hover_data=["Country"],
        title="Financial Loss vs Affected Users"
)
    st.plotly_chart(fig3, use_container_width=True)

# Area Chart
    fig4 = px.area(
        graph_df,
        x="Year",
        y="Number of Affected Users",
        color="Country",
        title="Affected Users Trend"
)
    st.plotly_chart(fig4, use_container_width=True)

# 3D Scatter
    fig5 = px.scatter_3d(
        graph_df,
        x="Year",
        y="Financial Loss (in Million $)",
        z="Number of Affected Users",
        color="Attack Type",
        title="3D Cyber Threat Analysis"
)
    st.plotly_chart(fig5, use_container_width=True)

# Pie Chart
    fig6 = px.pie(
        graph_df,
        names="Attack Type",
        values="Number of Affected Users",
        title="Attack Type Distribution"
)
    st.plotly_chart(fig6, use_container_width=True)

# Sunburst Chart
    fig7 = px.sunburst(
        graph_df,
        path=["Country", "Attack Type"],
        values="Number of Affected Users",
        title="Country → Attack Type"
)
    st.plotly_chart(fig7, use_container_width=True)

# Matplotlib
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(graph_df["Country"], graph_df["Number of Affected Users"])
    plt.xticks(rotation=90)
    plt.title("Affected Users by Country")
    st.pyplot(fig) 

    st.markdown("---")
    st.caption("Developed by Sonali | CybArena | B.Tech AIML")
        
        
# ---------------------------------A T T A C K -T Y P E --------------------------------------------

        
elif selected=="Attack Guide":

    st.title("🛡️ Cyber Attack Guide")
    st.write("Learn about different cyber attacks, their impact, and how to prevent them.")

    attack = st.selectbox(
        "Select an Attack Type",
        sorted(df["Attack Type"].dropna().unique())
    )
    st.write(attack)
    attack_info = {

    "Phishing": {
        "description": "Phishing is a social engineering attack where cybercriminals trick users into revealing sensitive information through fake emails, websites, or messages.",
        "target": "Individuals, Employees, Banking Customers",
        "impact": "Credential theft, Financial fraud, Identity theft",
        "prevention": "Verify email senders, avoid clicking suspicious links, enable Multi-Factor Authentication (MFA), and never share passwords."
    },

    "Ransomware": {
        "description": "Ransomware encrypts files or systems and demands a ransom payment to restore access.",
        "target": "Businesses, Hospitals, Government Organizations",
        "impact": "Financial loss, Data loss, Business downtime",
        "prevention": "Maintain regular backups, update software, use antivirus software, and avoid downloading unknown files."
    },

    "DDoS": {
        "description": "A Distributed Denial-of-Service (DDoS) attack floods a server or network with excessive traffic, making services unavailable to legitimate users.",
        "target": "Websites, Online Services, Enterprises",
        "impact": "Service disruption, Revenue loss, Customer dissatisfaction",
        "prevention": "Use firewalls, Content Delivery Networks (CDNs), traffic filtering, and rate limiting."
    },

    "SQL Injection": {
        "description": "SQL Injection is a web attack where attackers inject malicious SQL queries to access, modify, or delete database information.",
        "target": "Database-driven Websites and Web Applications",
        "impact": "Data theft, Database corruption, Unauthorized access",
        "prevention": "Use parameterized queries, validate user input, and implement prepared statements."
    },

    "Malware": {
        "description": "Malware is malicious software designed to damage systems, steal information, or gain unauthorized access to devices.",
        "target": "Computers, Mobile Devices, Networks",
        "impact": "Data theft, System damage, Spyware installation, Unauthorized access",
        "prevention": "Install antivirus software, keep operating systems updated, and avoid downloading suspicious files."
    },

    "Man-in-the-Middle": {
        "description": "A Man-in-the-Middle (MitM) attack occurs when an attacker secretly intercepts communication between two parties to steal or alter information.",
        "target": "Public Wi-Fi Users, Online Banking, Business Communication",
        "impact": "Data interception, Credential theft, Financial fraud",
        "prevention": "Use HTTPS websites, VPNs, secure Wi-Fi networks, and Multi-Factor Authentication."
    }

}
    
    if attack in attack_info:

        st.markdown(f"## 🔰 {attack}")

        st.info(f"**📖 Description**\n\n{attack_info[attack]['description']}")

        st.warning(f"**🎯 Common Targets**\n\n{attack_info[attack]['target']}")

        st.error(f"**⚠️ Possible Impact**\n\n{attack_info[attack]['impact']}")

        st.success(f"**🛡️ Prevention Tips**\n\n{attack_info[attack]['prevention']}")
        
    st.markdown("---")
    st.caption("Developed by Sonali | CybArena | B.Tech AIML")
    
# --------------------------------------- A B O U T --------------------------------------------

elif selected=="About":
    st.title("About")
    st.markdown("""
## 🛡️ CybArena
CybArena is an interactive Cyber Threat Intelligence Dashboard developed to analyze and visualize global cybersecurity threats.It hepls users understand cyber attack trends, affected industries, financial losses, interactive charts and filters.

### 🎯Project Objective
To provide a user - friendly platform for exploring cybersecurity data and identifying trends using data visualization techniques.

### ✨ Key Features
- 📊 Interactive Dashboard
- 🌍 Country-wise Analysis
- 🛡️ Attack Type Filtering
- 📆 Year-wise Analysis

- 📈 Streamlit, Plotly & Matplotlib Visualizations
""")
    st.markdown("## 🛠️ Technologies Used")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg", width=70)
        st.caption("Python")

    with col2:
        st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=70)
        st.caption("Streamlit")

    with col3:
        st.image("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg", width=70)
        st.caption("Pandas")

    with col4:
        st.image("https://images.plot.ly/logo/new-branding/plotly-logomark.png", width=70)
        st.caption("Plotly")

    with col5:
        st.image("https://matplotlib.org/stable/_images/sphx_glr_logos2_001.png", width=70)
        st.caption("Matplotlib")

    
    st.markdown("## 🚨 Cyber Threat Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.error(
        f"🔴 Highest Financial Loss Country: "
        f"{df.groupby('Country')['Financial Loss (in Million $)'].sum().idxmax()}"
    )

    st.warning(
        f"🟠 Most Common Attack: "
        f"{df['Attack Type'].mode()[0]}"
    )

    with col2:
        st.success(
        f"🟢 Most Targeted Industry: "
        f"{df['Target Industry'].mode()[0]}"
    )

    st.info(
        f"🔵 Average Resolution Time: "
        f"{df['Incident Resolution Time (in Hours)'].mean():.1f} Hours"
    )
    
    st.markdown("""
### 👩‍💻 Developed By
*****Sonali Rawat*****

    Course : B.Tech(Artificial Intelligence & Machine Learning)

    Project  : CybArena - Cyber Threat Intelligence Dashboard
""")
    
    st.markdown("## 📊 Dataset Integrity Report")

    col1, col2, col3, col4 = st.columns(4)

    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    quality = (
    (1 - (missing + duplicates) / (df.shape[0] * df.shape[1])) * 100
)

    with col1:
        st.success(f"📄 Records\n\n{len(df)}")

    with col2:
        st.info(f"📑 Columns\n\n{df.shape[1]}")

    with col3:
        st.error(f"❌ Missing Values\n\n{missing}")

    with col4:
        st.info(f"⭐ Quality Score\n\n{quality:.1f}%")
    
    
    st.warning("Thank you for exploring CybArena!🛡️")

    st.markdown("---")
    st.caption("Developed by Sonali | CybArena | B.Tech AIML")
