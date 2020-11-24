#!/usr/bin/env python3
import requests
import xmltodict
import warnings


class RCSB_Search:
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    query_type_set = {"PubmedIdQuery", "AdvancedKeywordQuery",
                      "ChainTypeQuery", "TaxQuery", "ExpTypeQuery"}

    def __init__(self, search_term, query_type="AdvancedKeywordQuery",
                 query_type_set=query_type_set):
        assert query_type in query_type_set, "\
            Query type {} not supported yet.".format(query_type)
        self.search_term = search_term
        self.query_type = query_type

        query_params = dict()
        query_params['queryType'] = "org.pdb.query.simple." + query_type

        if query_type == 'AdvancedKeywordQuery':
            query_params['description'] = 'Text Search for: ' + search_term
            query_params['keywords'] = search_term

        elif query_type == 'PubmedIdQuery':
            query_params['description'] = '\
                Pubmed Id Search for Pubmed Id ' + search_term
            query_params['pubMedIdList'] = search_term

        elif query_type == 'ExpTypeQuery':
            query_params['experimentalMethod'] = search_term
            query_params['description'] = 'Experimental Method Search :\
                Experimental Method=' + search_term
            query_params['mvStructure.expMethod.value'] = search_term

        elif query_type == 'ChainTypeQuery':
            type_list = search_term.lower().split()
            protein = dna = rna = hybrid = 'N'
            if "protein" in type_list:
                protein = 'Y'
            if "dna" in type_list:
                dna = 'Y'
            if "rna" in type_list:
                rna = 'Y'
            if "hybrid" in type_list:
                hybrid = 'Y'
            query_params['description'] = 'Chain Type Search : \
                Contains Protein={}, Contains DNA={}, Contains RNA={}, \
                Contains DNA/RNA Hybrid={}'.format(protein, dna, rna, hybrid)
            query_params['containsProtein'] = protein
            query_params['containsDna'] = dna
            query_params['containsRna'] = rna
            query_params['containsHybrid'] = hybrid

        elif query_type == 'TaxQuery':
            query_params['description'] = 'Taxonomy Search for ' + search_term
            query_params['Organisms'] = 'Homo Sapiens'

        self.params = dict()
        self.params['orgPdbQuery'] = query_params
        self.search_term = search_term
        self.url = 'http://www.rcsb.org/pdb/rest/search'
        self.idlist = self.search()

    def __str__(self):
        return 'Search item: {}, Query type: {}.'.format(self.search_term,
                                                         self.query_type)
    __repr__ = __str__

    def search(self, headers=headers):
        queryText = xmltodict.unparse(self.params, pretty=False)
        response = requests.post(url=self.url, data=queryText, headers=headers)

        if response.status_code == 200:
            pass
        else:
            warnings.warn("Retrieval failed, returning None")
            return None

        result = response.text

        idlist = str(result)
        idlist = idlist.split('\n')[:-1]

        return idlist


def get_info(pdb_id, url_root='http://www.rcsb.org/pdb/rest/describePDB?structureId='):
    url = url_root + pdb_id
    response = requests.get(url)

    if response.status_code == 200:
        pass
    else:
        warnings.warn("Retrieval failed, returning None")
        return None

    result = str(response.text)

    out = xmltodict.parse(result, process_namespaces=True)

    return out


def get_entities_info(pdb_id, url_root='http://www.rcsb.org/pdb/rest/describeMol?structureId='):
    url = url_root + pdb_id
    response = requests.get(url)

    if response.status_code == 200:
        pass
    else:
        warnings.warn("Retrieval failed, returning None")
        return None

    result = str(response.text)

    out = xmltodict.parse(result, process_namespaces=True)

    return out


def get_pdb_file(pdb_id, filetype='pdb', compression=False):

    full_url = "https://files.rcsb.org/download/"

    full_url += pdb_id

    if (filetype == 'structfact'):
        full_url += "-sf.cif"
    else:
        full_url += "." + filetype

    if compression:
        full_url += ".gz"
    else:
        pass

    response = requests.get(full_url)

    if response.status_code == 200:
        pass
    else:
        warnings.warn("Retrieval failed, returning None")
        return None

    if compression:
        result = response.content
    else:
        result = response.text

    return result
