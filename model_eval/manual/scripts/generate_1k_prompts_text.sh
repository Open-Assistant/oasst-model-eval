#!/bin/bash
python subsample_dataset.py --input-file ~/LAION/exports/2023-03-07_oasst_all_with_labels.gz --lang en --only-prompt --state prompt_lottery_waiting -k 100 --output-file 00_en_100_seed_2637670843.jsonl --seed 2637670843 --only-text
python subsample_dataset.py --input-file ~/LAION/exports/2023-03-07_oasst_all_with_labels.gz --lang en --only-prompt --state prompt_lottery_waiting -k 100 --output-file 01_en_100_seed_3522131311.jsonl --seed 3522131311 --only-text
python subsample_dataset.py --input-file ~/LAION/exports/2023-03-07_oasst_all_with_labels.gz --lang en --only-prompt --state prompt_lottery_waiting -k 100 --output-file 02_en_100_seed_3772407843.jsonl --seed 3772407843 --only-text
python subsample_dataset.py --input-file ~/LAION/exports/2023-03-07_oasst_all_with_labels.gz --lang en --only-prompt --state prompt_lottery_waiting -k 100 --output-file 03_en_100_seed_1591628218.jsonl --seed 1591628218 --only-text
python subsample_dataset.py --input-file ~/LAION/exports/2023-03-07_oasst_all_with_labels.gz --lang en --only-prompt --state prompt_lottery_waiting -k 100 --output-file 04_en_100_seed_3853958079.jsonl --seed 3853958079 --only-text
python subsample_dataset.py --input-file ~/LAION/exports/2023-03-07_oasst_all_with_labels.gz --lang en --only-prompt --state prompt_lottery_waiting -k 100 --output-file 05_en_100_seed_0409526259.jsonl --seed 0409526259 --only-text
python subsample_dataset.py --input-file ~/LAION/exports/2023-03-07_oasst_all_with_labels.gz --lang en --only-prompt --state prompt_lottery_waiting -k 100 --output-file 06_en_100_seed_0798925925.jsonl --seed 0798925925 --only-text
python subsample_dataset.py --input-file ~/LAION/exports/2023-03-07_oasst_all_with_labels.gz --lang en --only-prompt --state prompt_lottery_waiting -k 100 --output-file 07_en_100_seed_3504426902.jsonl --seed 3504426902 --only-text
python subsample_dataset.py --input-file ~/LAION/exports/2023-03-07_oasst_all_with_labels.gz --lang en --only-prompt --state prompt_lottery_waiting -k 100 --output-file 08_en_100_seed_3570948328.jsonl --seed 3570948328 --only-text
python subsample_dataset.py --input-file ~/LAION/exports/2023-03-07_oasst_all_with_labels.gz --lang en --only-prompt --state prompt_lottery_waiting -k 100 --output-file 09_en_100_seed_0600081992.jsonl --seed 0600081992 --only-text
 
