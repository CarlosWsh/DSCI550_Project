import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

def scrape_alcohol_abuse_data(url):
    """Scrape alcohol abuse statistics from the given URL."""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print(f"Error fetching page: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    data = []

    for section in soup.find_all(['h3', 'p']):
        text = section.text.strip()
        if section.name == 'h3' and 'Alcohol Abuse Statistics' in text:
            state_name = text.replace(' Alcohol Abuse Statistics', '').strip()
            stats_list = section.find_next_sibling('ul')

            if stats_list:
                stats = [item.text.strip() for item in stats_list.find_all('li')]

                binge_rate = median_drinks = top_25_drinks = None
                median_binge_freq = top25_binge_freq = annual_deaths = None
                death_rate_increase = death_rate_per_capita = male_death_percentage = None
                chronic_death_percentage = adult_35plus_death_percentage = under_21_death_percentage = None
                years_of_potential_life_lost = taxpayer_cost = None

                for stat in stats:
                    if 'binge drink at least once per month' in stat:
                        binge_rate_match = re.search(r'([\d.]+)%', stat)
                        binge_rate = float(binge_rate_match.group(1)) if binge_rate_match else None

                    elif 'The median number of drinks per binge is' in stat:
                        parts = stat.split(';')
                        if len(parts) == 2:
                            median_drinks_match = re.search(r'The median number of drinks per binge is ([\d.]+)',
                                                            parts[0])
                            median_drinks = float(median_drinks_match.group(1)) if median_drinks_match else None
                            top_25_drinks_match = re.search(
                                r'the 25% most active drinkers consume a median ([\d.]+) drinks per binge', parts[1],
                                re.IGNORECASE)
                            top_25_drinks = float(top_25_drinks_match.group(1)) if top_25_drinks_match else None

                    elif 'binge a median' in stat:
                        parts = stat.split(';')
                        if len(parts) == 2:
                            median_binge_freq_match = re.search(r'binge a median ([\d.]+) times', parts[0])
                            median_binge_freq = float(
                                median_binge_freq_match.group(1)) if median_binge_freq_match else None
                            top25_binge_freq_match = re.search(r'the 25% most active drinkers binge ([\d.]+) times',
                                                               parts[1], re.IGNORECASE)
                            top25_binge_freq = float(
                                top25_binge_freq_match.group(1)) if top25_binge_freq_match else None

                    elif 'annual deaths' in stat:
                        annual_deaths_match = re.search(r'([\d,]+)', stat)
                        annual_deaths = int(
                            annual_deaths_match.group(1).replace(',', '')) if annual_deaths_match else None


                    elif '5-year average annual rate of excessive alcohol deaths per capita' in stat:
                        death_rate_increase_match = re.search(r'increased by as much as ([\d.]+)% from \d{4} to \d{4}', stat)
                        death_rate_increase = (float(death_rate_increase_match.group(1)) if death_rate_increase_match else None)

                    elif 'averages one (1) death from excessive alcohol use for every' in stat:
                        death_rate_per_capita_match = re.search(r'one \(1\) death from excessive alcohol use for every ([\d,]+) people', stat)
                        death_rate_per_capita = int(death_rate_per_capita_match.group(1).replace(',', '')) if death_rate_per_capita_match else None

                    elif 'who die from excessive alcohol use' in stat and 'are male' in stat:
                        male_death_percentage_match = re.search(r'([\d.]+)% of people who die from excessive alcohol use .*? are male', stat)
                        male_death_percentage = (float(male_death_percentage_match.group(1)) if male_death_percentage_match else None)

                    elif 'of excessive alcohol use deaths are from chronic causes' in stat:
                        chronic_death_percentage_match = re.search(r'([\d.]+)% of excessive alcohol use deaths are from chronic causes', stat)
                        chronic_death_percentage = float(chronic_death_percentage_match.group(1)) if chronic_death_percentage_match else None

                    elif 'from excessive alcohol use are adults aged 35 years and older' in stat:
                        adult_35plus_death_percentage_match = re.search(r'([\d.]+)% of deaths in .*? from excessive alcohol use are adults aged 35 years and older',stat)
                        adult_35plus_death_percentage = float(adult_35plus_death_percentage_match.group(1)) if adult_35plus_death_percentage_match else None

                    elif 'who die from excessive alcohol use are under the age of 21' in stat:
                        under_21_death_percentage_match = re.search(r'([\d.]+)% of people in .*? who die from excessive alcohol use are under the age of 21',stat)
                        under_21_death_percentage = float( under_21_death_percentage_match.group(1)) if under_21_death_percentage_match else None


                    elif 'The CDC estimates' in stat and 'years of potential life is lost' in stat:
                        years_of_potential_life_lost_match = re.search(r'The CDC estimates ([\d,]+(?:\.\d+)?) years of potential life is lost to excessive alcohol use each year',stat)
                        years_of_potential_life_lost = (float(years_of_potential_life_lost_match.group(1).replace(',', ''))if years_of_potential_life_lost_match else None)


                    elif 'taxpayers spent' in stat and 'as a result of excessive alcohol use' in stat:
                        taxpayer_cost_match = re.search(r'taxpayers spent \$([\d,.]+) (million|billion) as a result of excessive alcohol use in (\d{4})',stat)
                        inflation_adjusted_cost_match = re.search(r'adjusted for inflation, this is equivalent to \$([\d,.]+) (million|billion)', stat)
                        cost_per_drink_match = re.search(r'or \$([\d.]+) per drink in (\d{4}) US\$', stat)

                        if taxpayer_cost_match:
                            cost_value = float(taxpayer_cost_match.group(1).replace(',', ''))
                            cost_unit = taxpayer_cost_match.group(2)
                            taxpayer_cost = cost_value * (1e9 if cost_unit == "billion" else 1e6)
                            taxpayer_cost = round(taxpayer_cost, 1)
                        if inflation_adjusted_cost_match:
                            adj_cost_value = float(inflation_adjusted_cost_match.group(1).replace(',', ''))
                            adj_cost_unit = inflation_adjusted_cost_match.group(2)
                            inflation_adjusted_cost = adj_cost_value * (1e9 if adj_cost_unit == "billion" else 1e6)
                            inflation_adjusted_cost = round(inflation_adjusted_cost, 1)
                        cost_per_drink = (float(cost_per_drink_match.group(1)) if cost_per_drink_match else None)

                data.append({
                    'State': state_name,
                    'Binge Drinking (%)': binge_rate,
                    'Median Drinks per Binge': median_drinks,
                    'Top 25% Median Drinks per Binge': top_25_drinks,
                    'Median Binges Monthly': median_binge_freq,
                    'Top 25% Monthly Binges': top25_binge_freq,
                    'Annual Deaths (Excessive Alcohol)': annual_deaths,
                    'Death Rate Increase (%)': death_rate_increase,
                    'Death Rate per Capita': death_rate_per_capita,
                    'Male Death Percentage':male_death_percentage,
                    'Chronic Death Percentage':chronic_death_percentage,
                    'adult_35plus Death Percentage':adult_35plus_death_percentage,
                    'Under 21 Death Percentage':under_21_death_percentage,
                    'Years of Potential Life Lost':years_of_potential_life_lost,
                    'Taxpayer Cost':taxpayer_cost,
                    'Inflation Adjusted Cost':inflation_adjusted_cost,
                    'Cost per Drink (in 2022 US$)':cost_per_drink
                })
    df = pd.DataFrame(data)

    # Manually append missing data
    df.loc[df['State'] == 'Georgia', 'Median Binges Monthly'] = 1.6
    df.loc[df['State'] == 'New Jersey', 'Top 25% Monthly Binges'] = 3.5
    df.loc[df['State'] == 'Arkansas', 'Years of Potential Life Lost'] = 35826
    df.loc[df['State'] == 'Alabama', 'Male Death Percentage'] = 71.5

    return df


def save_data(df, filename, delimiter=','):
    """Save DataFrame to CSV or TSV."""
    raw_data_dir = os.path.join("..", "data", "raw")
    os.makedirs(raw_data_dir, exist_ok=True)
    output_file = os.path.join(raw_data_dir, filename)
    df.to_csv(output_file, sep=delimiter, index=False)
    print(f"Data saved successfully at: {output_file}")


def main():
    url = "https://drugabusestatistics.org/alcohol-abuse-statistics/"
    df = scrape_alcohol_abuse_data(url)
    if not df.empty:
        save_data(df, "state_alcohol_abuse.csv", delimiter=',')
        save_data(df, "state_alcohol_abuse.tsv", delimiter='\t')


if __name__ == "__main__":
    main()

