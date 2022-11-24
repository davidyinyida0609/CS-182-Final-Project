
def mixup(batch1, batch2, alpha = 0.5):
    ''' We want to combine batch1 and batch2 into the mixuped version: lambda * batch1 + (1-lambda) * batch2
    lambda follows a predetermined beta distribution beta(alpha, alpha).
    For each batch, we need to mixup a lot of things:
        past trajectories
        neighbor info (edge and history)
        map (it should be None)
        robot info (it should be None)
        future trajectories
        DON'T MIXUP FIRST INDEX HISTORY
    You should look into dataset/preprocessing.py and trajectron.py

    Also, some of the past trajectories might contain NAN values.
    This is because each agent has a limited moving time in the map
    Fortunately, we could use first_history_index to index out the first
    valid non-Nane value. ALl the values after that should be fine.

    When we mixup two things, we need to consider both potential NAN info:
    1. if both are NAN, just leave it
    2. if one of them is NAN, use the other non-NONE without mixup
    3. if both of them are non-NAN, use standard mixup
    We also need to update the first_history_index when we change the first non-NAN value through mixup.'''
    lam = None
    mixup_batch = None
    return mixup_batch, lam