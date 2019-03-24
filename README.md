# Work Plan
For now we will track our work plan in `README.md`

we will use `nbs` folder for testing the ideas or frameworks in Jupyter notebooks.  
only tested code would be moved to `src`

## Tasks
- [x] Make list of Instagram (ig) influencers 
- [x] Make list of Websites to scrape
- [ ] Prioritize the type of wardrobe we are going to focus on `V0`
- [ ] Decide on ig scraping mechanism
- [ ] Make template for website scraping
- [ ] Get a working version of auto-encoder notebook for the open fashion dataset
... add all the task here

# Environment Setup
We will be using a ubuntu image for hosting server to make things simple
run the [setup script](setup.sh) to install the required dependencies and set up the required environment

To work make *muimui* conda environment in jupyter run the following commands:
```bash
pip install ipykernel
python -m ipykernel install --user --name myenv --display-name "muimui"
```

We are using this [Instagram scraper](https://github.com/rarcega/instagram-scraper)