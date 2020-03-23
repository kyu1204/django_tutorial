def create_query(query=None, script=None, size=None, multi=None, querys=None, sort=True, sort_key=None, query_range=None):
    if multi is not None:
        queryform = {
            "query": {
                "bool": {
                    "filter": {
                        "bool": {
                            "must": querys
                        }
                    }
                }
            }
        }
    else:
        queryform = {
            "query": {
                "bool": {
                    "filter": {
                        "bool": {
                            "must": [query]
                        }
                    }
                }
            }
        }
    if sort and sort_key is None:
        queryform['sort'] = [{"date": {"order": "desc"}}]
        queryform['size'] = 1
    if sort and sort_key is not None:
        queryform['sort'] = [{sort_key: {"order": "desc"}}]
        queryform['size'] = 1
    if script is not None:
        queryform['script'] = script
    if size is not None:
        queryform['size'] = size
    if query_range is not None:
        queryform['query']['bool']['filter']['bool']['filter'] = query_range

    return queryform
