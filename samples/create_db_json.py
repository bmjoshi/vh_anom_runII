import os
import json
import subprocess

datasetlist = ['ZHiggs0L1ToGG',
        'ZHiggs0L1ZgToGG',
        'ZHiggs0L1Zgf05ph0ToGG',
        'ZHiggs0L1f05ph0ToGG',
        'ZHiggs0MToGG',
        'ZHiggs0PHToGG',
        'ZHiggs0PHf05ph0ToGG',
        'ZHiggs0PMToGG',
        'ZHiggs0Mf05ph0ToGG',
        'WHiggs0L1ToGG',
        'WHiggs0L1f05ph0ToGG',
        'WHiggs0MToGG',
        'WHiggs0Mf05ph0ToGG',
        'WHiggs0PHToGG',
        'WHiggs0PHf05ph0ToGG',
        'WHiggs0PMToGG',
        'GluGluHToGG_M125',
        'VBFHToGG_M125',
        'VHToGG_M125',
        'ttHJetToGG_M125',
        'DYJetsToLL_M-50',
        'DiPhotonJetsBox_M40',
        'DiPhotonJetsBox_MGG-80toInf',
        'GJet_Pt-20to40',
        'GJet_Pt-40toInf',
        'TTGJets_TuneCP5',
        'TTJets_TuneCP5',
        'WGToLNuG_01J',
        'WW_TuneCP5',
        'WZ_TuneCP5',
        'ZGToLLG_01J',
        'ZZ_TuneCP5',
        'TGJets_TuneCP5',
        'TTGG_0Jets']
era = {
    '2018': 'RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16',
    '2017': 'RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9',
    '2016_preVFP': 'RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11',
    '2016_postVFP': 'RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17'
}

alt_era = {
    '2016_postVFP': 'RunIISummer20UL16MiniAOD-106X_mcRun2_asymptotic_v13-v3',
    '2016_preVFP': 'RunIISummer20UL16MiniAODAPV-106X_mcRun2_asymptotic_preVFP_v8-v3',
    '2017': 'RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v3',
    '2018': 'RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v3'
}

db = {}
for dset in datasetlist:
    db[dset] = {}
    for yr in era:
        
        jsonfile = 'microaod/microaod_{dset}_{year}.json'.format(dset=dset, year=yr)
        
        with open(jsonfile, 'r') as f0:
            das_ = json.load(f0)
        
        db[dset][yr] = {
            'ndatasets': len(das_),
            'name': [],
            'modification_time': [],
            'location': []
        }
        
        for i in range(len(das_)):
            mdtime_ = das_[i]['dataset'][0]['modification_time']
            name_ = das_[i]['dataset'][0]['name']

            # get location
            q_ = "file dataset={name_} instance=prod/phys03".format(name_=name_)
            p = subprocess.Popen(["dasgoclient", "--query", q_], stdout=subprocess.PIPE)
            stdout, stderr = p.communicate()
            files = [ f for f in stdout.decode('utf-8').split('\n') if f!='' ]
            loc_ = ''
            if len(files)>0: loc_ = '/eos/cms'+'/'.join(files[0].split('/')[:-1])
            
            db[dset][yr]['name'].append(name_)
            db[dset][yr]['modification_time'].append(mdtime_)
            db[dset][yr]['location'].append(loc_)

with open('vh_anom_samples_db.json','w') as f0:
   json.dump(db, f0)
