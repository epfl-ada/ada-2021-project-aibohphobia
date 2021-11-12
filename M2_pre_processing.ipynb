{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "6119acc8-475d-4232-8309-e84c626355b9",
   "metadata": {},
   "source": [
    "## Initial pre-processing\n",
    "\n",
    "In this notebook we will:\n",
    "- Proceed with basic cleaning of each year from **2015-2020** which includes removing nan speakers, nan quotes and further inconsistencies \n",
    "- Exploit the useful information from the wikidata dumps provided to us \n",
    "- Add columns of interest for further analysis \n",
    "\n",
    "The **output** will be pickle files for each year with additional columns such as tags, gender (male/female), domain name, citizenship of spokesperson...\n",
    "This output file will be used in the **second notebook** containing the `basic data analysis`\n",
    "\n",
    "\n",
    "#### Useful libraries"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "59b83648-ee02-4be9-8280-923761c459b6",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[nltk_data] Downloading package stopwords to\n",
      "[nltk_data]     /home/lavinia/nltk_data...\n",
      "[nltk_data]   Package stopwords is already up-to-date!\n",
      "[nltk_data] Downloading package punkt to /home/lavinia/nltk_data...\n",
      "[nltk_data]   Package punkt is already up-to-date!\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import pickle\n",
    "from tqdm.auto import trange, tqdm\n",
    "import time\n",
    "from journal_API_wikidata import extract_info_wiki\n",
    "from Data_clean_functions import *\n",
    "from tld import get_tld\n",
    "\n",
    "from collections import Counter\n",
    "import warnings\n",
    "warnings.filterwarnings(\"ignore\")\n",
    "\n",
    " "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "0b959ddd-4327-46bd-b33c-34d311e5629f",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Whether to run cleaning or not\n",
    "RUN_CLEANING = False\n",
    "# Note: Approximate 4 hours per year --> over a day on a single computer"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4c23ec22-509a-417d-a94a-460ac5ac5d84",
   "metadata": {},
   "source": [
    "### Data paths"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "2fee7d63-8c3b-4f88-b6c8-7d7dfb1218d4",
   "metadata": {},
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "    Please note the data is not provided but the `FILE` represents the \n",
    "    data given by QuoteBank \n",
    "\"\"\"\n",
    "\n",
    "DATA_PATH = './data/'\n",
    "\n",
    "# Original files from Quotebank\n",
    "FILES = [DATA_PATH + 'quotes-2015.json.bz2', DATA_PATH + 'quotes-2016.json.bz2', DATA_PATH + 'quotes-2017.json.bz2',\n",
    "         DATA_PATH + 'quotes-2018.json.bz2', DATA_PATH + 'quotes-2019.json.bz2', DATA_PATH + 'quotes-2020.json.bz2']\n",
    "\n",
    "# Files after rapid cleaning and explose function \n",
    "# Note: Because of the explose function we get a great number of lines, thus the saved file is large in size (approx 4 times original)\n",
    "PATHS_OUT =[ DATA_PATH + 'rapid_clean-quotes-2015.json.bz2',DATA_PATH + 'rapid_clean-quotes-2016.json.bz2',\n",
    "            DATA_PATH + 'rapid_clean-quotes-2017.json.bz2',DATA_PATH + 'rapid_clean-quotes-2018.json.bz2',\n",
    "            DATA_PATH + 'rapid_clean-quotes-2019.json.bz2',DATA_PATH + 'rapid_clean-quotes-2020.json.bz2',]\n",
    "\n",
    "PATHS_OUT_filter = [DATA_PATH + 'filter_clean-quotes-2015.json.bz2',DATA_PATH + 'filter_clean-quotes-2016.json.bz2',\n",
    "                   DATA_PATH + 'filter_clean-quotes-2017.json.bz2',DATA_PATH + 'filter_clean-quotes-2018.json.bz2',\n",
    "                   DATA_PATH + 'filter_clean-quotes-2019.json.bz2',DATA_PATH + 'filter_clean-quotes-2020.json.bz2']"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "89db466e-dda2-4bdf-ada8-4549dbc8ca28",
   "metadata": {},
   "source": [
    "#### Read file, clean and save in pickle"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "a323b368-06b6-41d8-89d0-3c2aa85ff561",
   "metadata": {},
   "outputs": [],
   "source": [
    "def clean_original_file_top_sites(FILE, PATH_OUT):\n",
    "    \n",
    "    with pd.read_json(FILE, lines=True, compression='bz2', chunksize=100000) as df_reader:\n",
    "        for chunk in tqdm(df_reader):\n",
    "\n",
    "            # Basic cleaning (refer to function doc)\n",
    "            df_base_clean = rapid_clean(chunk)\n",
    "\n",
    "            # Extract site name from dataframe\n",
    "            extract_name(df_base_clean)\n",
    "\n",
    "            # Expand the df on sitenames and urls\n",
    "            df_base_clean_exp = df_base_clean.explode([\"sitenames\", \"urls\"])\n",
    "\n",
    "            # Save chunk by chunk appending the clean df\n",
    "            with open(PATH_OUT, 'ab') as d_file:\n",
    "                pickle.dump(df_base_clean_exp, d_file)\n",
    "                n_chunks += 1\n",
    "\n",
    "            # Add counter for occurences of a specific media\n",
    "            counts = Counter(df_base_clean_exp['sitenames'].tolist()) \n",
    "            Total_count += counts\n",
    "            print(\"Chunk done\")\n",
    "\n",
    "        # List the top 100 most occuring media\n",
    "        for site, count in Total_count.most_common(100):\n",
    "                top_sites.append(site)\n",
    "        \n",
    "        \n",
    "        # Pickle save the top_sites for future use\n",
    "        with open(DATA_PATH + f'top_sites_{FILE[14:18]}.pkl', 'wb') as output:\n",
    "            pickle.dump(top_sites, output)\n",
    "        TOP_LIST.append(top_sites)\n",
    "\n",
    "        print(\"finished top sites\")\n",
    "    \n",
    "    \n",
    "    return n_chunks, TOP_LSIT\n",
    "\n",
    "\n",
    "\n",
    "# Save the number of chunks dumped for each file in order to open again later\n",
    "N_CHUNKS_LIST = []\n",
    "\n",
    "# Save the top sites for quick access in following function\n",
    "TOP_LIST = []\n",
    "\n",
    "if RUN_CLEANING:\n",
    "    for index, FILE in enumerate(FILES):\n",
    "\n",
    "        n_chunks = 0\n",
    "        Total_count = Counter()\n",
    "        top_sites = []\n",
    "\n",
    "        n_chunks,TOP_LIST = clean_original_file_top_sites(FILE, PATHS_OUT[index], TOP_LIST)\n",
    "        N_CHUNKS_LIST.append(n_chunks)\n",
    "    \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "776b94de-6e70-4a74-9e4e-afcb20d7a525",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "\"\\nwith open(DATA_PATH + 'top_sites.pkl', 'rb') as file:\\n    top_sites = pickle.load(file)\\n    \\n\""
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "# Pickle open the top_sites\n",
    "\"\"\"\n",
    "with open(DATA_PATH + 'top_sites.pkl', 'rb') as file:\n",
    "    top_sites = pickle.load(file)\n",
    "    \n",
    "\"\"\""
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b90961a0-a898-4342-a8de-46a8fc60001c",
   "metadata": {},
   "source": [
    "### For Milestone 2 keep 10 most citing media\n",
    "\n",
    "\n",
    "**Note**: We intend on increasing the number from 10 to 50 but this would take \n",
    "an approximate 5 hours to run per year, we thus plan on running it after the deadline \n",
    "and focused on making a main pipeline first\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6276d00e-45c2-4db7-a2db-6a26f3d4887d",
   "metadata": {},
   "source": [
    "### Filter the rows belonging to top 10 sites"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "c3bc3451-7826-4b7e-a742-da4e4b413202",
   "metadata": {},
   "outputs": [],
   "source": [
    "# New df with rows belonging to top 10 sites\n",
    "#PATHS_OUT_filter\n",
    "def extract_top_sites_rows(PATH_OUT, top_10_sites, n_chunks, PATH_OUT_filter):\n",
    "    \n",
    "    chunks_all_filtered = pd.DataFrame(columns=['quoteID', 'quotation', 'speaker', 'qids', 'date', 'numOccurrences',\n",
    "           'probas', 'urls', 'phase', 'sitenames'])\n",
    "\n",
    "    chunk_nbr = 0\n",
    "\n",
    "    with open(PATH_OUT, 'rb') as d_file:\n",
    "        while (chunk_nbr < n_chunks):\n",
    "\n",
    "            # Progress meter\n",
    "            print(f\"{chunk_nbr}/{n_chunks}\")\n",
    "\n",
    "            chunk = pickle.load(d_file)\n",
    "\n",
    "            # Filter chunks with sitenames belonging to top 10\n",
    "            chunk_filtered = chunk[chunk.sitenames.isin(top_10_sites)]\n",
    "\n",
    "            # Save filtered chunks\n",
    "            with open(PATH_OUT_filter, 'ab') as d_file_out:\n",
    "                pickle.dump(chunk_filtered, d_file_out)\n",
    "\n",
    "\n",
    "            chunks_all_filtered = chunks_all_filtered.append(chunk_filtered)\n",
    "\n",
    "            chunk_nbr+=1\n",
    "\n",
    "        # Save as pickle for future use\n",
    "        with open(DATA_PATH + f'chunks_all_filtered_{FILE[14:18]}.pkl', 'wb') as output:\n",
    "            pickle.dump(chunks_all_filtered, output)\n",
    "if RUN_CLEANING:\n",
    "    for index, PATH_OUT in enumerate(PATHS_OUT):\n",
    "\n",
    "        # TOP_SITES[index][:10] are the first top 10 sites for a year\n",
    "        extract_top_sites_rows(PATH_OUT, TOP_SITES[index][:10], N_CHUNKS_LIST[index], PATHS_OUT_filter[index])"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a8829f5c-5f01-41bb-bb0c-a583f2cce2c7",
   "metadata": {},
   "source": [
    "**Note:**\n",
    "\n",
    "The function above may be used to process all yearly quotes but this requires a powerful computer and a lot of memory (as mentionned with the exploded dataset). Thus we each treated different years for efficiency.\n",
    "\n",
    "Below we will pursue the last part of the analysis with an example on one specific year. For eg:2020\n",
    "This can be and was done for each pre-processed year (2015-2020)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "2304ce04-3688-4afc-9d35-653af9eaf7d1",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "\n",
    "if RUN_CLEANING:\n",
    "    # Open pickled dataframe\n",
    "    with open(DATA_PATH +'chunks_all_filtered_2020.pkl', 'rb') as output:\n",
    "        chunks_all_filtered = pickle.load(output)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "8b91404d-efaa-495c-a467-c0f8e0fe1465",
   "metadata": {},
   "outputs": [],
   "source": [
    "if RUN_CLEANING:\n",
    "    # Groupby the exploded data set \n",
    "    gb_all_filtered = chunks_all_filtered[[\"speaker\", \"qids\" , \"urls\", \"quoteID\", \"quotation\",\"date\"]].groupby([\"speaker\", \"qids\", \"quoteID\", \"quotation\"])\n",
    "\n",
    "    # One row, quote, may be cited by different media so we list them\n",
    "    df_filtered = gb_all_filtered[\"urls\"].apply(list)\n",
    "\n",
    "    df_filtered_final = df_filtered.reset_index()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "a0d7ca73-9fae-454e-a21f-964bdace57a0",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "if RUN_CLEANING:\n",
    "    # Save pickled dataframe\n",
    "    with open(DATA_PATH + 'df_filtered_final_2020.pkl', 'wb') as output:\n",
    "        pickle.dump(df_filtered_final, output)\n",
    "\n",
    "    '''# Open pickled dataframe\n",
    "    with open(DATA_PATH + 'df_filtered_final.pkl', 'rb') as output:\n",
    "        df_filtered = pickle.load(output)\n",
    "    '''"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "468e22fb-c9b5-4f1d-b96d-d48773823ec2",
   "metadata": {
    "tags": []
   },
   "source": [
    "### Create a dictionnary of categories and associated synonyms\n",
    "\n",
    "This will enable us to tag the different category of the quote\n",
    "\n",
    "*Note*: This is a restrictive list and some additional content will be added"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "d0ab30d8-b3b6-4bc1-88ec-72f1481ee7a4",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "if RUN_CLEANING:\n",
    "    matchers = {\"art\": [\"art\", \"paint\", \"draw\", \"museum\"], \\\n",
    "                \"business\": [\"business\", \"finance\", \"economy\", \"commerce\", \"bank\", \"money\", \"trade\"], \\\n",
    "                \"entertainment\":[\"entertainment\"], \n",
    "                \"fashion\":[\"fashion\", \"couture\", \"designer\"], \\\n",
    "                \"medicine\":[\"medicine\", \"health\", \"pharmacy\", \"wellbeing\", \"body\"], \\\n",
    "                \"music\":[\"music\", \"song\", \"album\", \"concert\"], \\\n",
    "                \"politics\":[\"politics\", \"government\"], \\\n",
    "                \"science\":[\"science\", \"research\"], \\\n",
    "                \"sport\": [\"sport\", \"football\", \"athletics\", \"swimming\", \"rugby\", \"tennis\", \"volleyball\", \"ski\"]}\n",
    "\n",
    "    # Find general form for categories and words\n",
    "    generalizeDictionary(matchers)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "239b7084-82c3-4c8e-9ff2-dccc4043ce31",
   "metadata": {},
   "source": [
    "### Extract information from URL"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "492ea7ce-a7d5-4b2c-bbac-89f4cc0214a8",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "if RUN_CLEANING:\n",
    "    df_extract = Chunk_url_extract(df_filtered_final, matchers)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "fd98785c-df8c-4868-9e51-8a06cf3da781",
   "metadata": {},
   "outputs": [],
   "source": [
    "if RUN_CLEANING:\n",
    "    with open(DATA_PATH + 'df_extract_2020.pkl', 'wb') as output:\n",
    "        pickle.dump(df_extract, output)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "4c2dc0eb-3fb7-4a6c-8ab4-47c8f1b63407",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "\"\\n# Open pickled dataframe\\nwith open(DATA_PATH + 'df_extract.pkl', 'rb') as output:\\n    df_extract = pickle.load(output)\\n\""
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\"\"\"\n",
    "# Open pickled dataframe\n",
    "with open(DATA_PATH + 'df_extract.pkl', 'rb') as output:\n",
    "    df_extract = pickle.load(output)\n",
    "\"\"\""
   ]
  },
  {
   "cell_type": "markdown",
   "id": "909a6c00-f6a3-41bf-842d-3e886baccc7a",
   "metadata": {},
   "source": [
    "### Formatting wikidata data of interest\n",
    "Using the Wikidata speakers and label description files provided by TA's, we extract data we need for our project.\n",
    "\n",
    "This includes gender, citizenship, data of birth...\n",
    "\n",
    "**Note**:The file is the same for each year so it was saved and utilized by each of us for the respective year we treated"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "cd06fead-2097-4a0b-af14-4778713ebd3d",
   "metadata": {},
   "outputs": [],
   "source": [
    "if RUN_CLEANING:\n",
    "    Wikidata_speakers = pd.read_parquet(DATA_PATH + 'speaker_attributes.parquet')\n",
    "    Wikidata_countries = pd.read_csv(DATA_PATH + 'wikidata_labels_descriptions_quotebank.csv.bz2', compression = 'bz2')\n",
    "\n",
    "    Wikidata_utils = formating_wikidata(Wikidata_speakers, Wikidata_countries)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "4c27b9e1-4468-4ef6-9044-0ede5a448cc8",
   "metadata": {},
   "outputs": [],
   "source": [
    "if RUN_CLEANING:\n",
    "    # Save wikidata utils\n",
    "    with open(DATA_PATH + 'Wikidata_utils.pkl', 'wb') as output:\n",
    "        pickle.dump(Wikidata_utils, output)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "94e4215f-c86f-464b-8e73-5506b4954f92",
   "metadata": {},
   "outputs": [],
   "source": [
    "if RUN_CLEANING:\n",
    "    # Open file \n",
    "    with open(DATA_PATH + 'Wikidata_utils.pkl', 'rb') as input_file:\n",
    "        Wikidata_utils = pickle.load(input_file)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c520674f-7931-4674-b82b-a230c465809b",
   "metadata": {},
   "source": [
    "### Add information from wikidata"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "5b11451b-9aa1-4bee-b51c-135d50de99dc",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "if RUN_CLEANING:\n",
    "    # Merge the info of wikidata from speaker to the initial dataframe\n",
    "    df_merged = merge_quotes_wikidata(Wikidata_utils, df_extract)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3da4a34b-2a1a-40c9-a04b-baf38daee513",
   "metadata": {},
   "source": [
    "### Final dataframe after merging \n",
    "\n",
    "The final dataframe for each year after the basic cleaning and merging is given in the drive link provided in the README.MD\n",
    "\n",
    "\n",
    "**Note**: These data frames are the ones used in the Notebook on the \"Basic data analysis \""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "798252b1-043a-47e8-9383-6664fcae5302",
   "metadata": {},
   "outputs": [],
   "source": [
    "if RUN_CLEANING:\n",
    "    with open(DATA_PATH + 'df_2020_no_media.pkl', 'wb') as output:\n",
    "        pickle.dump(df_merged, output)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (ada_project)",
   "language": "python",
   "name": "ada_project"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
