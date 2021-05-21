import pandas as pd

fi1 = '/Users/han/Desktop/Date.csv'

df1 = pd.read_csv(fi1)

States = {
    "AB":"Alberta",	
    "BC":"British Columbia",
    "MB":"Manitoba",
    "NB":"New Brunswick",
    "NL":"Newfoundland And Labrador",
    "NS":"Nova Scotia",
    "NT":"Northwest Territories",
    "NU":"Nunavut",
    "ON":"Ontario",
    "PE":"Prince Edward Island",
    "QC":"Quebec",
    "SK":"Saskatchewan",
    "YT":"Yukon"
}


def clean():
    
    # remove excess words
    df1['phone'] = df1['phone'].str.replace("phone='",'')
    df1['location'] = df1['location'].str.replace('where=', '')
    
    # remove duplicates
    df1 = df1.drop_duplicates(keep='first')
    
    # get states extensions and make new column
    df1['State'] = df1['location'].str.extract(r'\+([A-Z]{2})')
    df1['location'] = df1['location'].str.replace('\+', ' ', regex=True)
    df1['location'] = df1['location'].str.replace(' [A-Z]{2}', '', regex=True)
    
    # replace abbrivation with proper state names
    df1['State'] = df1['State'].replace(States)
    
    # remove other than website links % clean links
    df1['Website'] = df1['Website'].str.replace('.*yellowpages\.ca.*', 'NA', regex=True)
    df1['Website'] = df1['Website'].str.replace('%2F', '/', regex=True)
    final = df1[df1["Website"].str.contains("NA|facebook")==False]
    final = final.drop_duplicates(subset=['Website'])   
    
    return final


def save():
    df = clean()
    df.to_csv('/Users/han/Desktop/21_May_2021.csv', index=False)


if __name__="__main__":
    print(clean())
