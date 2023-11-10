import os
from elasticsearch import Elasticsearch, helpers
import elasticsearch
from gig import Gig
import database
from typing import List

import ssl
import certifi

# Path to your 'http_ca.crt' file
cert_path = '/Users/ibe/School/AdvancedProgrammingTechniquesCOS333/gigl/elasticsearch-8.11.0/config/certs/http_ca.crt'

# Create an SSL context
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.load_verify_locations(cert_path)

username = 'elastic'
password = os.environ.get('ELASTIC_PASSWORD')

es = Elasticsearch([os.environ.get('ELASTICSEARCH_URL')],
                   ssl_context=ssl_context,
                   basic_auth=(username, password))


class GigSearch:
    def __init__(self, index_name='gigs') -> None:
        self.index_name = index_name
        self.es = Elasticsearch([os.environ.get('ELASTICSEARCH_URL')])
        all_gigs: List[Gig] = database.get_gigs()
        for gig in all_gigs:
            payload = {}
            payload['title'] = gig.get_title()
            payload['description'] = gig.get_description()
            payload['qualifications'] = gig.get_qualifications()
            es.index(index='gigs', id=gig.get_gigID(), body=payload)

    def query(self, keyword='', category=None):
        # bool_query = {
        #     "should": [
        #         {"match": {"title": keyword}},
        #         {"match": {"description": keyword}}
        #     ],
        # }
        # if category:
        #     bool_query["must"] = [{"match": {"category": category}}] THIS IS FOR CATEGORIES WILL MAKE THIS WORK LATER
        query = {
            "query": {
                "bool": {
                    "should": [
                        {"wildcard": {"title": f"{keyword}*"}}, # we want 'love' and 'love2' to appear when 'love' is searched
                        {"match": {"description": keyword}}
                    ],
                    "minimum_should_match": 1  # do an either or 
                }
            }
        }
        if not keyword and not category:
            query = {
                "query": {
                    "match_all": {}
                }
            }
        response = None
        try:
            response = es.search(index='gigs', body=query)
        except elasticsearch.BadRequestError as e:
            print(f"bad request: {e.info}")
        except Exception as e:
            print(f"exception occurred: {e}")
        return response

    def add_gig():
        pass

    def delete_gig():
        pass

    def test(self):
        mapping = es.indices.get_mapping(index='gigs')
        print(mapping)
        analyze_love = es.indices.analyze(index="gigs", body={"text": "love"})
        print(analyze_love)

        # Analyze the keyword "love2"
        analyze_love2 = es.indices.analyze(index="gigs", body={"text": "love2"})
        print(analyze_love2)    


# -----------------------------------------------------------------------


def _test():
    search = GigSearch()
    #search.test()
    #print()
    response = search.query(keyword="assist")
    print(response)
    return


if __name__ == '__main__':
    _test()
