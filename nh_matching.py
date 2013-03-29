#!/usr/bin/python
import argparse
import csv

"Takes in 3 files: sourced, vf, matched output."

def parseSF(s_name):
    sourced ={} 
    with open(s_name, 'rU') as sfile:
        reader = csv.DictReader(sfile, delimiter=',')
        key_count = 0
        for data in reader:
            sourced[key_count] = data
            key_count += 1
    return sourced

def matchtoVF(sourced_data, vf_name, m_name):
    with open(vf_name, 'rU') as vfile:
        reader = csv.DictReader(vfile, delimiter=',')
        with open(m_name,'a') as match_file:
            appender = csv.writer(match_file, delimiter=',')
            appender.writerow(['s_county', 'vf_county', 's_city', 'vf_city', 's_name', 'vf_name',
                               's_number', 'vf_number', 's_ward', 'vf_ward'])
            match_count = 0
            for row in reader:
                for k in sourced_data:
                    if sourced_data[k]['county'] == row['vf_precinct_county']:
                        if sourced_data[k]['city'] == row['vf_precinct_city']:
                            try:
                                if (0 <= int(sourced_data[k]['clean_precinct_name'][-2:]) <= 10
                                    and sourced_data[k]['clean_precinct_name'][-2:] == row['vf_precinct_ward']
                                    or sourced_data[k]['clean_precinct_name'][-2:] == row['vf_precinct_name'][-2:]):
                                    match_count += 1
                                    appendMatch(appender, sourced_data[k],row)
                            except ValueError:
                                match_count += 1
                                appendMatch(appender, sourced_data[k],row)                          
    print 'Matched {} out of {}'.format(match_count, len(sourced_data))
        
                                      
def appendMatch(appender, source, vf):
    appender.writerow([source['county'], vf['vf_precinct_county'], source['city'], vf['vf_precinct_city'],
                       source['clean_precinct_name'], vf['vf_precinct_name'], source['clean_precinct_number'],
                       vf['vf_precinct_code'], source['ward'], vf['vf_precinct_ward']])

def main():
    parser = argparse.ArgumentParser(description='Takes in file names')
    parser.add_argument('s', help='clean sourced file name')
    parser.add_argument('vf', help='voterfile file name')
    parser.add_argument('m', help='name of the output file for matches')
    args = parser.parse_args()

    sourced_data = parseSF(args.s)
    matchtoVF(sourced_data, args.vf, args.m)
    
if __name__ == "__main__":
    main()
