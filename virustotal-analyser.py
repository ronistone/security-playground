import json


def processAnalyse(item):
    id = item['data']['id']
    attributes = item['data']['attributes']
    description = attributes['popular_threat_classification']['suggested_threat_label']
    type_description = attributes['type_description']
    size = attributes['size']
    analyse = []
    lastAnalysis = attributes['last_analysis_results']
    for av in lastAnalysis.keys():
        analyse.append({
            'name': av,
            'result': lastAnalysis[av]['result'],
            'category': lastAnalysis[av]['category']
        })
    analyse.sort(key=lambda x : x['name'])
    return {
        'id': id,
        'description': description,
        'type_description': type_description,
        'size': size,
        'analyse': analyse
    }


vendors = {}

with open('./virus.json', 'r') as f:
    payload = json.loads(f.read())
    processed = []
    for analyse in payload:
        process = processAnalyse(analyse)
        for vendor in process['analyse']:
            # if vendor['category'] == 'type-unsupported':
            #     continue
            if vendor['name'] not in vendors:
                vendors[vendor['name']] = 0

            if vendor['category'] == 'malicious':
                vendors[vendor['name']] += 1
        processed.append(process)

    vendors = dict(sorted(vendors.items(), key=lambda item: item[1]))
    print(json.dumps(processed))
    print(json.dumps(vendors))
