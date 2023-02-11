import io
import os
import pandas as pd
import requests as req
import zipfile as zf
from glob import glob
from tqdm import tqdm

def award_xml_to_df( xml_file ):
    try:
        award_df = pd.read_xml(xml_file)
    except:
        print(f'ERROR: could not convert xml file ot dataframe: {xml_file}')
        award_df = None
    return award_df

def download_award_year_files( award_year ):
    zip_dl_url = fr"https://www.nsf.gov/awardsearch/download?DownloadFileName={award_year}&All=true"
    dl_url_r = req.get(zip_dl_url,allow_redirects=True)
    xml_dir_path = fr".\downloads\xml\{award_year}"
    os.makedirs(xml_dir_path,exist_ok=True)
    print('extracting xml files')
    with zf.ZipFile(io.BytesIO(dl_url_r.content)) as zr:
        zr.extractall(xml_dir_path)
    return xml_dir_path

def get_year_award_df( xml_dir_path ):
    print('converting to dataframe')
    xml_file_list = glob(os.path.join(xml_dir_path,'*.xml'))
    return pd.concat(
        [award_xml_to_df(xml_file) for xml_file in tqdm(xml_file_list)],
        ignore_index=True)

def cleanup_xml_files( xml_dir=r'./downloads/xml' ):
    xml_files = glob(os.path.join(xml_dir,'*','*.xml'))
    for xml_file in tqdm(xml_files):
        os.remove(xml_file)

def main():
    overwrite = False
    year_list = list(range(1959,2024))
    award_df = pd.DataFrame()
    os.makedirs(r'.\years',exist_ok=True)
    for year in year_list:
        year_table_file = rf'.\years\awards_{year}.csv'
        if os.path.exists(year_table_file) and (not overwrite):
            print(f'loading records found for year: {year}')
            award_year_df = pd.read_csv(year_table_file)
        else:
            print(f'downloading records for year: {year}')
            award_year_xml_path = download_award_year_files(year)
            award_year_df = get_year_award_df(award_year_xml_path)
            award_year_df.to_csv(year_table_file,index=False)
        award_df = pd.concat([award_df,award_year_df],ignore_index=True)
    award_df.to_csv('nsf_awards.csv',index=False)
    print('removing xml files...')
    cleanup_xml_files()
    print('done!')

if __name__ == "__main__":
    main()