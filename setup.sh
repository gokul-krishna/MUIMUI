conda env create -f environment.yml -n muimui
conda activate muimui
git clone https://github.com/rarcega/instagram-scraper.git
cd instagram-scraper
python setup.py install
cd ..
rm -rf instagram-scraper/