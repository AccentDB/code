cd all_accents_out
for i in *.wav                                                                                                                                  ✔  ⚙  00:54:25 
do
    sox "$i" ../all_accents_trim/"$i" trim 0 300                       
done
