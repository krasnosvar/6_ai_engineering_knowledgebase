def validate_action(action):
    raise NotImplementedError('TODO: allowlist and strict arguments')

def may_continue(steps,limit,cancelled):
    raise NotImplementedError('TODO: enforce cancellation and budget')

def handle_jsonrpc(request, tools, allowed):
    raise NotImplementedError('TODO: tools/list, tools/call, errors, allowlist')

def agent_tokens(system, per_step, steps):
    raise NotImplementedError('TODO: input tokens of one agent loop')

def multi_agent_cost(system, per_step, steps, workers, summary):
    raise NotImplementedError('TODO: workers plus two orchestrator calls')
