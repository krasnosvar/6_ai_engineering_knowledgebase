import numpy as np  # пригодится в ivf_candidates


def authorized_topk(rows,tenant,k):
    raise NotImplementedError('TODO: filter before ranking')

def rrf(rankings,k=60):
    raise NotImplementedError('TODO: reciprocal rank fusion')

def ann_recall_at_k(approx_ids,exact_ids,k):
    raise NotImplementedError('TODO: ANN recall against exact search')

def ivf_candidates(query,centers,cell,n_probe):
    raise NotImplementedError('TODO: documents of n_probe nearest cells')
