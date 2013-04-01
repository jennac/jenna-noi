#!/usr/bin/python
import argparse
import csv

def parseSF(s_name, pl_name):
    sourced ={} 
    with open(s_name, 'rU') as sfile:       
            s_reader = csv.DictReader(sfile, delimiter=',')            
            key_count = 0
            for data in s_reader:
                sourced[key_count] = data
                addPL(pl_name, sourced[key_count])
                key_count += 1                
    return sourced

def addPL(pl_name, sourced):
    with open(pl_name, 'rU') as plfile:
        pl_reader = csv.DictReader(plfile, delimiter=',')
        for row in pl_reader:
            if sourced['polling_location_ids'] == row['polling_location_id']:               
                sourced['city'] = row['address_city']
                 
def matchtoVF(v_name, sourced, writer):
    with open(v_name, 'rU') as vfile:
        reader = csv.DictReader(vfile, delimiter=',')
        match_count = 0
        for row in reader:
            for k in sourced:
                if sourced[k]['county'].lower() == row['vf_precinct_county'].lower():
                    if sourced[k]['city'].lower() == row['vf_precinct_city'].lower():
                        index = sourced[k]['clean_precinct_name'].find('/')
                        if ((sourced[k]['clean_precinct_name'][:index] == row['vf_precinct_ward'])
                            or row['vf_precinct_ward'] == ''
                            or sourced[k]['clean_precinct_name'] == 0):                           
                            if sourced[k]['clean_precinct_name'][index+1:] == row['vf_precinct_code']:
                                writer.writerow([sourced[k]['county'], row['vf_precinct_county'], sourced[k]['city'],
                                                 row['vf_precinct_city'],sourced[k]['clean_precinct_name'], row['vf_precinct_name'],
                                                 sourced[k]['clean_precinct_name'][index+1:], row['vf_precinct_code'],
                                                 sourced[k]['clean_precinct_name'][:index], row['vf_precinct_ward']])
                                match_count += 1
    print 'Matched {} out of {}'.format(match_count, len(sourced))


    
def main():
    parser = argparse.ArgumentParser(description='Takes in file names')
    parser.add_argument('s', help='clean sourced file name')
    parser.add_argument('vf', help='voterfile file name')
    parser.add_argument('pl', help='polling location file')
    parser.add_argument('m', help='name of the output file for matches')
    args = parser.parse_args()

    sourced = parseSF(args.s, args.pl)
    
    with open(args.m, 'w') as match_file:
        writer = csv.writer(match_file, delimiter=',')
        writer.writerow(['s_county', 'vf_county','s_city', 'vf_city', 's_precinct_name', 'vf_precinct_name',
                         's_precinct_number', 'vf_precinct_number', 's_ward', 'vf_ward'])
        matchtoVF(args.vf, sourced, writer)

if __name__ == "__main__":
    main()

