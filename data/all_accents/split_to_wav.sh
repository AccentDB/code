for file in *.wav
do
	python3 alt_split.py "$file" --output-dir all_accents_out/ --min-silence-length=2 --silence-threshold=0.01
done
