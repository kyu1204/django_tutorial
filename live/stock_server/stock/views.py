from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from elasticsearch import Elasticsearch
from .utils import create_query

import json
import copy
import datetime


with open('./config/config.json') as f:
    config = json.load(f)


class PredictView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.es = Elasticsearch(config['ES']['HOSTS'])
        self.pre_stock_index = config['ES']['PRED_INDEX']

    def post(self, request):
        if 'date' not in request.data:
            match = {
                "match_all": {}
            }
            query = create_query(match, size=1, sort=True)
            result = self.es.search(index=self.pre_stock_index, body=query, request_timeout=60)

            if len(result) <= 0:
                result = {
                    "message": "not found data"
                }
                return Response(status=status.HTTP_400_BAD_REQUEST, data=result)

            else:
                if len(result['hits']['hits']) <= 0:
                    result = {
                        "message": "not found data"
                    }
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=result)

                recent_date = result['hits']['hits'][0]['_source']['date']

                match = {
                    "match": {
                        "date": recent_date
                    }
                }
                query = create_query(match, size=200, sort=False)
                result = self.es.search(index=self.pre_stock_index, body=query, request_timeout=60)

                return Response(result)
        else:
            date = request.data['date']
            match = {
                "match": {
                    "date": date
                }
            }
            query = create_query(match, size=200, sort=False)
            result = self.es.search(index=self.pre_stock_index, body=query, request_timeout=60)
            if len(result) <= 0:
                result = {
                    "message": "not found data"
                }
                return Response(status=status.HTTP_400_BAD_REQUEST, data=result)

            if len(result['hits']['hits']) <= 0:
                result = {
                    "message": "not found data"
                }
                return Response(status=status.HTTP_400_BAD_REQUEST, data=result)

            return Response(result)


class KospiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.es = Elasticsearch(config['ES']['HOSTS'])
        self.kospi_index = config['ES']['KOSPI_INDEX']

    def post(self, request):
        if 'date' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'not found paramas'})
        date = request.data['date']

        match = {
            "match": {
                "_id": "kospi200_" + str(date)
            }
        }
        query = create_query(match, size=1, sort=False)
        result = self.es.search(index=self.kospi_index, body=query, request_timeout=60)

        return Response(result)


class ReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.es = Elasticsearch(config['ES']['HOSTS'])

    def post(self, request):
        if 'date' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'not found paramas'})
        date = request.data['date']

        match = {
            "match": {
                "date": date
            }
        }
        query = create_query(match, size=200, sort=True)
        result = self.es.search(index="up_stock", body=query, request_timeout=60)

        if len(result) <= 0:
            result = {
                "message": "not found data"
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=result)

        else:
            if len(result['hits']['hits']) <= 0:
                result = {
                    "message": "not found data"
                }
                return Response(status=status.HTTP_400_BAD_REQUEST, data=result)

            return Response(result)


class PredictRateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.es = Elasticsearch(config['ES']['HOSTS'])

    def get(self, request):
        match = {
            "exists": {
                "field": 'rate'
            }
        }
        query = create_query(match, size=30, sort=True, sort_key='@timestamp')
        result = self.es.search(index="pre_report", body=query, request_timeout=60)

        if len(result) <= 0:
            result = {
                "message": "not found data"
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=result)

        else:
            if len(result['hits']['hits']) <= 0:
                result = {
                    "message": "not found data"
                }
                return Response(status=status.HTTP_400_BAD_REQUEST, data=result)

            docs = result['hits']['hits']
            date_list = list()
            rate_list = list()
            for doc in docs:
                date = datetime.datetime.strptime(doc['_source']['@timestamp'], '%Y-%m-%dT%H:%M:%S.000+09:00')
                date = date.strftime('%m/%d')
                date_list.append(date)
                rate_list.append(doc['_source']['rate'])

            date_list.reverse()
            rate_list.reverse()
            return Response({
                "date": date_list,
                "rate": rate_list
            })


class HitDateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.es = Elasticsearch(config['ES']['HOSTS'])

    def get(self, request):
        match = {
            "exists": {
                "field": 'rate'
            }
        }
        query = create_query(match, size=200, sort=False)
        result = self.es.search(index="pre_report", body=query, request_timeout=60, scroll='30m')
        if len(result) <= 0:
            result = {
                "message": "not found data"
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=result)

        if len(result['hits']['hits']) <= 0:
            result = {
                "message": "not found data"
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=result)

        num_docs = len(result['hits']['hits'])
        scroll_id = result['_scroll_id']
        date_list = list()

        while num_docs > 0:
            docs = result['hits']['hits']
            for doc in docs:
                timestamp = doc['_source']['@timestamp']
                date = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.000+09:00')
                date = int(date.strftime('%Y%m%d'))
                if date < 20200104 or date == 20200131:
                    continue
                date_list.append(date)

            result = self.es.scroll(scroll_id=scroll_id, scroll='30m')
            num_docs = len(result['hits']['hits'])

        hit_date_list = copy.deepcopy(date_list)
        hit_date_list.sort(reverse=True)
        date_list.sort(reverse=True)
        date_list.pop(0)
        return Response({'pred': date_list, 'hits': hit_date_list})
