def parse_ticket(raw):
    raise NotImplementedError('TODO: strict JSON contract')

def remaining_tokens(limit,input_tokens,reserved_output):
    raise NotImplementedError('TODO: context budget')

def call_cost(input_tokens,output_tokens,cached_tokens,prices):
    raise NotImplementedError('TODO: cost with cached input')

def wrap_untrusted(text,tag):
    raise NotImplementedError('TODO: delimiters for untrusted data')

def weights_memory_gb(params,bits):
    raise NotImplementedError('TODO: weight memory estimate')
