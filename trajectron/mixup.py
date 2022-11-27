import torch
import numpy as np
from model.dataset import*

def mixup(batch, dist = np.random.beta, alpha = 0.5):
     ''' We want to combine batch and permuted_batch into the mixuped version: lambda * batch + (1-lambda) * permuted_batch
     lambda follows a predetermined beta distribution beta(alpha, alpha).

     When we mixup two things, we need to consider both possible NAN values:
     1. if both are NAN, just leave it
     2. if one of them is NAN, use the other non-NONE without mixup
     3. if both of them are non-NAN, use standard mixup
     We also need to update the first_history_index when we change the first non-NAN value through mixup.
     For each batch, we have the following information: (first_history_index,
         x_t, y_t, x_st_t, y_st_t,
         neighbors_data_st,
         neighbors_edge_value,
         robot_traj_st_t,
         map) = batch
     The main idea originates from here: https://arxiv.org/pdf/1710.09412.pdf'''
     (first_history_index,
         x_t, y_t, x_st_t, y_st_t,
         neighbors_data_st,
         neighbors_edge_value,
         robot_traj_st_t,
         map) = batch
     batch_size = first_history_index.size(0)
     # Sample lambda from predefined distribution
     # We need to cast it into float
     lam = torch.tensor(dist(alpha, alpha, size = (batch_size, 1, 1))).float()
     # Sample permuted indicies
     indices = torch.randperm(batch_size)

     # Apply mixup to input based on sampled lambda and permuted indices.
     # We need use first_history_index to find the first non-zero history index
     # We also need to update the first_history_index because the combination might result in earlier history information.
     mixup_x_t, updated_first_history_index_t = helper_mixup(x_t, lam, indices, first_history_index)
     mixup_x_st, updated_first_history_index_st = helper_mixup(x_st_t, lam, indices, first_history_index)
     if not torch.all(updated_first_history_index_st == updated_first_history_index_t):
          raise AssertionError("We have different first history index for standardized and non-standardized inputs.")
     rest = [y_t, y_st_t, neighbors_data_st, neighbors_edge_value, robot_traj_st_t, map] 
     rest = [helper_mixup(each, lam, indices) for each in rest]
     mixup_batch = [updated_first_history_index_st, mixup_x_t, rest[0], mixup_x_st, *rest[1:]]
     assert len(mixup_batch) == len(batch)
     return mixup_batch, lam


def helper_mixup(x, lam, indices, first_history_index = None):
     '''This function takes in x and returns lam*x+(1-lam)x[indices], where lam is the
     weight sampled out from the predefined distribution and indices are a permutation of the
     mini-batch. We might need to handle NAN entries based on first_history_index for x_t and x_st_t.
     We might also need to all None x.'''
     # If x is None, we simply return as it is
     if x == None:
          return None
     
     if type(x) is torch.Tensor and first_history_index is None:
          # We are dealing with raw non-NAN values tensors
          assert not torch.any(torch.isnan(x))
          mixup_x = lam*x + (1-lam)*x[indices]
          return mixup_x
     elif type(x) is torch.Tensor:
          # We are dealing with possible-NAN values tensors.
          # The output is NAN at the place if and only if the entry 
          # for both x and permuted x is NAN at the place.

          # NOTE: torch.argmin operation behaves differently in 1.4 according to documentation
          # It will return the index of the last smallest element instead of the first, so we instead 
          # use np.argmin, which returns the index of the first smallest element instead of the last.
     
          # create permuted_x by permuting the indices
          permuted_x = x[indices]
          # helper tensor to track where x and permuted_x is NAN
          x_nan_or_not = torch.isnan(x)
          permuted_x_nan_or_not = torch.isnan(permuted_x)

          # check whether our self implementation is the same as the preprocessing one
          manual_first_history_index = find_first_false_index(x_nan_or_not)
          # We check whether the self-implemented finding first non-NAn history index the same as the default one
          assert torch.all(manual_first_history_index == first_history_index)

          # We replace all NAN with 0
          # Do everything on the copy
          x = x.clone()
          x[x_nan_or_not] = 0
          permuted_x[permuted_x_nan_or_not] = 0

          lam_x = lam*x
          one_minus_lam_x = (1-lam)*permuted_x
          # apply mixup as if there isn't any NAN
          no_nan_mixup_x = lam_x + one_minus_lam_x
          
          # get the entry where both are NAN
          is_nan_both = x_nan_or_not & permuted_x_nan_or_not
          # the entry of mixup_x is NAN if and only if the entry of x and permuted_x is both NAN
          mixup_x = torch.where(is_nan_both, torch.tensor(float('nan')), no_nan_mixup_x.float())

          # check whether the mixup result improve the first history index and matches the logic.
          dummy = find_first_false_index(permuted_x_nan_or_not)
          updated_first_history_index = find_first_false_index(is_nan_both)
          smallest = torch.where(dummy < manual_first_history_index, dummy, manual_first_history_index) 
          assert torch.all(smallest == updated_first_history_index)
          
          return mixup_x, updated_first_history_index
     elif type(x) is bytes:
          x = restore(x)
          mixup = dict()
          for k, v in x.items():
               output = []
               for i in range(len(v)):
                    # tensor [#edges] or list of [#PH, #state]
                    curr = v[i]
                    index = indices[i]
                    # tensor [#edges] or list of [#PH, #state]
                    permuted_one = v[index]
                    flag = False
                    if type(curr) is tuple or type(curr) is list:
                         # check the other is also list
                         assert type(permuted_one) is list or type(permuted_one) is tuple
                         # whether the neighbors data is empty
                         if len(curr) == 0 and len(permuted_one) == 0:
                              output.append([])
                              continue
                         elif len(permuted_one) == 0:
                              output.append(torch.unbind(lam[[i]] * torch.stack(curr, dim = 0), dim = 0))
                              continue
                         elif len(curr) == 0:
                              output.append(torch.unbind((1 -lam[[i]]) * torch.stack(permuted_one, dim = 0), dim = 0))
                              continue
                         else:
                              flag = True
                              curr = torch.stack(curr, dim = 0)
                              permuted_one = torch.stack(permuted_one, dim = 0)
                    
                    # We need to pad the smaller one into the same size
                    # as the greater one so we could mixup them together
                    if flag:
                         # lam is the same for each neighbor data
                         lam_i = lam[i].reshape(1, 1, 1)
                    else:
                         # lam is the same for each neighbor edge
                         lam_i = lam[i].reshape(-1)
                    if curr.size(0) < permuted_one.size(0):
                         dummy = torch.zeros_like(permuted_one)
                         dummy[:curr.size(0)] = curr
                         curr = dummy
                    else:
                         dummy = torch.zeros_like(curr)
                         dummy[:permuted_one.size(0)] = permuted_one
                         permuted_one = dummy
                    # combine the curr one with the permuted one
                    # [max(#neigh1, #neigh2), #PH, #state]
                    mixup_curr = lam_i*curr + (1-lam_i)*permuted_one
                    assert not torch.any(torch.isnan(mixup_curr))
                    # if the curr one is a list, we need to unbind it into a list
                    if flag:
                         output.append(torch.unbind(mixup_curr, dim = 0))
                    else:
                         output.append(mixup_curr)
               mixup[k] = output
                    # check whether there is any NAN value
                    
          return mixup

     else:
          raise AssertionError("Receive invalid type data for mixup operation")
def find_first_false_index(x):
     nan_or_not = torch.any(x, dim = -1).type(torch.uint8).numpy()
     return torch.tensor(np.argmin(nan_or_not, axis = -1))


