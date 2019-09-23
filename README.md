# accentNet

`repo.tree` contains the structure of the repo including `.npy` and `.wav` files. These files are not tracked by git. 

### Preprocessing .wav recordings

└── `speech2vec`        
        &nbsp;&nbsp;&nbsp;&nbsp;├── `all_split.sh` : bash script to run all models on a given X and Y npy vectors.   
        &nbsp;&nbsp;&nbsp;&nbsp;├── `gen_x.py`: generate MFCC vectors for all files in specified folder.       
        &nbsp;&nbsp;&nbsp;&nbsp;├── `gen_y.py`: generate class labels for all files in specified folder.   
        &nbsp;&nbsp;&nbsp;&nbsp;├── `mfcc.py`: MFCC utilty.    
        
 `*.npy*` files are stored in `/data/numpy_vectors`.    
 
--------
### Initial run with MFCC

The results can be found inside `data/numpy_vectors/terminal.log`.

 Models ran:    
   > ├── `classification`    
    │    &nbsp;&nbsp;&nbsp;&nbsp;├── `attention_lstm.py`    
    │    &nbsp;&nbsp;&nbsp;&nbsp;├── `attention_utils.py`    
    │    &nbsp;&nbsp;&nbsp;&nbsp;├── `cnn_bilstm.py`    
    │    &nbsp;&nbsp;&nbsp;&nbsp;├── `conv_1d_model_aws.py`    
    │    &nbsp;&nbsp;&nbsp;&nbsp;├── `conv_1d_model.py`    
    │    &nbsp;&nbsp;&nbsp;&nbsp;├── `conv_1d_model_run.py`    
    
---------
