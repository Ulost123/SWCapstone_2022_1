import numpy as np
import os
import json 
import easydict

import torch
import torch.multiprocessing as mp

from core.philly import ompi_size, ompi_local_size, ompi_rank, ompi_local_rank
from core.philly import get_master_ip, gpu_indices, ompi_universe_size
from core.utils import set_seed
from core.trainer import Trainer


args = easydict.EasyDict
(
  {
    "config": '/content/drive/MyDrive/SW_capstone/PCN-main/FISH_Net/configs/places2.json', 
    "name": 'pennet4', 
    "mask": 'square', 
    "size": 256, 
    "exam": 'store_true'
  }
)

def main_worker(gpu, ngpus_per_node, config):
  if 'local_rank' not in config:
    config['local_rank'] = config['global_rank'] = gpu
  if config['distributed']:
    torch.cuda.set_device(int(config['local_rank']))
    print('using GPU {} for training'.format(int(config['local_rank'])))
    torch.distributed.init_process_group(backend = 'nccl', 
      init_method = config['init_method'],
      world_size = config['world_size'], 
      rank = config['global_rank'],
      group_name='mtorch'
    )
  
  set_seed(config['seed'])

  config['save_dir'] = os.path.join(config['save_dir'], '{}_{}_{}{}'.format(config['model_name'], 
    config['data_loader']['name'], config['data_loader']['mask'], config['data_loader']['w']))
  if (not config['distributed']) or config['global_rank'] == 0:
    os.makedirs(config['save_dir'], exist_ok=True)
    print('[**] create folder {}'.format(config['save_dir']))

  trainer = Trainer(config, debug=args.exam)
  trainer.train()


if __name__ == "__main__":
  print('check if the gpu resource is well arranged on philly')
  assert ompi_size() == ompi_local_size() * ompi_universe_size()
  
  # loading configs 
  config = json.load(open(args.config))
  if args.mask is not None:
    config['data_loader']['mask'] = args.mask
  if args.size is not None:
    config['data_loader']['w'] = config['data_loader']['h'] = args.size
  config['model_name'] = args.name
  config['config'] = args.config

  # setup distributed parallel training environments
  world_size = ompi_size()
  ngpus_per_node = torch.cuda.device_count()
  if world_size > 1:
    config['world_size'] = world_size
    config['init_method'] = 'tcp://' + get_master_ip() + args.port
    config['distributed'] = True
    config['local_rank'] = ompi_local_rank()
    config['global_rank'] = ompi_rank()
    main_worker(0, 1, config)
  elif ngpus_per_node > 1:
    config['world_size'] = ngpus_per_node
    config['init_method'] = 'tcp://127.0.0.1:'+ args.port 
    config['distributed'] = True
    mp.spawn(main_worker, nprocs=ngpus_per_node, args=(ngpus_per_node, config))
  else:
    config['world_size'] = 1 
    config['distributed'] = False
    main_worker(0, 1, config)
