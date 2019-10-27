# accentNet

`repo.tree` contains the structure of the repo including `.npy` and `.wav` files. These files are not tracked by git. 

### Preprocessing .wav recordings

#### Step 1: Convert .mp3 files to .wav
Use the following script to convert all .mp3 files to .wav files. 
```
for file in *.mp3                                                                                                             
do
  ffmpeg -i "$file" "$file".wav
done
```
This makes .wav files with <filename>.mp3.wav names from which the .mp3 can be removed using a bulk remave via:
```
$ qmv -f do
```

#### Step 2: Split hour long .wav recordings to sentence level    
        
 This is done using `split_to_wav.py` present in the corresponding folders or a generic file `helpers/alt_split.py`.
 The splitting is done based on silence thresholds in terms of duration and energy. The threholds that were used for the experiments are noted below:
```

Splitting Bangla_Arc.wav where energy is below 1.0% for longer than 2.0s.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉| 20134/20143 [00:43<00:00, 459.96it/s]
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 778/778 [00:13<00:00, 56.96it/s]
Splitting Bangla_Jay.wav where energy is below 1.0% for longer than 2.0s.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉| 19824/19833 [00:44<00:00, 447.85it/s]
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 750/750 [00:06<00:00, 110.16it/s]
Splitting Malayalam_Hab.wav where energy is below 1.0% for longer than 2.0s.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉| 19902/19911 [01:01<00:00, 323.10it/s]
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 751/751 [00:08<00:00, 84.67it/s]
Splitting Malayalam_Sal.wav where energy is below 1.0% for longer than 2.0s.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉| 19969/19978 [00:59<00:00, 334.94it/s]
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 28/28 [00:11<00:00,  2.54it/s]
Splitting Malayalam_Sha.wav where energy is below 1.0% for longer than 2.0s.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉| 23904/23913 [01:06<00:00, 357.02it/s]
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 895/895 [00:23<00:00, 38.31it/s]
Splitting Odiya_Suc.wav where energy is below 1.0% for longer than 2.0s.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉| 19675/19684 [01:06<00:00, 294.34it/s]
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 120/120 [00:09<00:00, 12.26it/s]
Splitting Telugu_Nav.wav where energy is below 1.0% for longer than 2.0s.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉| 19554/19563 [00:54<00:00, 356.87it/s]
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 766/766 [00:09<00:00, 83.00it/s]
Splitting Telugu_Tho.wav where energy is below 1.0% for longer than 2.0s.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉| 19347/19356 [01:06<00:00, 291.94it/s]
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 749/749 [00:07<00:00, 95.36it/s]

Updated with:
Splitting /home/enigmaeth/accentPhase2/data/all_accents/Malayalam_Sal.wav where energy is below 0.1% for longer than 2.0s.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉| 19969/19978 [00:45<00:00, 443.22it/s]
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 747/747 [00:08<00:00, 91.82it/s]


Splitting /home/enigmaeth/accentPhase2/data/all_accents/Odiya_Suc.wav where energy is below 0.1% for longer than 2.0s.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉| 19675/19684 [00:41<00:00, 470.82it/s]
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 747/747 [00:08<00:00, 85.22it/s]

```
The number of files produced per recording is noted in the tqdm output above. For example: 747 files for the last row here.
Most files are around 5 seconds while some files are 13 to 14 seconds long.

#### Step 3: Trim all files to 5s.
Run script similar to `/data/all_accents/all_accents_trim.sh` to trim all files to less than 5s. This command runs using `sox`, details here: https://stackoverflow.com/questions/9667081/how-do-you-trim-the-audio-files-end-using-sox

#### Step 4: Generate X and Y vectors for training

└── `speech2vec`        
        &nbsp;&nbsp;&nbsp;&nbsp;├── `all_split.sh` : bash script to run all models on a given X and Y npy vectors.   
        &nbsp;&nbsp;&nbsp;&nbsp;├── `gen_x.py`: generate MFCC vectors for all files in specified folder.       
        &nbsp;&nbsp;&nbsp;&nbsp;├── `gen_y.py`: generate class labels for all files in specified folder.   
        &nbsp;&nbsp;&nbsp;&nbsp;├── `mfcc.py`: MFCC utilty.    
        
 `*.npy*` files are stored in `/data/numpy_vectors` or in the corresponding folder for some experiments.    
 
--------
### Step 5: Classification using initial run with MFCC

Run the following colabs for 2 experimental setups.
1. [conv1d on all_accents](https://colab.research.google.com/drive/1Z5vg1eRU3zCskrlTc2kp1y9xzUx8P9H8?authuser=2#scrollTo=Zz0tpQ_kiQNo)
2. [train_on_one_person_and_test_on_other](https://colab.research.google.com/drive/1dMZxbFCPBc2gJkNM47F_j7lDtvVaDhxb?authuser=2#scrollTo=koL6wrhIq_em)

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
