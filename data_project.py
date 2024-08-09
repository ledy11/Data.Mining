import pandas as pd
import os


pd.set_option('display.max_columns', None)

print("Start")

file_path = "data.csv"

if os.path.exists(file_path):
    print("File available.")
    try:
        df = pd.read_csv(file_path)
        print("File loaded successfully")

        # Process the DataFrame
        df = df.drop_duplicates()
        #remove attributes
        df = df.drop(columns="DR_NO")
        print("Duplicates removed and column dropped")
        df = df.drop(columns="AREA")
        print("Area removed ")
        df = df.drop(columns="Rpt Dist No")
        print("District removed ")
        df = df.drop(columns="Part 1-2")
        print("Part 1-2 removed ")
        df = df.drop(columns="Crm Cd")
        print("Crime cd removed ")
        df = df.drop(columns="Mocodes")
        print("Mocodes removed ")
        df = df.drop(columns="Status")
        print("Status removed ")
        df = df.drop(columns="Status Desc")
        print("Status Desc removed ")
        df = df.drop(columns="Crm Cd 1")
        print("Crm Cd 1 removed ")
        df = df.drop(columns="LAT")
        print("LAT removed ") 
        df = df.drop(columns="LON")
        print("LON removed ")
        df = df.drop(columns="Premis Cd")
        print("CPremis Removed")
        df = df.drop(columns="Weapon Used Cd")
        print("Weapons Removed")
        df = df.drop(columns="Crm Cd 2")
        print("Crime 2 Removed")
        df = df.drop(columns="Crm Cd 3")
        print("Crime 3 Removed")
        df = df.drop(columns="Crm Cd 4")
        print("Crime 4 Removed")
        df = df.drop(columns="Cross Street")
        print("Cross street Removed")
        df = df.drop(columns="LOCATION")
        print("Location Removed")

        #remove NaN values
        for column in df.select_dtypes(include='object').columns:
            df[column] = df[column].fillna('')
        print("NaN removed")

        #final number of columns  
        num_columns = df.shape[1]
        print(f"Final number of columns: {num_columns}")

        #print the names for when needed in writing report 
        column_names = df.columns.tolist()
        print("column names:")
        for name in column_names:
            print(name)

        # show head 
        print("head:")
        print(df.head())  


        #age has negative values
        #filtering out to see the ones that are > 0 
        df = df[df['Vict Age'] >= 0]

        # get rid of NaN and replacing NaN with zeroes
        df['Vict Age'] = df['Vict Age'].fillna(0)


        # Create the bins which will be the cut off for the different ages. 
        #after 100 then it is all grouped (float('inf'))
        #This part will give me a new age group in power BI so I can directly use the processed data 
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, float('inf')]

        #create labels for the different ages 
        labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100', '100+']

        # set ages to the different bins using pd.cut()
        df['Age Group'] = pd.cut(df['Vict Age'], bins=bins, labels=labels, right=False)

        # Calculate the value counts and percentages for each age bracket(aggregation)
        age_group_count = df['Age Group'].value_counts(sort=False)
        age_group_percent = age_group_count  / age_group_count .sum() * 100

        # Print the age bracket percentages to make sure they're good 
        print("Victim Age Percentages:")
        print(age_group_percent)

        #convert time to datetime format for month/popular times analysis 

        #"The object to convert to a datetime. If a DataFrame is provided, 
        # the method expects minimally the following columns: "year", "month", "day". 
        # The column “year” must be specified in 4-digit format.""

        # Convert DATE OCC to datetime

        df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], errors='coerce')

        # the time is on military time, so it must have leading zeros if ints > 0 are not present 
        df['TIME OCC'] = df['TIME OCC'].astype(str).str.zfill(4)

        # we use HHMM formart so  this line will report the hour as a whole int. example, if it is 1210, then 
        #report it back as hour 12 instead of all the following nums since I am interested in learning 
        #which under which time during the day and different months crime occurs the most 
        df['HOUR OCC'] = df['TIME OCC'].str[:2].astype(int)

        # same for month to compare 
        df['MONTH OCC'] = df['DATE OCC'].dt.month

       #check 
        # print("test data:")
        # print(df[['TIME OCC', 'HOUR OCC']].head(10))

        # create the month/hour groups 
        #.size() will help me count the number of groups I created above
        hour_count = df.groupby(['MONTH OCC', 'HOUR OCC']).size().reset_index(name='crime count')

        #test 2
        # print("test 2:")
        # print(hourly_counts.head(20))

        # I used idxmax() to give me the hour with max number of counts for each month 
        pop_hour = hour_count.loc[hour_count.groupby('MONTH OCC')['crime count'].idxmax()]

        #test 3
        print("test 3:")
        print(pop_hour)


        #save this data as a dataset to upload to power BI this clean data 
        output_file_path = "cleaned_data2.csv"
        df.to_csv(output_file_path, index=False)

        #print(f"data saved to {output_file_path}")

    except Exception as e:
        print(f"error: {e}")
else:
    print("isnt available")

print("done")

