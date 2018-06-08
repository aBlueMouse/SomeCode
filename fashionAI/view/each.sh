python submit_each.py --cloth blouse --ann result_blouse_0407.csv
python submit_each.py --cloth skirt --ann result_skirt_0407.csv
python submit_each.py --cloth outwear --ann result_outwear_0407.csv
python submit_each.py --cloth dress --ann result_dress_0407.csv
python submit_each.py --cloth trousers --ann result_trousers_0407.csv

cat title.csv submit_bluse.csv submit_skirt.csv submit_outwear.csv submit_dress.csv submit_trousers.csv > submission_each_0407.csv
