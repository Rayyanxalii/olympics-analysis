import numpy as np
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset= ['Team','NOC','City','Games','Year', 'Sport', 'Event','Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally
    

def country(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country


def fetch_medal_tally(year, country, df):
    medal_df = df.drop_duplicates(subset= ['Team','NOC','City','Games','Year', 'Sport', 'Event','Medal'])
    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x 


def data_time(df,col):
    nation_over_time = df
    nation_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().sort_index(ascending=True)
    nation_over_time = nation_over_time.reset_index()        
    nation_over_time = nation_over_time.rename(columns={'Year': 'Edition', 'count': col})
    
    return nation_over_time

def most_successful_ath(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals per athlete
    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Athlete', 'Medals']

    # Merge to get additional info (e.g., region and sport)
    top_athletes = top_athletes.merge(df[['Name', 'region', 'Sport']], left_on='Athlete', right_on='Name', how='left')

    # Drop duplicates to avoid repeated athlete names from different rows
    top_athletes = top_athletes.drop_duplicates('Athlete')

    # Final clean DataFrame
    return top_athletes[['Athlete', 'region', 'Sport', 'Medals']].set_index('Athlete')


def country_wise_medal(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region']== country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    
    return final_df

def country_medal_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region']== country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')
    
    return pt

def most_success_ath_count_wise(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    top_athletes = temp_df['Name'].value_counts().reset_index().head(10)
    top_athletes.columns = ['Athlete', 'Medals']

    top_athletes = top_athletes.merge(
        df[['Name', 'region', 'Sport']],
        left_on='Athlete',
        right_on='Name',
        how='left'
    )

    top_athletes = top_athletes.drop_duplicates('Athlete')
    return top_athletes[['Athlete', 'region', 'Sport', 'Medals']].set_index('Athlete')


def weight_v_height(df, sport):
    # Remove duplicate athletes
    ath_df = df.drop_duplicates(subset=['Name', 'region'])

    # Replace NaNs in Medal column with 'No Medal'
    ath_df['Medal'] = ath_df['Medal'].fillna('No Medal')

    # Filter by sport only if a specific sport is selected
    if sport != 'Overall':
        temp_df = ath_df[ath_df['Sport'] == sport]
    else:
        temp_df = ath_df  # Don't filter by sport

    return temp_df

def men_v_women(df):
    athelte_df = df.drop_duplicates(subset=['Name','region'])
    men = athelte_df[athelte_df['Sex']== 'M'].groupby('Year').count()['Name'].reset_index()
    women = athelte_df[athelte_df['Sex']== 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on= 'Year', how = 'left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    final.fillna(0,inplace=True)
    
    return final
