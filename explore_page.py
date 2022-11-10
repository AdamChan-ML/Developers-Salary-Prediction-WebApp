import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

# Create a function to compile the countries with smaller values into "Others" categories
def compile_countries(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "Others"
    return categorical_map

# Create a function to standardize and clean the coding experience column
# Convert Coding Experience Column into float data type
def clean_yearsCodePro(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

# Clean education column into a few categories
def clean_edLevel(x):
    if "Bachelor’s degree" in x:
        return "Bachelor's degree"
    if "Master’s degree" in x:
        return "Master's degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Postgraduate"
    return "Less than a Bachelors"

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    # Extracting Columns that are being used for model training
    df = df[["Country", "EdLevel", "YearsCodePro", "WorkExp", "Employment", "RemoteWork", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly":"Salary"}, axis = 1)
    df = df[df["Salary"].notnull()]
    df= df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df= df.drop("Employment", axis = 1)
    country_map = compile_countries(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)

    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df["Country"] != "Others"]

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_yearsCodePro)
    df['EdLevel'] = df["EdLevel"].apply(clean_edLevel)

    return df

df = load_data()

def show_explore_page():
    st.title("Explore Developers Salaries")

    st.write(
        """#### Stack Overflow Developer Survey 2021"""
        )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    # equal ensures that pie chart is drawn as a circle
    ax1.axis("equal")      

    st.write("""#### Number of Data from different countries""") 

    st.pyplot(fig1)

    st.write("""#### Mean Salry Based on Country""") 

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""#### Mean Salary Based on Experience""") 

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

