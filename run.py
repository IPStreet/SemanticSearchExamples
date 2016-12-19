import csv
from datetime import datetime

from IPStreet import client, query
# from Tkinter import *


def revelant_patents_search(search_seed_text,api_key):
    # instantiate client
    ip_street_client = client.Client(api_key, 2)

    # instantiate a claim_only semantic search query, claim_text as search seed add query parameters
    search_query = query.ClaimOnlySearch()
    search_query.add_raw_text(search_seed_text) # add search seed to query
    search_query.add_end_date(datetime.now().strftime("%Y-%m-%d"),"publication_date") # open time window up to today
    search_query.add_expired('True') # include expired patents
    search_query.add_max_expected_results(1000) # grab top 1000 results
    search_query.add_page_size(100) # set page size to 100 results

    # send the claim_only semantic search query
    search_results = ip_street_client.send(search_query)


    # instantiate the enrichment query
    enrichment_query = query.PatentData()

    # from semantic search results, prepare enrichment data query
    for asset in search_results:
        application_number = asset['application_number']
        # print(application_number)
        enrichment_query.add_application_number(application_number) # add application number to query

    # send final query
    final_results = ip_street_client.send(enrichment_query)

    # join concept scores with data results for writing to csv
    data_to_write = join_concept_results_to_enrichment_results(search_results, final_results)

    # return enriched results to user, write csv in this case
    write_results_to_csv("related_patents_search", data_to_write)

def prior_art_search(grant_number,api_key):
    # instantiate client
    ip_street_client = client.Client(api_key, 2)

    # instantiate data query, add query parameters
    data_query = query.PatentData()
    data_query.add_grant_number(grant_number)

    # send the data query
    data_results = ip_street_client.send(data_query)

    # extract claim text from response
    claim_text = data_results[0]['claims'][0]
    # extract priority date from response
    priority_date = data_results[0]['earliest_file_date']

    # instantiate a claim_only semantic search query, claim_text as search seed add query parameters
    search_query = query.ClaimOnlySearch()
    search_query.add_raw_text(claim_text)  # add claim text to query
    search_query.add_end_date(priority_date, "earliest_date_filed") # set time window to priority date and before
    search_query.add_expired('True')  # include expired patents
    search_query.add_max_expected_results(500)
    search_query.add_page_size(100)


    # send the claim_only semantic search query
    search_results = ip_street_client.send(search_query)
    # print(search_results)

    # instantiate the enrichment query
    enrichment_query = query.PatentData()

    # from semantic search results, prepare enrichment data query
    for asset in search_results:
        application_number = asset['application_number']
        # print(application_number)
        enrichment_query.add_application_number(application_number)

    # send final query
    final_results = ip_street_client.send(enrichment_query)

    # join concept scores with data results for writing to csv
    data_to_write = join_concept_results_to_enrichment_results(search_results, final_results)


    # return enriched results to user, write csv in this case
    write_results_to_csv("prior_art_search",data_to_write)

def join_concept_results_to_enrichment_results(concept_results, data_results):
    """ Joins concept scores and index position from concept search results with data results
    """
    for asset in data_results:
        for search_result in concept_results:
            if search_result['application_number'] == asset['application_number']:
                asset['index_position'] = search_result['index_position']
                asset['relevence_score'] = search_result['relevence_score']

    return data_results

def write_results_to_csv(file_name,data_to_write):
    """" writes a list of enriched IP Street results to a csv file
    """
    write_payload = sorted(data_to_write, key=lambda k: k['index_position'])
    fieldnames = ['index_position',
                  'relevence_score',
                  'application_number',
                  'publication_number',
                  'grant_number',
                  'title',
                  'abstract',
                  'claims',
                  'owner',
                  'inventor',
                  'law_firm',
                  'earliest_file_date',
                  'application_date',
                  'publication_date',
                  'grant_date',
                  'expire_date'
                  ]
    with open(str(file_name)+'.csv', "w", encoding="utf8", newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, dialect='excel', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(write_payload)


if __name__ == "__main__":
    api_key = "API_KEY"
    prior_art_search('7477713',api_key)

    search_seed_text = "a configurable battery pack charging system coupled to said " \
                       "charging system controller, said battery pack and a power source, " \
                       "wherein said configurable battery pack charging system charges " \
                       "said battery pack in accordance with " \
                       "said battery pack charging conditions set by said charging system controller."
    revelant_patents_search(search_seed_text)