import json
import os
import numpy as np
from sklearn.metrics import accuracy_score

import sys

#modified from https://github.com/mgalley/sacreBLEU
# import sacrebleu_deltableu
import bleu as sacrebleu
import pandas as pd

try:
    import evaluate
except ImportError as e:
    print( e )
    pass  # module doesn't exist, deal with it.

# #############
# print('Checking BLEU')
# bleu = evaluate.load("sacrebleu")
# https://huggingface.co/spaces/evaluate-metric/sacrebleu
# >>> predictions = ["hello there", "general kenobi"]
# >>> references = [["hello", "there"], ["general kenobi", "general yoda"]]
# >>> sacrebleu = evaluate.load("sacrebleu"
# >>> results = sacrebleu.compute(predictions=predictions,
# ...                         references=references)
# will also run: https://github.com/mgalley/sacreBLEU
# #############


def read_json( file_path ) :
    with open( file_path, 'r' ) as f :
        return json.load( f )


def get_weight_schemes( df_userinfo, author_id, completeness, contains_freq_ans ) :

    userrow = df_userinfo[ df_userinfo['author_id']==author_id ].iloc[0]
    user_validlevel = userrow[ 'validation_level' ]
    user_rank = userrow[ 'rank_level' ]
    if user_rank == 'unk' :
        user_rank = 'level_0'

    answer_profile = [
           [ 1 if str(user_validlevel)[:2]=='md' else 0 ][0],
           [ 1 if int( user_rank.replace('level_','') ) >=4 else 0 ][0], # rank is between 0-8
           [ 1 if contains_freq_ans==1.0 else 0 ][0],
           [ 1 if completeness==1.0 else 0 ][0],
        ]
    
    w1 = -100
        
    if answer_profile[-1] == 1 :
        first_3 = sum( answer_profile[:-1] )
        if first_3 == 3 :
            w1 = 1.0
        elif first_3 == 2 :
            w1 = 0.9
        elif first_3 == 1 :
            w1 = 0.8
        else :
            w1 = 0.7
    else :
        first_3 = sum( answer_profile[:-1] )
        if first_3 == 3 :
            w1 = 0.9
        elif first_3 == 2 :
            w1 = 0.8
        elif first_3 == 1 :
            w1 = 0.7
        else :
            w1 = 0.6

    return w1


def get_ref_scores( references, df_userinfo ) :
    ref_scores = []

    for reference in references :
        author_id = reference[ 'author_id' ]
        completeness = reference[ 'completeness' ]
        contains_freq_ans = reference[ 'contains_freq_ans' ]
        ref_scores.append( get_weight_schemes( df_userinfo, author_id, completeness, contains_freq_ans ) )

    return ref_scores


# #############

reference_dir = os.path.join('/project/pi_hongyu_umass_edu/zonghai/parth/mediqa', '')
prediction_dir = os.path.join('/project/pi_hongyu_umass_edu/zonghai/parth/mediqa', '')
score_dir = '/project/pi_hongyu_umass_edu/zonghai/parth/mediqa'

print('Reading reference dataset')
truth = read_json( os.path.join(reference_dir, 'mediqa-m3-clinicalnlp2024/valid_ht.json') )
print( 'Number of instances: {}'.format( len( truth ) ) )
reference_langs = [ x.replace( 'content_', '' ) for x in truth[0]['responses'][0].keys() if 'content_' in x ]
reference_ids = [ x['encounter_id'] for x in truth ]
print( 'Reference languages: {}, {}'.format( len(reference_langs), str( reference_langs ) ) )

print('Reading prediction')
prediction = read_json( os.path.join(prediction_dir, './experiments/val_preds.json') )
print( 'Number of instances: {}'.format( len( prediction ) ) )
prediction_langs = [ x.replace( 'content_', '' ) for x in prediction[0]['responses'][0].keys() if 'content_' in x ]
prediction_ids = [ x['encounter_id'] for x in truth ]
print( 'Predicted languages: {}, {}'.format( len(prediction_langs), str( prediction_langs ) ) )

#checking that the encounter id's are the same and that instance id's
print( 'Checking instance ids match.')
bad_match = 0
for ind, reference_id in enumerate( reference_ids ) :
    prediction_id = prediction_ids[ ind ]
    if reference_id != prediction_id :
        bad_match += 1
        print( 'INDEX {} has different ids for reference and prediction, {} and {} respectively.'.format( ind, reference_id, prediction_id ) )

if bad_match > 0 :
    print('Please check that your encounter id for your prediction and input are in the same order!!')
    sys.exit(0)

print('Calculating evaluation')

prediction_langs = list( set( prediction_langs ) & set( reference_langs ) )

references = {}
predictions = {}
reference_weights = []

for prediction_lang in prediction_langs :
    references[ prediction_lang ] = []
    predictions[ prediction_lang ] = []

df_userinfo = pd.read_csv( '{}/df_userinfo.csv'.format( reference_dir ) )

for ind, reference_instance in enumerate( truth ) :
    reference_weights.append( get_ref_scores( reference_instance[ 'responses' ], df_userinfo ) )
    for prediction_lang in prediction_langs :
        
        refs = [ x[ 'content_{}'.format( prediction_lang ) ] for x in reference_instance[ 'responses' ] ]
        hyp = prediction[ ind ][ 'responses' ][0][ 'content_{}'.format( prediction_lang ) ]
        
        references[ prediction_lang ].append( refs )
        predictions[ prediction_lang ].append( hyp )

print('Scores:')
scores = {}

for pred_lang in prediction_langs :
    # if pred_lang == 'zh' :
    #     delatbleu = sacrebleu_deltableu.corpus_bleu_t( predictions[ pred_lang ],
    #                                     references[ pred_lang ],
    #                                     ref_weights= reference_weights,
    #                                     tokenize='zh' )
    # else :
    #     delatbleu = sacrebleu_deltableu.corpus_bleu_t( predictions[ pred_lang ],
    #                                     references[ pred_lang ],
    #                                     ref_weights= reference_weights )

    deltableu = sacrebleu.corpus_bleu(predictions[ pred_lang ], references[ pred_lang ], ref_weights=reference_weights)
    # print( deltableu )
    scores[ 'deltableu{}'.format( pred_lang) ] = deltableu.score


print(scores)

with open(os.path.join(score_dir, 'scores.json'), 'w') as score_file:
    score_file.write(json.dumps(scores))
