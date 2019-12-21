DROP TABLE IF EXISTS member_ids_urls, member_data_keys, congress_member, district_demographics, member_service;

CREATE TABLE member_data_keys
(
  record_id   SERIAL PRIMARY KEY,
  member_id   VARCHAR(20),
  district    INT,
  full_name   VARCHAR(100),
  first_name  VARCHAR(50),
  middle_name VARCHAR(50),
  last_name   VARCHAR(50),
  suffix      VARCHAR(15)
);

/* Basic demographic profiles */
CREATE TABLE congress_member
(
  record_id    INT,
  first_name   VARCHAR(50),
  middle_name  VARCHAR(50),
  last_name    VARCHAR(50),
  suffix       VARCHAR(15),
  chamber      VARCHAR(10),
  district     INT,
  state        VARCHAR(10),
  birthdate    DATE,
  gender       VARCHAR(10),
  religion     VARCHAR(50),
  race         VARCHAR(30),
  lgbtq        VARCHAR(30),
  last_updated TIME
);

/* Various identifiers for websites and urls as well */
CREATE TABLE member_ids_urls
(
  record_id        INT,
  member_id        VARCHAR(20),
  govtrack_id      VARCHAR(20),
  cspan_id         VARCHAR(20),
  votesmart_id     VARCHAR(20),
  icpsr_id         VARCHAR(20),
  crp_id           VARCHAR(20),
  google_entity_id VARCHAR(20),
  fec_candidate_id VARCHAR(20),
  ocd_id           VARCHAR(20),
  geoid            VARCHAR(20),
  rss_url          VARCHAR(100),
  url              VARCHAR(100),
  api_uri          VARCHAR(100)
);

/* district_demographics */
CREATE TABLE district_demographics
(
  district                            INT,
  record_id                           INT,
  acs_white_adult_pct_2016            NUMERIC,
  acs_black_adult_pct_2016            NUMERIC,
  acs_latinx_adult_pct_2016           NUMERIC,
  acs_asian_pac_adult_pct_2016        NUMERIC,
  acs_native_amer_adult_pct_2016      NUMERIC,
  acs_other_adult_pct_2016            NUMERIC,
  census_white_adult_pct_2010         NUMERIC,
  census_black_adult_pct_2010         NUMERIC,
  census_latinx_adult_pct_2010        NUMERIC,
  census_asian_pac_adult_pct_2010     NUMERIC,
  census_native_amer_adult_pct_2010   NUMERIC,
  census_other_adult_pct_2010         NUMERIC,
  pct_bachelors_or_higher_2017        NUMERIC,
  rankings_bachelors_or_higher_2017   INT,
  acs_median_household_income_2017    NUMERIC,
  acs_household_income_rankings_2017  INT,
  population_total                    INT,
  population_white                    INT,
  population_black                    INT,
  population_latinx                   INT,
  population_asian_pac                INT,
  population_native_amer              INT,
  population_other                    INT,
  number_potential_voters_total       INT,
  number_potential_voters_white       INT,
  number_potential_voters_black       INT,
  number_potential_voters_latinx      INT,
  number_potential_voters_asian_pac   INT,
  number_potential_voters_native_amer INT,
  number_potential_voters_other       INT,
  census_population_total_2010        INT,
  census_population_white_2010        INT,
  census_population_black_2010        INT,
  census_population_latinx_2010       INT,
  census_population_asian_pac_2010    INT,
  census_population_native_amer_2010  INT,
  census_population_other_2010        INT
);


/* Political career and voting record */
CREATE TABLE member_service
(
  record_id               INT,
  member_id               VARCHAR(20),
  in_office               BOOLEAN,
  office                  VARCHAR(300),
  term_start              DATE,
  term_end                DATE,
  next_election           INT,
  leadership_role         VARCHAR(50),
  seniority               INT,
  party                   VARCHAR(20),
  caucus                  VARCHAR(100),
  total_votes             INT,
  missed_votes            INT,
  total_present           INT,
  missed_votes_pct        NUMERIC,
  votes_with_party_pct    NUMERIC,
  votes_against_party_pct NUMERIC
);
