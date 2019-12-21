#!/usr/bin/python
import psycopg2
from psycopg2 import sql
from datetime import datetime
import sys
import csv

DATA_PATH = 'data/'
file_list = ['data/test.csv', 'data/test.csv']

expenditure_column_conversions = {
    'BIOGUIDE_ID': 'bioguide_id',
    'OFFICE': 'office',
    'QUARTER': 'fiscal_quarter',
    'SORT SEQUENCE': 'sort_sequence',
    'PROGRAM': 'program_type',
    'CATEGORY': 'expense_category',
    'DATE': 'record_date',
    'PAYEE': 'payee',
    'START DATE': 'start_date',
    'END DATE': 'end_date',
    'PURPOSE': 'purpose',
    'AMOUNT': 'amount',
    'YEAR': 'fiscal_year',
    'RECIP (orig.)': 'original_recipient',
    '': 'old_payee'
}

member_data_col_conversions = {
    'member_id': 'id',
    'district': 'district',
    'full_name': 'officialFullName',
    'First name': 'first_name',
    'Last name': 'last_name'
}

congress_member_col_conversions = {
    "first_name": "first_name",
    "middle_name": "middle_name",
    "last_name": "last_name",
    "suffix": "suffix",
    "chamber": "chamber",
    "district": "district",
    "state": "state",
    "birthdate": "date_of_birth",
    "gender": "gender",
    "religion": "religion",
    "race": "raceEthnicity",
    "lgbtq": "lgbtq",
    "last_updated": "last_updated"
}

member_ids_urls_conversions = {
    "member_id": "id",
    "govtrack_id": "govtrack_id",
    "cspan_id": "cspan_id",
    "votesmart_id": "votesmart_id",
    "icpsr_id": "icpsr_id",
    "crp_id": "crp_id",
    "google_entity_id": "google_entity_id",
    "fec_candidate_id": "fec_candidate_id",
    "ocd_id": "ocd_id",
    "geoid": "geoid",
    "rss_url": "rss_url",
    "url": "url",
    "api_uri": "api_uri"
}

district_demographics_conversions = {
    "district": "district",
    "record_id": "record_id",
    "acs_white_adult_pct_2016": "whiteACS2012-16citizenAdultPopulation",
    "acs_black_adult_pct_2016": "blackACS2012-16citizenAdultPopulation",
    "acs_latinx_adult_pct_2016": "latinoACS2012-16citizenAdultPopulation",
    "acs_asian_pac_adult_pct_2016": "asianPacificIslanderACS2012-16citizenAdultPopulation",
    "acs_native_amer_adult_pct_2016": "nativeACS2012-16citizenAdultPopulation",
    "acs_other_adult_pct_2016": "otherACS2012-16citizenAdultPopulation",
    "census_white_adult_pct_2010": "white2010censusAdultPopulation",
    "census_black_adult_pct_2010": "black2010censusAdultPopulation",
    "census_latinx_adult_pct_2010": "latino2010censusAdultPopulation",
    "census_asian_pac_adult_pct_2010": "asianPacificIslander2010censusAdultPopulation",
    "census_native_amer_adult_pct_2010": "native2010censusAdultPopulation",
    "census_other_adult_pct_2010": "other2010censusAdultPopulation",
    "pct_bachelors_or_higher_2017": "bachelorsPlusACS2013-17",
    "rankings_bachelors_or_higher_2017": "bachelorsPlusRankACS2013-17",
    "acs_median_household_income_2017": "medianHouseholdIncomeACS2013-17",
    "acs_household_income_rankings_2017": "householdIncomeRankACS2013-17",
    "population_total": "citizenPopulation",
    "population_white": "whiteCitizenPopulation",
    "population_black": "blackCitizenPopulation",
    "population_latinx": "latinoCitizenPopulation",
    "population_asian_pac": "asianPacificIslanderCitizenPopulation",
    "population_native_amer": "nativeAmericanCitizenPopulation",
    "population_other": "otherCitizenPopulation",
    "number_potential_voters_total": "citizenVotingAgePopulation",
    "number_potential_voters_white": "whiteCitizenVotingAgePopulation",
    "number_potential_voters_black": "blackCtizenVotingAgePopulation",
    "number_potential_voters_latinx": "latinoCitizenVotingAgePopulation",
    "number_potential_voters_asian_pac": "asianPacificIslanderCitizenVotingAgePopulation",
    "number_potential_voters_native_amer": "nativeCitizenVotingAgePopulation",
    "number_potential_voters_other": "otherCitizenVotingAgePopulation",
    "census_population_total_2010": "censusTotalPopulation",
    "census_population_white_2010": "censusWhitePopulation",
    "census_population_black_2010": "censusBlackPopulation",
    "census_population_latinx_2010": "censusLatinoPopulation",
    "census_population_asian_pac_2010": "censusAsianPacificIslanderPopulation",
    "census_population_native_amer_2010": "censusNavtiveAmericanPopulation",
    "census_population_other_2010": "censusOtherPopulation"
}

