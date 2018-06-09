python submit_each.py --cloth blouse --ann result_blouse_0516.csv
python submit_each.py --cloth skirt --ann result_skirt_0519.csv
python submit_each.py --cloth outwear --ann result_outwear_0525.csv
python submit_each.py --cloth dress --ann result_dress_0523.csv
python submit_each.py --cloth trousers --ann result_trousers_0501.csv

cat title.csv submit_bluse.csv submit_skirt.csv submit_outwear.csv submit_dress.csv submit_trousers.csv > submission_each_0526_2.csv
