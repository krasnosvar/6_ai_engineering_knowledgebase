def slice_accuracy(rows):
    raise NotImplementedError('TODO: per-slice quality')

def citations_allowed(cited_ids,context_ids):
    raise NotImplementedError('TODO: references cannot invent sources')

def position_bias_check(verdicts_ab,verdicts_ba):
    raise NotImplementedError('TODO: compare verdicts in both orders')

def judge_calibration(human,judge):
    raise NotImplementedError('TODO: agreement, kappa, false approvals')

def guard_tool_call(call,allowlist,needs_approval):
    raise NotImplementedError('TODO: allow, confirm or deny a tool call')