"""
Different scenarios:

- Has a bioguide_id, then is from a congressman's budget. Include in house_rep_expenses
- If sort_sequence is subtotal or ????, skip line
- If payee is "DO", use the previous payee (means ditto)

Fields for expense_line
- types: representative, committee, 
- row_id, bioguide_id, office
- fiscal_quarter, fiscal_year, record_date, start_date, end_date
- expense_category, purpose, payee, amount, original_recipient/old_payee
"""


def process_csvs(files):
    """ Iterate over a list of csv files and ingest into Postgres db
    :param files: list of file names in string format
    :return:
    """

    for file in files:
        column_names = ''

        # open the csv file--if it's readable, process the rows
        with open(DATA_PATH + file, newline='') as csv_file:
            reader = csv.reader(csv_file)

            try:
                for row in reader:

                    # If processing 1st row of csv, convert headings to column names,
                    # otherwise process row data
                    if not column_names:
                        # converts csv headings to associated columns in table
                        column_names = normalize_column_names(row)
                    else:
                        expense_id = process_row(row, column_names)
                        print(expense_id)

            except csv.Error as e:
                log_error_and_exit((e, file, reader.line_num))

    print("{} files processed successfully!".format(len(files)))


def normalize_column_names(header_row):
    """ Convert headers from csv file to their equivalent in the database.
        The csv files vary in their columns fields and order, so having the explicit column name means no strange errors
    when inserting into db!
    :param header_row: first row of csv file, column labels
    :return: list with db column name at the index matching the data's position in the (normalized) data row's list.
    """
    column_names = list()

    for header_entry in header_row:
        try:
            column_name = expenditure_column_conversions[header_entry]
            column_names.append(column_name)
        except KeyError as e:
            print("No matching entry for {}".format(header_entry))
            log_error_and_exit(e)

    return column_names


def process_row(row, column_names):
    """ Edit the data's raw format to normalize and prepare for insertion into db.
    :param row: list representing a row from an inported csv file
    :param column_names: column names corresponding to fields in the database table
    :return: new row id
    """
    row_keys_values = dict()
    expense_row = row.split(',')

    for i in range(len(expense_row)):
        value = expense_row[i]
        key = column_names[i]

        if key == 'start_date' or key == 'end_date' or key == 'record_date':
            value = datetime.strptime(value, '%B-%d-%Y')

        elif key == 'fiscal_year' and not value.isdigit():
            split_val = value.split()
            value = split_val[-1]
        elif key == 'amount':
            value = format(float(value), '.2f')
        elif key == 'office':
            if len(value) > 4 and value[0:4].isnumeric():
                value = value[4:len(value)]
                value = normalize_entry(value)
        elif key == 'payee' or key == 'original_recipient' or key == 'old_payee':
            value = normalize_entry(value)

        if value:
            row_keys_values[key] = value

    return insert_into_db(row_keys_values)


def normalize_entry(value):
    """Removes: special characters, extra tabs and spacing, most punctuation for the sake of being able
        to combine matching records with character variations. Also converts to title case.

    :param value: unprocessed data value from csv
    :return: normalized data value
    """

    char_list = ['.', ',', '\t', '¬', '≠', '!', '?', '=']
    slash_list = [' \\ ', ' \\', '\\ ']
    amp_list = [' & ', '& ', ' &']

    normed_value = value.translate(None, ''.join(char_list))
    normed_value = normed_value.translate(None, '&'.join(amp_list))
    normed_value = normed_value.translate(None, '\\'.join(slash_list))
    normed_value = " ".join(normed_value.split())
    normed_value = normed_value.title()

    return normed_value

"""
    conn = psycopg2.connect("dbname=house-spending user=house-spending")

"""


def insert_into_db(key_val_dict, table, connection_str):
    """ Sanitize db input using psycopg2's Composable class. Create a variable-length insert statement, and execute.

    :param key_val_dict: dictionary with keys == database columns and values = the values to insert
    :param table name of table to insert into
    :return: new id generated by the insert statement.
    """
    keys = list(key_val_dict.keys())
    values = list(key_val_dict.values())

    query = sql.SQL('INSERT INTO {} ({}) VALUES ({})').format(
        sql.Identifier(table),
        sql.SQL(', ').join(sql.Identifier(n) for n in keys),
        sql.SQL(', ').join(sql.Identifier(n) for n in values))

    try:
        conn = psycopg2.connect(connection_str)
        cur = conn.cursor()
        cur.execute(query)
        inserted_id = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return inserted_id
    except psycopg2.Error as err:
        log_error_and_exit(err)



def log_error_and_exit(error):
    """ Print and exit when an exception is thrown.
    :param error: message returned by system
    :return: none, exit
    """
    error_output = "{} - Error message: {} \n".format(datetime.now(), error)
    f = open("logs/ingest_csv_py_log.txt", "a")
    f.write(error_output)
    f.close()
    sys.exit(error_output)
